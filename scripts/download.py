#!/usr/bin/env python3
from sqlite3 import connect
import sqlite3
from fire import Fire
from os.path import isdir, basename, splitext, join
from os import listdir, makedirs
from json import loads
from pprint import pprint
from urllib.parse import urlparse
from requests import get
from shutil import copyfile
from jinja2 import Template

select_query = "SELECT count(*) FROM downloads WHERE emoji=?"
insert_query = "INSERT INTO downloads VALUES (?)"

def run(input_file, db="./downloads.db", outputDir="./output", listDir="./lists"):
  makedirs(outputDir, exist_ok=True)

  with open(input_file) as fp:
    raw = loads(fp.read())["emoji"]
  
  emoji = dict(filter(lambda elem: "https://emoji.slack-edge.com" in elem[1], raw.items()))
  aliases = dict(filter(lambda elem: "alias:" in elem[1], raw.items()))

  to_download = set([])
  conn = connect(db)
  with conn:
    for e in emoji.keys():
      for row in conn.execute(select_query, (e,)):
        if row[0] == 1:
          continue
        to_download.add(e)
  
  
  for d in to_download:
    ext = splitext(emoji[d])
    print(f"Downloading emoji {d}{ext[1]}")
    r = get(emoji[d])
    with open(join(outputDir, f"{d}{ext[1]}"), 'wb') as fp:
      for chunk in r.iter_content(chunk_size=128):
        fp.write(chunk)
    with conn:
      if conn.execute(insert_query, (d,)).rowcount != 1:
        print(f"error adding {d} to downloads table")

  to_copy = set([])
  with conn:
    for a in aliases.keys():
      for row in conn.execute(select_query, (a,)):
        if row[0] == 1:
          continue
        to_copy.add(a)
  for c in to_copy:
    name = c.split(":")
    downloaded = listdir(outputDir)
    for d in downloaded:
      ext = splitext(d)
      if name == ext[0]:
        print(f"Copying {d} to alias {c}")
        copyfile(join(outputDir, d), join(outputDir, f"{c}{ext[1]}"))
    with conn:
      if conn.execute(insert_query, (c,)).rowcount != 1:
        print(f"error adding {c} to downloads table")

  conn.close()

def gen(outputDir="./output"):
  emoji = sorted(listdir(outputDir))

  split = list(map(lambda x: splitext(x), emoji))

  tpl_str ="""
  ## Emojis (Page {{page}})
  |Emoji Name|Image|
  | :-: | :-: |
  {%- for emoji in emojis %}
  |{{emoji[0]}}| ![{{emoji[0]}}]({{dir | replace('./', '/')}}/{{emoji[0]}}{{emoji[1]}})|
  {%- endfor %}
  """

  template = Template(tpl_str)
  count = 0
  for i in range(0, len(emoji), 100):
    chunk = split[i:i + 100]
    out = template.render(emojis=chunk, page=count, dir=outputDir)
    first_letter = chunk[0][0][0]

    with open(f"docs/page-{first_letter}-{count:04d}.md", 'w') as fp:
      fp.write(out)
    count += 1

  readme_tpl_str = """

  # Emojis


  {% for count in range(total) -%}
  * [{{pages[count] | replace('.md', '') | replace('-', ' ')|title}}](/docs/{{pages[count]}})
  {% endfor %}
  """

  with open("docs/index.md", 'w') as fp:
    files = sorted(listdir('docs/'))
    pages = [file for file in files if "page" in file]
    fp.write(Template(readme_tpl_str).render(pages=pages, total=count))


if __name__ == "__main__":
  Fire({
    "run": run,
    "gen": gen
  })