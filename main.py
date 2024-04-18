import json
import threading

from DiscordMessager import DiscordMessager

with open("config.json", 'r') as f:
    data = json.load(f)
    messagers = []
    for item in data:
        messager = DiscordMessager(**item)
        if messager.enable:
            messagers.append(messager)


def run(obj):
    obj.start()


threads = []
for item in messagers:
    threads.append(threading.Thread(target=run, args=(item,)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("All threads are done")
