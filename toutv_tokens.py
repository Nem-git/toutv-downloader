from urllib.parse import urlencode
from urllib.request import build_opener, HTTPCookieProcessor, Request
from io import StringIO as StringIO 
import http.cookiejar as cookielib
import sys
import gzip
import requests
import json
import base64
import time
import tools




def login(settings_path: str) -> tuple[str, str, str]:
    email, password, wvd_path, custom_string = tools.read_creds_from_file(file_path=settings_path)
    a_token = ""
    x_token = ""

    try:
        headers = tools.read_tokens()
        if not verify_premium(headers["Authorization"]):
            a_token = get_access_token(email, password)
            x_token = get_x_token(a_token)

    except:
        try:
            a_token = get_access_token(email, password)
            x_token = get_x_token(a_token)
        except:
            a_token = ""
            x_token = ""
    
    headers = {"Authorization" : a_token, "x-claims-token" : x_token}

    tools.write_tokens("toutv_tokens", headers)

    return headers, wvd_path, custom_string


def verify_premium(auth_token: str) -> bool:

    decrypted_auth = base64.b64decode(auth_token.split(".")[1] + "==").decode(encoding="ascii")
    time_auth = json.loads(decrypted_auth)["exp"]
    
    if time_auth < time.time():
        print("You need to refresh your Authorization Token")
        return False
    
    return True


def get_x_token(access_token: str):

    url = "https://services.radio-canada.ca/ott/subscription/v2/toutv/subscriber/profile?device=web"
    r = requests.get(url, headers={"Authorization": access_token})
    resp = r.json()

    token = resp["claimsToken"]

    return token



def get_access_token(email: str, password: str):

    #params = GET_AUTHORISE("https://rcmnb2cprod.b2clogin.com/rcmnb2cprod.onmicrosoft.com/B2C_1A_ExternalClient_FrontEnd_Login/oauth2/v2.0/authorize?client_id=ebe6e7b0-3cc3-463d-9389-083c7b24399c&nonce=85e7800e-15ba-4153-ac2f-3e1491918111&redirect_uri=https%3A%2F%2Fici.tou.tv%2Fauth-changed&scope=openid%20offline_access%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Foidc4ropc%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fprofile%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Femail%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.write%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-validation.read%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-validation%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-meta%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-drmt%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Ftoutv-presentation%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Ftoutv-profiling%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmetrik%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fsubscriptions.write%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.info%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.create%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.modify%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.reset-password%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.send-confirmation-email%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.delete%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fsubscriptions.validate%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Ftoutv&response_type=id_token%20token&response_mode=fragment&prompt=login&state=ZDY1Nzg2YzctZDQ4YS00YWRjLWEwNDMtMGI2MWIyM2UyZjUxfHsiYWN0aW9uIjoibG9naW4iLCJyZXR1cm5VcmwiOiIvIiwiZnJvbVN1YnNjcmlwdGlvbiI6ZmFsc2V9&state_value=ZDY1Nzg2YzctZDQ4YS00YWRjLWEwNDMtMGI2MWIyM2UyZjUxfHsiYWN0aW9uIjoibG9naW4iLCJyZXR1cm5VcmwiOiIvIiwiZnJvbVN1YnNjcmlwdGlvbiI6ZmFsc2V9&ui_locales=fr")
    params = GET_AUTHORISE("https://rcmnb2cprod.b2clogin.com/rcmnb2cprod.onmicrosoft.com/B2C_1A_ExternalClient_FrontEnd_Login/oauth2/v2.0/authorize?client_id=ebe6e7b0-3cc3-463d-9389-083c7b24399c&redirect_uri=https%3A%2F%2Fici.tou.tv%2Fauth-changed&scope=openid%20offline_access%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Femail%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.create%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.delete%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.info%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.modify%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.reset-password%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.account.send-confirmation-email%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fid.write%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-drmt%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-meta%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-validation%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmedia-validation.read%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fmetrik%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Foidc4ropc%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fott-profiling%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fott-subscription%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fprofile%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fsubscriptions.validate%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Fsubscriptions.write%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Ftoutv%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Ftoutv-presentation%20https%3A%2F%2Frcmnb2cprod.onmicrosoft.com%2F84593b65-0ef6-4a72-891c-d351ddd50aab%2Ftoutv-profiling&response_type=id_token%20token")

    data = {'email': email, 'request_type': 'RESPONSE'}
    valassert1 = GET_SELF_ASSERTED(params, data)

    tokenS1 = GET_ACCESS_TOKEN_MS(False, valassert1)

    data = {'email': email, 'request_type': 'RESPONSE', 'password': password}
    valassert2 = GET_SELF_ASSERTED(tokenS1[0], data)

    tokenS2 = GET_ACCESS_TOKEN_MS(True, valassert2)
    
    tokenS3 = tokenS2[1].split("access_token=")
    access_token = tokenS3[1].split("&token_type")
    accessToken = access_token[0]

    return "Bearer " + accessToken


def handleHttpResponse(response):
    if sys.version_info.major >= 3:
        if response.info().get('Content-Encoding') == 'gzip':
            f = gzip.GzipFile(fileobj=response)
            data = f.read()
            return data
        else:
            data = response.read()
            return data
    else:
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read() )
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            return data
        else:
            return response.read()

def BYTES_PY2(bytesOrString):
    if sys.version_info.major >= 3:
        return bytes(bytesOrString, encoding='utf8')
    else:
        return bytesOrString

def GET_AUTHORISE(url):

    cookiejar = cookielib.LWPCookieJar()
    cookie_handler = HTTPCookieProcessor(cookiejar)
    opener = build_opener(cookie_handler)

    request = Request(url)
    request.get_method = lambda: "GET"
    
    response = opener.open(request)
    text = handleHttpResponse(response)

    parts = text.split(BYTES_PY2("StateProperties="), 1)
    #parts = text.split(bytes("StateProperties=", encoding='utf8'), 1)
    parts = parts[1].split(BYTES_PY2("\""), 1)
    #parts = parts[1].split(bytes("\"", encoding='utf8'), 1)
    #print(m)
    state = parts[0]

    return cookiejar, state


def GET_SELF_ASSERTED( params, data ):

    csrf = None
    
    for c in params[0]:
        if c.name == "x-ms-cpim-csrf":
            csrf = c.value

    url = "https://rcmnb2cprod.b2clogin.com/rcmnb2cprod.onmicrosoft.com/B2C_1A_ExternalClient_FrontEnd_Login/SelfAsserted?tx=StateProperties=" + params[1].decode('utf-8') + "&p=B2C_1A_ExternalClient_FrontEnd_Login"

    cookie_handler = HTTPCookieProcessor(params[0])
    opener = build_opener(cookie_handler)

    opener.addheaders = [
    ('X-CSRF-TOKEN', csrf)
    ]

    post_data = urlencode(data)

    request = Request(url, data=BYTES_PY2(post_data))
    #request = Request(url, data=bytes(post_data, encoding='utf8'))
    request.get_method = lambda: "POST"
    
    response = opener.open(request)

    rawresp = handleHttpResponse(response)
    #print(rawresp)

    return params[0], params[1]


def GET_ACCESS_TOKEN_MS(modeLogin, params ):

    csrf = None
    
    for c in params[0]:
        if c.name == "x-ms-cpim-csrf":
            csrf = c.value

    url = None
    if modeLogin == True:
        url = "https://rcmnb2cprod.b2clogin.com/rcmnb2cprod.onmicrosoft.com/B2C_1A_ExternalClient_FrontEnd_Login/api/CombinedSigninAndSignup/confirmed?rememberMe=true&csrf_token=" + csrf + "&tx=StateProperties=" + params[1].decode('utf-8') + "&p=B2C_1A_ExternalClient_FrontEnd_Login&diags=%7B%22pageViewId%22%3A%2226127485-f667-422c-b23f-6ebc0c422705%22%2C%22pageId%22%3A%22CombinedSigninAndSignup%22%2C%22trace%22%3A%5B%7B%22ac%22%3A%22T005%22%2C%22acST%22%3A1632790122%2C%22acD%22%3A4%7D%2C%7B%22ac%22%3A%22T021%20-%20URL%3Ahttps%3A%2F%2Fmicro-sites.radio-canada.ca%2Fb2cpagelayouts%2Flogin%2Fpassword%3Fui_locales%3Dfr%22%2C%22acST%22%3A1632790122%2C%22acD%22%3A36%7D%2C%7B%22ac%22%3A%22T019%22%2C%22acST%22%3A1632790122%2C%22acD%22%3A5%7D%2C%7B%22ac%22%3A%22T004%22%2C%22acST%22%3A1632790122%2C%22acD%22%3A2%7D%2C%7B%22ac%22%3A%22T003%22%2C%22acST%22%3A1632790122%2C%22acD%22%3A4%7D%2C%7B%22ac%22%3A%22T035%22%2C%22acST%22%3A1632790122%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T030Online%22%2C%22acST%22%3A1632790122%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T002%22%2C%22acST%22%3A1632790129%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T018T010%22%2C%22acST%22%3A1632790128%2C%22acD%22%3A695%7D%5D%7D"
        url = "https://rcmnb2cprod.b2clogin.com/rcmnb2cprod.onmicrosoft.com/B2C_1A_ExternalClient_FrontEnd_Login/api/CombinedSigninAndSignup/confirmed?rememberMe=true&csrf_token=" + csrf + "&tx=StateProperties=" + params[1].decode('utf-8') + "&p=B2C_1A_ExternalClient_FrontEnd_Login&diags=%7B%22pageViewId%22%3A%22fef7143d-a216-4fa8-a066-cbfa7c315a93%22%2C%22pageId%22%3A%22CombinedSigninAndSignup%22%2C%22trace%22%3A%5B%7B%22ac%22%3A%22T005%22%2C%22acST%22%3A1730670125%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T021%20-%20URL%3Ahttps%3A%2F%2Fmicro-sites.radio-canada.ca%2Fb2cpagelayouts%2Flogin%2Fpassword%22%2C%22acST%22%3A1730670125%2C%22acD%22%3A40%7D%2C%7B%22ac%22%3A%22T019%22%2C%22acST%22%3A1730670125%2C%22acD%22%3A2%7D%2C%7B%22ac%22%3A%22T004%22%2C%22acST%22%3A1730670125%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T003%22%2C%22acST%22%3A1730670125%2C%22acD%22%3A1%7D%2C%7B%22ac%22%3A%22T035%22%2C%22acST%22%3A1730670125%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T030Online%22%2C%22acST%22%3A1730670125%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T002%22%2C%22acST%22%3A1730670148%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T018T010%22%2C%22acST%22%3A1730670147%2C%22acD%22%3A348%7D%5D%7D"
    else:
        url = "https://rcmnb2cprod.b2clogin.com/rcmnb2cprod.onmicrosoft.com/B2C_1A_ExternalClient_FrontEnd_Login/api/SelfAsserted/confirmed?csrf_token=" + csrf + "&tx=StateProperties=" + params[1].decode('utf-8') + "&p=B2C_1A_ExternalClient_FrontEnd_Login&diags=%7B%22pageViewId%22%3A%2222e91666-af5b-4d27-b6f0-e9999cb0b66c%22%2C%22pageId%22%3A%22SelfAsserted%22%2C%22trace%22%3A%5B%7B%22ac%22%3A%22T005%22%2C%22acST%22%3A1633303735%2C%22acD%22%3A3%7D%2C%7B%22ac%22%3A%22T021%20-%20URL%3Ahttps%3A%2F%2Fmicro-sites.radio-canada.ca%2Fb2cpagelayouts%2Flogin%2Femail%3Fui_locales%3Dfr%22%2C%22acST%22%3A1633303735%2C%22acD%22%3A154%7D%2C%7B%22ac%22%3A%22T019%22%2C%22acST%22%3A1633303735%2C%22acD%22%3A3%7D%2C%7B%22ac%22%3A%22T004%22%2C%22acST%22%3A1633303735%2C%22acD%22%3A5%7D%2C%7B%22ac%22%3A%22T003%22%2C%22acST%22%3A1633303735%2C%22acD%22%3A1%7D%2C%7B%22ac%22%3A%22T035%22%2C%22acST%22%3A1633303735%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T030Online%22%2C%22acST%22%3A1633303735%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T017T010%22%2C%22acST%22%3A1633303742%2C%22acD%22%3A699%7D%2C%7B%22ac%22%3A%22T002%22%2C%22acST%22%3A1633303742%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T017T010%22%2C%22acST%22%3A1633303742%2C%22acD%22%3A700%7D%5D%7D"
        url = "https://rcmnb2cprod.b2clogin.com/rcmnb2cprod.onmicrosoft.com/B2C_1A_ExternalClient_FrontEnd_Login/api/SelfAsserted/confirmed/?csrf_token=" + csrf + "&tx=StateProperties=" + params[1].decode('utf-8') + '&p=B2C_1A_ExternalClient_FrontEnd_Login&diags=%7B%22pageViewId%22%3A%22ced09dac-0687-48c9-87de-f5a60d4ae43f%22%2C%22pageId%22%3A%22SelfAsserted%22%2C%22trace%22%3A%5B%7B%22ac%22%3A%22T005%22%2C%22acST%22%3A1730670689%2C%22acD%22%3A1%7D%2C%7B%22ac%22%3A%22T021%20-%20URL%3Ahttps%3A%2F%2Fmicro-sites.radio-canada.ca%2Fb2cpagelayouts%2Flogin%2Femail%22%2C%22acST%22%3A1730670689%2C%22acD%22%3A64%7D%2C%7B%22ac%22%3A%22T019%22%2C%22acST%22%3A1730670689%2C%22acD%22%3A2%7D%2C%7B%22ac%22%3A%22T004%22%2C%22acST%22%3A1730670689%2C%22acD%22%3A3%7D%2C%7B%22ac%22%3A%22T003%22%2C%22acST%22%3A1730670689%2C%22acD%22%3A1%7D%2C%7B%22ac%22%3A%22T035%22%2C%22acST%22%3A1730670689%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T030Online%22%2C%22acST%22%3A1730670689%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T017T010%22%2C%22acST%22%3A1730671535%2C%22acD%22%3A447%7D%2C%7B%22ac%22%3A%22T002%22%2C%22acST%22%3A1730671536%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T017T010%22%2C%22acST%22%3A1730671535%2C%22acD%22%3A448%7D%5D%7D'

    #cookiejar = cookielib.LWPCookieJar()
    cookie_handler = HTTPCookieProcessor(params[0])
    opener = build_opener(cookie_handler)

    request = Request(url)
    request.get_method = lambda: "GET"
    
    response = opener.open(request)
    text = handleHttpResponse(response)

    #print(response.geturl())
    return params, response.geturl()


