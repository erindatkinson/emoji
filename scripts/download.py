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

select_query = "SELECT count(*) FROM downloads WHERE emoji=? and namespace=?"
insert_query = "INSERT INTO downloads VALUES (?, ?)"
download_dir = "emojis"
debug = False

def download(input_file, db="./downloads.db", namespace="hashicorp", listDir="./lists", ):
  print("performing setup")
  setup_db(db)
  makedirs(join(download_dir, namespace), exist_ok=True)

  print("getting new list")
  with open(input_file) as fp:
    raw = loads(fp.read())["emoji"]
  
  print("filtering emoji and aliases")
  emoji = dict(filter(lambda elem: "https://emoji.slack-edge.com" in elem[1], raw.items()))
  aliases = dict(filter(lambda elem: "alias:" in elem[1], raw.items()))

  print("filtering emoji previously downloaded")
  to_download = set([])
  conn = connect(db)
  with conn:
    for e in emoji.keys():
      for row in conn.execute(select_query, (e, namespace)):
        if row[0] == 1:
          continue
        to_download.add(e)
  
  
  print("downloading new emoji")
  for d in to_download:
    ext = splitext(emoji[d])
    debug_print(f"Downloading emoji {d}{ext[1]}")
    r = get(emoji[d])
    debug_print("writing emoji")
    with open(join(download_dir, namespace, f"{d}{ext[1]}"), 'wb') as fp:
      for chunk in r.iter_content(chunk_size=128):
        fp.write(chunk)
    debug_print("adding emoji to db")
    with conn:
      if conn.execute(insert_query, (d, namespace)).rowcount != 1:
        print(f"error adding {d} to downloads table")

  to_copy = set([])
  with conn:
    for a in aliases.keys():
      for row in conn.execute(select_query, (a, namespace)):
        if row[0] == 1:
          continue
        to_copy.add(a)
  for c in to_copy:
    name = c.split(":")
    downloaded = listdir(join(download_dir, namespace))
    for d in downloaded:
      ext = splitext(d)
      if name == ext[0]:
        print(f"Copying {d} to alias {c}")
        copyfile(join(download_dir, namespace, d), join(download_dir, namespace, f"{c}{ext[1]}"))
    with conn:
      if conn.execute(insert_query, (c, namespace)).rowcount != 1:
        print(f"error adding {c} to downloads table")

  conn.close()

def gen(namespace="hashicorp"):
  makedirs(f"docs/{namespace}", exist_ok=True)
  emoji = sorted(listdir(join(download_dir, namespace)))

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
    out = template.render(emojis=chunk, page=count, dir=join("/", download_dir, namespace))
    first_letter = chunk[0][0][0]

    with open(f"docs/{namespace}/page-{first_letter}-{count:04d}.md", 'w') as fp:
      fp.write(out)
    count += 1

  readme_tpl_str = """

  # Emojis


  {% for count in range(total) -%}
  * [{{pages[count] | replace('.md', '') | replace('-', ' ')|title}}](/docs/{{ns}}/{{pages[count]}})
  {% endfor %}
  """

  with open(f"docs/{namespace}/index.md", 'w') as fp:
    files = sorted(listdir(f"docs/{namespace}"))
    pages = [file for file in files if "page" in file]
    fp.write(Template(readme_tpl_str).render(pages=pages, total=count, ns=namespace))



def setup_db(db):
  conn = connect(db)

  with conn:
    conn.execute("CREATE TABLE IF NOT EXISTS downloads (emoji text, namespace text)")
  
  conn.close()

def debug_print(msg):
  if debug:
    print(msg)

if __name__ == "__main__":
  Fire({
    "get": download,
    "gen": gen
  })