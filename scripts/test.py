from os import listdir
from json import loads, dumps
from os.path import join


lists = list(map(
  lambda x: join("./lists/", x), 
  list(filter(
    lambda x: "emoji" in x, 
    listdir("./lists")))))

full = "full_list.json"

list_objs = []

for l in lists:
  with open(l) as fp:
    list_objs.append(loads(fp.read()))
with open(full) as fp:
  full_objs = loads(fp.read())
  list_emojis=set([])
for obj in list_objs:
  for emoji in obj["emoji"].keys():
    list_emojis.add(emoji)

print(len(list_emojis))

