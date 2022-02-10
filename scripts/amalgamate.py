#!/usr/bin/env python3
import json
import os
import os.path

lists = list(filter(lambda x: "emoji" in x, os.listdir("./lists")))

emoji = {
  "ok": True,
  "emoji": {}
}

for l in lists:
  with open(os.path.join("./lists/", l)) as fp:
    data = json.loads(fp.read())
    for k,v in data["emoji"].items():
      emoji["emoji"][k]=v

with open("full_list.json", 'w') as fp:
  fp.write(json.dumps(data))

print(len(emoji["emoji"].items()))