import json
import threading

from DiscordMessenger import DiscordMessager

with open("config.json", 'r') as f:
    data = json.load(f)
    messengers = []
    for item in data:
        messenger = DiscordMessager(**item)
        if messenger.enable:
            messengers.append(messenger)


def run(obj):
    obj.start()


threads = []
for messenger in messengers:
    threads.append(threading.Thread(target=run, args=(messenger,)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("All threads are done")
