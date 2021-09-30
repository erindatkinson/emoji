from fire import Fire
from json import loads, dumps
from re import compile
from pprint import pprint

handle = compile('(@[\d\w.]+)')

def run(inFile, outFile=""):
  if outFile == "":
    outFile = inFile
  outData = {"responses":[]}
  with open(inFile, 'r') as fp:
    data = loads(fp.read())
    
  for bot in data["responses"]:
    party = False
    for trigger in bot["triggers"]:
      if "party" in trigger:
        party = True
    if party:
      outData["responses"].append(bot)
  
  with open(outFile, 'w') as fp:
    fp.write(dumps(outData))

if __name__ == "__main__":
  Fire({
    "filter": run,
  })