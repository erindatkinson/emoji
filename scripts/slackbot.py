#!/usr/bin/env python3
from fire import Fire
from json import loads
from pprint import pprint

def listGen(file_path, match="party"):
    parties = []

    with open(file_path) as fp:
        responses = loads(fp.read())

    triggers = list(map(lambda x: x["triggers"], responses["responses"]))

    for triggerset in triggers:
        for trigger in triggerset:
            if match in trigger:
                parties.append(trigger)

    print(parties)


if __name__ == "__main__":
    Fire({
        "gen": listGen,
    })
