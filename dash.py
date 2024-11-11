import base64
import subprocess
from pathlib import Path
import os
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import requests


def find_wv_pssh_offsets(raw: bytes) -> list[int]:
    offsets = []
    offset = 0
    while True:
        offset = raw.find(b"pssh", offset)
        if offset == -1:
            break
        size: int = int.from_bytes(bytes=raw[offset - 4 : offset], byteorder="big")
        pssh_offset = offset - 4
        offsets.append(raw[pssh_offset : pssh_offset + size])
        offset += size
    return offsets


def to_pssh(content: bytes) -> list:
    wv_offsets = find_wv_pssh_offsets(raw=content)
    return [base64.b64encode(s=wv_offset).decode() for wv_offset in wv_offsets]


def from_file(file_path: str) -> list[str]:
    return to_pssh(Path(file_path).read_bytes())


def get_pssh(mpd_link: str, quiet: bool):

    # Define yt-dlp download parameters

    file_path = f"{os.getcwd()}/init.mp4"
    
    command: str = f'yt-dlp -f bv --allow-u -o "{os.getcwd()}/init.mp4" --test "{mpd_link}"'
    command: list[str] = [
        "yt-dlp", #Command
        "-v", #Verbose
        "-f", #Format
        "bv", #Choose best video, but shouldnt matter
        "--allow-u", #Allow unplayable files to be downloaded
        "-o", #Output
        f"{os.getcwd()}/init.mp4", #Temporary file to recuperate pssh
        "--test", #No fucking clue ngl
        mpd_link #MPD link
    ]

    while True:
        try:
            if quiet:
                subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(command)
            
            break
        except:
            if not quiet:
                print("YT-dlp did not manage to download the init.mp4, trying again")
                

    pssh_list = from_file(file_path)
    target_pssh = None

    # No idea what this does
    for pssh in pssh_list:
        if 20 < len(pssh) < 220:
            target_pssh = pssh
    os.remove(file_path)

    if not quiet:
        print(f"PSSH KEY: {target_pssh}")

    return target_pssh


def setup_licence_challenge(pssh: str, licence_url: str, wvd_path: str, headers: str):

    # prepare pssh
    pssh = PSSH(data=pssh)

    # load device
    device: Device = Device.load(path=wvd_path)

    # load cdm
    cdm: Cdm = Cdm.from_device(device=device)

    # open cdm session
    session_id: bytes = cdm.open()

    # get license challenge
    challenge: bytes = cdm.get_license_challenge(session_id=session_id, pssh=pssh)

    # send license challenge (assuming a generic license server SDK with no API front)
    licence: requests.Response = requests.post(url=licence_url, headers=headers, data=challenge)

    licence.raise_for_status()

    # parse license challenge
    cdm.parse_license(session_id=session_id, license_message=licence.content)

    decryption_keys = []

    # print keys
    for key in cdm.get_keys(session_id=session_id):
        decryption_keys.append(f"{key.kid.hex}:{key.key.hex()}")
        print(decryption_keys[-1])

    # close session, disposes of session data
    cdm.close(session_id=session_id)

    return decryption_keys