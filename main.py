import requests
import threading
from email_api import Kopechka

class BoltNewRegister:
    def __init__(self, ref_code: str, proxy: str = None) -> None:
        self.ref_code = ref_code
        self.ref_url = f'https://bolt.new/?rid={self.ref_code}'
        self.base_url = 'https://bolt.new/'
        self.base_url_2 = 'https://stackblitz.com/'

        self.session = requests.Session()
        if proxy is not None:
            self.session.proxies = {'https': 'http://' + proxy}
        self.session.headers = {
            'Sec-Ch-Ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'tr-TR,tr;q=0.9',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive'
        }

        self.xpid = None
        self.state = None
        self.code_challenge = None

        self.email_api = Kopechka(kopechka_api_key, email_domain)
        self.email_info = self.email_api.get_email()
        self.email = self.email_info['email']
        self.username = self.email.split('@')[0].lower()
        self.password = self.email_info['password']


    def main_page(self) -> None:
        self.session.get(self.ref_url)

        payload = {
            'start': {
                'destination': f'/?rid={self.ref_code}',
                'rid': self.ref_code
            }
        }

        response = self.session.post(f'{self.base_url}api/sessions', json=payload).json()
        auth_url = response['authorizeUri']

        response = self.session.get(auth_url, allow_redirects=True)
        self.code_challenge = response.url.split('code_challenge%3D')[1].split('%26')[0]
        self.state = response.url.split('state%3D')[1].split('%26')[0]
        self.xpid = response.text.split('xpid:"')[1].split('"')[0]

    def register(self) -> bool:
        self.session.headers = {
            'X-Newrelic-Id': self.xpid,
            'Sec-Ch-Ua-Platform': '"Windows"',
            'X-Csrf-Token': self.session.cookies['CSRF-TOKEN'],
            'Sec-Ch-Ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://stackblitz.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'tr-TR,tr;q=0.9',
            'Priority': 'u=1, i'
        }
        payload = {
            'user': {
                'email': self.email,
                'username': self.username,
                'password': self.password,
                'password_confirmation': self.password
            }
        }

        response = self.session.post(
            f'{self.base_url_2}api/users/registrations',
            json=payload
        ).json()

        if 'sent to your email address' in str(response['message']):
            return True
        return False

    def confirmation(self) -> None:
        confirmation_token = self.email_api.get_code(self.email_info['token'])
        if confirmation_token != '':
            print(f"[+] Code => {confirmation_token}")
            self.session.headers = {
                'Sec-Ch-Ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Language': 'tr-TR,tr;q=0.9',
                'Priority': 'u=0, i'
            }
            self.session.get(
                f'{self.base_url_2}users/confirmation',
                params={
                    'confirmation_token': confirmation_token,
                },
                allow_redirects=True
            )
            self.oauth()
            print(f"[+] Created account => {self.username}")
            open("accounts.txt", "a+").write(f"{self.username}:{self.password}:{self.email}\n")
        else:
            print(f"[*] Not code => {self.email}")

    def oauth(self):
        headers = {
            'Sec-Ch-Ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'tr-TR,tr;q=0.9',
            'Priority': 'u=0, i'
        }

        params = {
            'client_id': 'bolt',
            'response_type': 'code',
            'redirect_uri': f'{self.base_url}oauth2',
            'code_challenge_method': 'S256',
            'code_challenge': self.code_challenge,
            'state': self.state,
            'scope': 'public',
            'rid': self.ref_code,
            'skip_register': '1'
        }

        self.session.get(f'{self.base_url_2}oauth/authorize', params=params, headers=headers, allow_redirects=True)

    def start(self) -> None:
        while True:
            self.main_page()
            if self.register():
                self.confirmation()
            self.email_api.cancel_kopchka(self.email_info['token'])

if __name__ == '__main__':
    kopechka_api_key = 'xxxx'
    email_domain = 'gmx.com'
    thread_count = 1

    for _ in range(thread_count):
        threading.Thread(target=BoltNewRegister('ref_code', None).start).start()
