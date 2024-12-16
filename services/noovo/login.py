
import base64
import json
import requests
import time

import common




class Login:
    # Logger

    subscriptions = None
    scopes = None
    packages = None
    #session = requests.Session()

    streaming_service_encoded_name: str
    streaming_service_name: str = "noovo"

    settings_path: str = "settings_"


    # ===================================================================
    #   LOGIN
    # ===================================================================


    def Login(self, options: common.Options) -> None:

        self.settings_path += self.streaming_service_name
        self.streaming_service_encoded_name = self.authorization_name(self.streaming_service_name)
        
        try:
            options.Load(self.settings_path)
        except:
            options.Write(self.settings_path)
            options.Load(self.settings_path)
        
        try:
            if not self.Verify_Expiration(options.authorization_token):
                self.Access_Token(options)
                options.Write(self.settings_path)
        except:
            try:
                self.Refresh_Token(options)
                options.Write(self.settings_path)
            except:
                options.authorization_token = ""
                options.claims_token = ""
                options.tier = "Free"


    def Access_Token(self, options: common.Options) -> None:
        # ===========================================================
        # Refresh token if possible
        # ===========================================================
        r: requests.Response = self.refresh_request(options)
        if r.status_code == 200:
            resp = r.json()
            options.authorization_token = f"Bearer {resp['access_token']}"
            options.claims_token = resp["refresh_token"]


    def Refresh_Token(self, options: common.Options) -> None:
        # ===========================================================
        # Do a username/password login if required
        # ===========================================================

        print('Trying username/password login...')
        r: requests.Response = self.login_request(options)
        if r.status_code == 200:
            resp = r.json()
            if resp["token_type"] == "Bearer":
                options.authorization_token = "Bearer "
            
            options.authorization_token += resp['access_token']
            options.claims_token = resp["refresh_token"]


    # ===================================================================
    #   TOKEN EXPIRY HANDLER
    # ===================================================================

    def Verify_Expiration(self, auth_token: str) -> bool:

        decrypted_auth: str = base64.b64decode(auth_token.split(".")[1] + "==").decode(encoding="ascii")
        time_auth: float = json.loads(decrypted_auth)["exp"]

        if time_auth < time.time():
            print("You need to refresh your Authorization Token")
            return False

        return True


    # ===================================================================
    #   REQUESTS
    # ===================================================================


    def refresh_request(self, options: common.Options) -> requests.Response:
        print('Making a refresh request...')
        url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=refresh_token'
        headers: dict[str, str] = {
            'accept-encoding': 'gzip',
            'authorization': f'Basic {self.streaming_service_encoded_name}',
            'connection': 'Keep-Alive',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'okhttp/4.9.0'
        }
        data = f'refresh_token={options.claims_token}'
        return requests.post(url=url, headers=headers, data=data)



    def login_request(self, options: common.Options) -> requests.Response:
        print('logging in user username and password...')

        url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=password'

        headers: dict[str, str] = {
            'accept-encoding': 'gzip',
            'authorization': f'Basic {self.streaming_service_encoded_name}',
            'connection': 'Keep-Alive',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'okhttp/4.9.0'
        }

        options.password = options.password.replace('&', '%26').replace('?', '%3F')
        data: str = f'password={options.password}&username={options.email}'

        return requests.post(url=url, headers=headers, data=data)



    def authorization_name(self, name: str) -> str:
        decoded = f"{name}-web:default"

        encoded = decoded.encode()
        b64 = base64.b64encode(encoded)
        return b64.decode()