import base64
import requests

from episode import Episode


class Pssh:

    def Get(self, episode: Episode) -> str:

        r: requests.Response = requests.get(episode.url)

        while not r.ok:
            r: requests.Response = requests.get(episode.url)
        
        resp = r.content

        offsets = []
        offset = 0
        while True:
            # Find where pssh is written in the file
            offset = resp.find(b"pssh", offset)

            if offset == -1:
                break

            # WTF
            size: int = int.from_bytes(bytes=resp[offset - 4 : offset], byteorder="big")
            pssh_offset = offset - 4
            offsets.append(resp[pssh_offset : pssh_offset + size])
            offset += size
        
        pssh_list: str = []
        for offset in offsets:
            pssh_list.append(base64.b64encode(offset).decode())
        

        target_pssh: str

        # No idea what this does
        for pssh in pssh_list:
            #if 20 < len(pssh) < 220:
            target_pssh = pssh

        #if not options.quiet:
        #    print(f"PSSH KEY: {target_pssh}")

        return target_pssh