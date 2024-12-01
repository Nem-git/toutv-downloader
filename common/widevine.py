
import pywidevine
import requests

from common.episode import Episode
from common.options import Options


class Widevine:

    def Challenge(self, episode: Episode, options: Options) -> list[str]:
        # prepare pssh
        pssh = pywidevine.PSSH(data=pssh)

        # load device
        device: pywidevine.Device = pywidevine.Device.load(path=options.wvd_path)

        # load cdm
        cdm: pywidevine.Cdm = pywidevine.Cdm.from_device(device=device)

        # open cdm session
        session_id: bytes = cdm.open()

        # get license challenge
        challenge: bytes = cdm.get_license_challenge(session_id=session_id, pssh=pssh)

        # send license challenge (assuming a generic license server SDK with no API front)
        licence: requests.Response = requests.post(url=episode.licence_url, headers=headers, data=challenge)

        licence.raise_for_status()

        # parse license challenge
        cdm.parse_license(session_id=session_id, license_message=licence.content)

        decryption_keys: list[str]

        # print keys
        for key in cdm.get_keys(session_id=session_id):
            decryption_keys.append(f"{key.kid.hex}:{key.key.hex()}")
            #print(decryption_keys[-1])

        # close session, disposes of session data
        cdm.close(session_id=session_id)

        return decryption_keys