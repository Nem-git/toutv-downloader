from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import base64
from base64 import b64encode
import requests
import re
import xml.etree.ElementTree as ET
import subprocess
import os
from pathlib import Path



from common.episode import Episode
from common.video import Video
from common.options import Options




class Pssh:

    # Widevine System ID
    WIDEVINE_SYSTEM_ID = 'EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED'

    def Get(self, episode: Episode, video: Video, options: Options) -> None:
        episode.mpd_content = self.fetch_mpd_content(episode.url)

        video.pssh = self.extract_or_generate_pssh(episode.url, episode.mpd_content)
        print("Extracted or generated PSSH:", video.pssh)

        video.decryption_keys = self.get_key(video.pssh, episode.licence_url, options.wvd_path, options.license_headers)





    def fetch_mpd_content(self, url: str) -> bytes:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        mpd_content = response.content
        return mpd_content
    

    def find_default_kid_with_regex(self, mpd_content: bytes) -> str | None:
        # Regular expression to find cenc:default_KID
        match = re.search(r'cenc:default_KID="([A-F0-9-]+)"', str(mpd_content))
        if match:
            return match.group(1)
        return None

    def extract_or_generate_pssh(self, url: str, mpd_content: bytes) -> str:
        # Parse the MPD content using ElementTree
        # deal with:-
        #       the cenc namespace varitions
        #       the default_KID ``
        # Provide a regex fallback

        tree = ET.ElementTree(ET.fromstring(mpd_content))
        root = tree.getroot()

        # Namespace map to handle the cenc namespace
        namespaces = {
            'cenc': 'urn:mpeg:cenc:2013',
            '': 'urn:mpeg:dash:schema:mpd:2011'
        }

        # Extract cenc:default_KID using XML parsing
        default_kid = None
        for elem in root.findall('.//ContentProtection', namespaces):
            scheme_id_uri = elem.attrib.get('schemeIdUri', '').upper()
            if scheme_id_uri == 'URN:MPEG:DASH:MP4PROTECTION:2011':
                default_kid = elem.attrib.get('cenc:default_KID')
                if default_kid:
                    print(f"Found default_KID using XML parsing: {default_kid}")
                    break

        # If default_kid is not found using XML parsing, use regex
        if not default_kid:
            default_kid = self.find_default_kid_with_regex(mpd_content)
            if default_kid:
                print(f"Found default_KID using regex: {default_kid}")

        # Extract Widevine cenc:pssh
        pssh = None
        for elem in root.findall('.//ContentProtection', namespaces):
            scheme_id_uri = elem.attrib.get('schemeIdUri', '').upper()
            if scheme_id_uri == f'URN:UUID:{self.WIDEVINE_SYSTEM_ID}':
            
                pssh_elem = elem.find('cenc:pssh', namespaces)
                if pssh_elem is not None:
                    pssh = pssh_elem.text
                    print(f"Found pssh element: {pssh}")
                    break

        if pssh is not None:
            return pssh
        elif default_kid is not None:
            # Generate pssh from default_kid
            default_kid = default_kid.replace('-', '')
            s = f'000000387073736800000000edef8ba979d64acea3c827dcd51d21ed000000181210{default_kid}48e3dc959b06'
            return b64encode(bytes.fromhex(s)).decode()
        else:
            # No pssh or default_KID found
            try:
                return self.get_pssh_from_mpd(url)  # init.m4f method
            except:
                return ""


    def get_key(self, pssh: str, license_url: str, wvd_path: str, headers: dict[str, str]) -> list[str]:
        """
        Retrieves a license key for a given PSSH and license URL.

        Args:
            pssh (str): The PSSH value.
            license_url (str): The URL of the license server.

        Returns:
            str: A string containing the license keys, separated by newlines.

        Raises:
            requests.HTTPStatusError: If there is an HTTP status error while making the request.

        Note:
            This function uses the Cdm class to interact with the device and retrieve the license key.
            It first calls the `get_license_challenge` method of the Cdm instance to obtain the challenge.
            If the `data` parameter is not None, it modifies the challenge based on the pattern found in `data`.
            It then prepares the payload by using the modified challenge or the original challenge if `data` is None.
            The payload is sent to the license server using an HTTP POST request.
            The response content is then parsed to extract the license content
            The license content is then parsed using the `parse_license` method of the Cdm instance.
            The `get_keys` method of the Cdm instance is then used to retrieve the license keys.
            The license keys are returned as a string separated by newlines.
        """
        device: Device = Device.load(wvd_path)
        cdm: Cdm = Cdm.from_device(device)
        session_id: bytes = cdm.open()

        challenge: bytes = cdm.get_license_challenge(session_id, PSSH(pssh))

        #if data:
        #    # deal with sites that need to return data with the challenge
        #    if match := re.search(r'"(CAQ=.*?)"', data):  # fix for windows
        #        challenge = data.replace(match.group(1), base64.b64encode(challenge).decode())
        #    elif match := re.search(r'"(CAES.*?)"', data):
        #        challenge = data.replace(match.group(1), base64.b64encode(challenge).decode())
        #    elif match := re.search(r'=(CAES.*?)(&.*)?$', data): 
        #        b64challenge = base64.b64encode(challenge).decode()
        #        quoted = urllib.parse.quote_plus(b64challenge)
        #        challenge = data.replace(match.group(1), quoted)

        # Prepare the final payload
        #payload = challenge if data is None else challenge
        payload = challenge
    
        license_response = requests.post(url=license_url, data=payload, headers=headers)

        license_content = license_response.content
        try:
            # if content is returned as JSON object:
            match = re.search(r'"(CAIS.*?)"', license_response.content.decode('utf-8'))
            if match:
                license_content = base64.b64decode(match.group(1))
        except:
            pass

        # Ensure license_content is in the correct format
        if isinstance(license_content, str):
            license_content = base64.b64decode(license_content)

        cdm.parse_license(session_id, license_content)

        keys: list[str] = []
        for key in cdm.get_keys(session_id):
            if key.type == 'CONTENT':
                keys.append(f"{key.kid.hex}:{key.key.hex()}")

        cdm.close(session_id)

        return keys

    # deal with getting pssh from init.m4f as last resort

    def find_wv_pssh_offsets(self, raw: bytes) -> list[bytes]:
        offsets: list[bytes] = []
        offset = 0
        while True:
            offset: int = raw.find(b'pssh', offset)
            if offset == -1:
                break
            size: int = int.from_bytes(raw[offset-4:offset], byteorder='big')
            pssh_offset: int = offset - 4
            offsets.append(raw[pssh_offset:pssh_offset+size])
            offset += size
        return offsets

    def to_pssh(self, content: bytes) -> list[str]:
        wv_offsets = self.find_wv_pssh_offsets(content)
        return [base64.b64encode(wv_offset).decode() for wv_offset in wv_offsets]

    def extract_pssh_from_file(self, file_path: str) -> list[str]:
        print('Extracting PSSHs from init file:', file_path)
        return self.to_pssh(Path(file_path).read_bytes())

    def get_pssh_from_mpd(self, url: str) -> str:

        print("Extracting PSSH from MPD...")

        yt_dl = 'yt-dlp'
        init = 'init.m4f'

        files_to_delete = [init]

        for file_name in files_to_delete:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"{file_name} file successfully deleted.")

        try:
            subprocess.run([yt_dl, '-q', '--no-warning', '--test', '--allow-u', '-f', 'bestvideo[ext=mp4]/bestaudio[ext=m4a]/best', '-o', init, url])
        except FileNotFoundError:
            print("yt-dlp not found. Trying to download it...")
            subprocess.run(['pip', 'install', yt_dl])
            import yt_dlp


            ydl_opts = {
                'format': 'bestvideo[ext=mp4]/bestaudio[ext=m4a]/best',
                'allow_unplayable_formats': True,
                'no_warnings': True,
                'quiet': True,
                'outtmpl': init,
                'no_merge': True,
                'test': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        pssh_list: list[str] = self.extract_pssh_from_file(init)
        pssh: str = ""
        for target_pssh in pssh_list:
            if 20 < len(target_pssh) < 220:
                pssh = target_pssh

        print(f'\n{pssh}\n')
        # with open("pssh.txt", "a") as f:
            # f.write(f"{pssh}\n {mpd}\n")    


        for file_name in files_to_delete:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"{file_name} file successfully deleted.")
        
        return pssh
















#import base64
#import requests
#
#from common.options import Options
#from episode import Episode
#
#
#class Pssh:
#
#    def Get(self, episode: Episode) -> str:
#
#        r: requests.Response = requests.get(episode.url)
#
#        while not r.ok:
#            r: requests.Response = requests.get(episode.url)
#        
#        resp = r.content
#
#        offsets = []
#        offset = 0
#        while True:
#            # Find where pssh is written in the file
#            offset = resp.find(b"pssh", offset)
#
#            if offset == -1:
#                break
#
#            # WTF
#            size: int = int.from_bytes(bytes=resp[offset - 4 : offset], byteorder="big")
#            pssh_offset = offset - 4
#            offsets.append(resp[pssh_offset : pssh_offset + size])
#            offset += size
#        
#        pssh_list: str = []
#        for offset in offsets:
#            pssh_list.append(base64.b64encode(offset).decode())
#        
#
#        target_pssh: str
#
#        # No idea what this does
#        for pssh in pssh_list:
#            #if 20 < len(pssh) < 220:
#            target_pssh = pssh
#
#        #if not options.quiet:
#        #    print(f"PSSH KEY: {target_pssh}")
#
#        return target_pssh



#import logging
#from pywidevine.cdm import Cdm
#from pywidevine.device import Device
#from pywidevine.pssh import PSSH
#import httpx
#
#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)
#
#WVD_PATH = "/home/angela/Programming/WKS-KEYS/device.wvd"
#from headers import headers
#
#def get_key(pssh, license_url):
#    logger.debug("Loading device...")
#    device = Device.load(WVD_PATH)
#    cdm = Cdm.from_device(device)
#    session_id = cdm.open()
#    logger.debug("Session opened...")
#
#    challenge = cdm.get_license_challenge(session_id, PSSH(pssh))
#    response = httpx.post(license_url, data=challenge, headers=headers)
#    cdm.parse_license(session_id, response.content)
#
#    keys = []
#    logger.debug("Retrieving keys...")
#    for key in cdm.get_keys(session_id):
#        logger.debug(f"Key found: {key.kid.hex}:{key.key.hex()}, Type: {key.type}")
#        if key.type == 'CONTENT':
#            keys.append(f"--key {key.kid.hex}:{key.key.hex()}")
#
#    cdm.close(session_id)
#    logger.debug("Session closed...")
#    return "\n".join(keys)


