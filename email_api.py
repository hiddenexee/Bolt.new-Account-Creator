import time
import secrets
import requests

class Kopechka:
    def __init__(self, api_key: str, domain: str = "outlook.com") -> None:
        self.api_url = 'https://api.kopeechka.store/'
        self.api_key = api_key
        self.domain = domain

    def get_email(self):
        while True:
            try:
                response = requests.get(
                    f"{self.api_url}mailbox-get-email?site=stackblitz.com&mail_type={self.domain}&token={self.api_key}&api=2.0").json()
                if response["status"] == "OK":
                    return {"email": response["mail"], "password": secrets.token_hex(8) + '1D', "token": response["id"]}
                time.sleep(2)
            except Exception as ex:
                print(ex)

    def get_code(self, task_id):
        print(f"[*] Wait code... {task_id}")
        time.sleep(2)
        trying = 0
        while True:
            try:
                response = requests.get(
                    f"{self.api_url}mailbox-get-message?&id={task_id}&token={self.api_key}&type=json&api=2.0").json()
                if response["status"] == "OK":
                    return response["fullmessage"].split('confirmation_token=')[1].split('"')[0]
            except:
                pass
            if trying == 100:
                return ""
            trying += 1
            time.sleep(2)

    def cancel_kopchka(self, task_id):
        requests.get(f"{self.api_url}mailbox-cancel?id={task_id}&token={self.api_key}&type=JSON&api=2.0")




