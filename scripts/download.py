#!/usr/bin/env python3
from sqlite3 import connect
from fire import Fire
from os.path import splitext, join
from os import listdir, makedirs
from json import loads
from requests import get
from shutil import copyfile, rmtree
from jinja2 import Template
from lib import templates, helpers

class Downloader(object):
  def __init__(self, db="./downloads.db", downloadDir="emojis", listDir="lists", namespace="hashicorp"):
    self.db = db
    self.ns = namespace
    self.downloadDir = downloadDir
    self.listDir = listDir

    self.nsDownload = join(downloadDir, namespace)
    self.conn = connect(db)
    helpers.setup_db(self.db)

  # download runs the logic to download any new emoji in the list given.
  def download(self, input_file):
    makedirs(self.nsDownload, exist_ok=True)

    print("getting new list")
    with open(input_file) as fp:
      raw = loads(fp.read())["emoji"]
    
    print("filtering previously downloaded emoji and aliases")
    emoji = dict(filter(lambda elem: "https://emoji.slack-edge.com" in elem[1], raw.items()))
    aliases = dict(filter(lambda elem: "alias:" in elem[1], raw.items()))
    
    to_download = set([])
    with self.conn:
      for e in emoji.keys():
        for row in self.conn.execute(templates.select_query, (e, self.ns)):
          if row[0] == 1:
            continue
          to_download.add(e)
    
    print("downloading new emoji")
    for d in to_download:
      ext = splitext(emoji[d])
      helpers.debug_print(f"Downloading emoji {d}{ext[1]}")
      r = get(emoji[d])
      helpers.debug_print("writing emoji")
      with open(join(self.nsDownload, f"{d}{ext[1]}"), 'wb') as fp:
        for chunk in r.iter_content(chunk_size=128):
          fp.write(chunk)
      helpers.debug_print("adding emoji to db")
      with self.conn:
        if self.conn.execute(templates.insert_query, (d, self.ns)).rowcount != 1:
          print(f"error adding {d} to downloads table")

    print("copying new aliases")
    to_copy = set([])
    with self.conn:
      for a in aliases.keys():
        for row in self.conn.execute(templates.select_query, (a, self.ns)):
          if row[0] == 1:
            continue
          to_copy.add(a)
    for c in to_copy:
      name = c.split(":")
      downloaded = listdir(self.nsDownload)
      for d in downloaded:
        ext = splitext(d)
        if name == ext[0]:
          helpers.debug_print(f"Copying {d} to alias {c}")
          copyfile(join(self.nsDownload, d), join(self.nsDownload, f"{c}{ext[1]}"))
      with self.conn:
        if self.conn.execute(templates.insert_query, (c, self.ns)).rowcount != 1:
          print(f"error adding {c} to downloads table")

    self.conn.close()



  def gen(self):
    rmtree(f"docs/{self.ns}")
    makedirs(f"docs/{self.ns}", exist_ok=True)
    emoji      = sorted(listdir(self.nsDownload))
    split      = list(map(lambda x: splitext(x), emoji))
    template   = Template(templates.tpl_str)
    pages_list = [(split[i:i + 100][0][0][0],int(i/100), split[i:i + 100]) for i in range(0, len(emoji), 100)]

    for i in range(len(pages_list)):
      z_next, f_next, z_prev, f_prev = helpers.get_surrounding(pages_list, i)
        
      out = template.render(
        count=pages_list[i][1], 
        z_next=z_next,
        z_prev=z_prev,
        f_next=f_next,
        f_prev=f_prev,
        emojis=pages_list[i][2], 
        dir=join("/", self.nsDownload),
        ns=self.ns)


      with open(f"docs/{self.ns}/page-{pages_list[i][0]}-{pages_list[i][1]:04d}.md", 'w') as fp:
        fp.write(out)

    
    with open(f"docs/{self.ns}/index.md", 'w') as fp:
      files = sorted(listdir(f"docs/{self.ns}"))
      pages = [file for file in files if "page" in file]
      fp.write(Template(templates.readme_tpl_str).render(pages=pages, total=pages_list[-1][1], ns=self.ns))

if __name__ == "__main__":
  Fire(Downloader)