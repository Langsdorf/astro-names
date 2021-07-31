import json
import random
import time

nameList = json.load(open("data.json","r", encoding='utf8'))

while(True):
    randomString = random.choice(nameList)
    print(randomString)
    time.sleep(0.5)