from datetime import datetime
import requests, time, json
from random import *

class DiscordMessager:
    def __init__(self, username, token, cooldown, channel_id, spam_times, messages, enable):
        self.username = username
        self.token = token
        self.cooldown = cooldown
        self.channel_id = channel_id
        self.spam_times = spam_times
        self.messages = messages
        self.enable = enable

    @classmethod
    def from_json(cls, json_string):
        json_data = json.loads(json_string)
        return cls(**json_data)

    def __repr__(self):
        return f"DiscordMessager(username={self.username}, token={self.token}, cooldown={self.cooldown}, channel_id={self.channel_id}, spam_times={self.spam_times}, messages={self.messages})"

    def start(self):
        if not self.enable:
            exit()
        global_headers = {
            'authorization': self.token,
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'zh-CN',
            'x-discord-timezone': 'Asia/Shanghai',
        }

        error_exit = 0

        for i in (range(int(self.spam_times))):
            message = choice(self.messages)
            payload = {
                "content": message,
                "nonce": randint(1, 100000),
                "tts": False
            }
            r = requests.request("POST", f"https://discord.com/api/v9/channels/{self.channel_id}/messages", json=payload,
                                 headers=global_headers)
            if r.status_code == 200:
                print(f"[Sucess] Message Sent in {self.channel_id} channel by user {self.username} at {datetime.now()}")
            elif r.status_code == 401:
                print("[Error] Your token might be invalid! Please check it")
                exit()
            elif r.status_code == 403:
                print(
                    "[Error] You might have been kicked out of the guild the token was previously sending message in, retrying...")
                error_exit = error_exit + 1
                if error_exit == 5:
                    print("[Error] Exiting due to token being kicked from the guide")
                    exit()
            elif r.status_code == 429:
                print("[Error] Spamming messages to fast! retrying...")
            else:
                zzz = r.json()
                print(f"[Error] Error while performing, error staus code: {r.status_code}, here is the error: {zzz}")
                error_exit = error_exit + 1
                if error_exit == 10:
                    print("[Error] Too many errors while requests, exiting.")
                    exit()
            time.sleep(self.cooldown)
        print("[Sucess] Finished Sending messages, exiting")