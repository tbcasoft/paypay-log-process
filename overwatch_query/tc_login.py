import json
import requests

def get_cookie():
    login_url = 'https://tc-2pn1ygvtl5.xiveh.com/tc/auth/login'
    login_data = {
        'username': 'casper',
        'password': 'hivex.casper'
    }

    session = requests.Session()
    response = session.post(login_url, data=login_data)

    if response.status_code == 200:
        print("Login successful")
        cookies = response.cookies
        for cookie in cookies:
            cookie_val = cookie.value
        print("cookie is:", cookie_val)
    else:
        print(response.status_code)
        print("Login failed")
    
    return cookie_val