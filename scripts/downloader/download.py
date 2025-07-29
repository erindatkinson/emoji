#!/usr/bin/env python
"""downloader"""

from sqlite3 import connect
from shutil import copyfile, rmtree
from os.path import splitext, join
from os import listdir, makedirs
from json import loads
from requests import get
from jinja2 import Template
from fire import Fire
from lib import templates, helpers


class Downloader(object):
    """downloader"""

    def __init__(self, db="./downloads.db", download_dir="emojis", namespace="hc"):
        self.db = db
        self.ns = namespace
        self.download_dir = download_dir

        self.ns_download = join(download_dir, namespace)
        self.conn = connect(db)
        helpers.setup_db(self.db)

    def admin_download(self, input_file):
        """download runner"""
        makedirs(self.ns_download, exist_ok=True)
        print("getting new list")
        with open(input_file, encoding='utf-8') as fp:
            raw = loads(fp.read())["emoji"]
        for emoji in raw:
            url = emoji['url']
            name = emoji['name']
            ext = splitext(url)
            print(f"Downloading emoji {name}{ext[1]}")
            r = get(url, timeout=60)
            with open(join(self.ns_download, f"{name}{ext[1]}"), "wb") as fp:
                for chunk in r.iter_content(chunk_size=128):
                    fp.write(chunk)

    # download runs the logic to download any new emoji in the list given.
    def download(self, input_file):
        """download runner"""
        makedirs(self.ns_download, exist_ok=True)

        print("getting new list")
        with open(input_file, encoding='utf-8') as fp:
            raw = loads(fp.read())["emoji"]

        print("filtering previously downloaded emoji and aliases")
        emoji = dict(
            filter(lambda elem: "https://emoji.slack-edge.com" in elem[1], raw.items())
        )
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
            r = get(emoji[d], timeout=60)
            helpers.debug_print("writing emoji")
            with open(join(self.ns_download, f"{d}{ext[1]}"), "wb") as fp:
                for chunk in r.iter_content(chunk_size=128):
                    fp.write(chunk)
            helpers.debug_print("adding emoji to db")
            with self.conn:
                if (
                    self.conn.execute(templates.insert_query, (d, self.ns)).rowcount
                    != 1
                ):
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
            downloaded = listdir(self.ns_download)
            for d in downloaded:
                ext = splitext(d)
                if name == ext[0]:
                    helpers.debug_print(f"Copying {d} to alias {c}")
                    copyfile(
                        join(self.ns_download, d), join(self.ns_download, f"{c}{ext[1]}")
                    )
            with self.conn:
                if (
                    self.conn.execute(templates.insert_query, (c, self.ns)).rowcount
                    != 1
                ):
                    print(f"error adding {c} to downloads table")

        self.conn.close()

    def gen(self):
        """generate docs runner"""
        rmtree(f"docs/{self.ns}")
        makedirs(f"docs/{self.ns}", exist_ok=True)
        emoji = sorted(listdir(self.ns_download))
        split = list(map(splitext, emoji))
        template = Template(templates.tpl_str)
        pages_list = [
            (split[i : i + 100][0][0][0], int(i / 100), split[i : i + 100])
            for i in range(0, len(emoji), 100)
        ]

        # pylint: disable=consider-using-enumerate
        for i in range(len(pages_list)):
            z_next, f_next, z_prev, f_prev = helpers.get_surrounding(pages_list, i)

            out = template.render(
                count=pages_list[i][1],
                z_next=z_next,
                z_prev=z_prev,
                f_next=f_next,
                f_prev=f_prev,
                emojis=pages_list[i][2],
                dir=join("/", self.ns_download),
                ns=self.ns,
            )

            with open(
                f"docs/{self.ns}/page-{pages_list[i][0]}-{pages_list[i][1]:04d}.md", "w",
                encoding='utf-8'
            ) as fp:
                fp.write(out)

        with open(f"docs/{self.ns}/index.md", "w", encoding='utf-8') as fp:
            files = sorted(listdir(f"docs/{self.ns}"))
            pages = [file for file in files if "page" in file]
            fp.write(
                Template(templates.readme_tpl_str).render(
                    pages=pages, total=pages_list[-1][1], ns=self.ns
                )
            )


if __name__ == "__main__":
    Fire(Downloader)
