from episode import Episode

class File(Episode):
    path: str

    pssh: str
    decryption_keys: list[str]
    