from sqlite3 import connect
from fire import Fire
from os.path import isdir, basename, splitext
from os import mkdir
from json import loads
from pprint import pprint
from urllib.parse import urlparse





def init(
  db_path,
  output_path="output",
  setup_query='''CREATE TABLE IF NOT EXISTS downloads 
                 (namespace text, name text, created_at text, last_updated text)'''):
  with connect(db_path) as db:
    db.execute(setup_query)

  if not isdir(output_path):
    mkdir(output_path)
  
def already_downloaded(namespace, name, db_path):
  with connect(db_path) as db:
    cursor = db.cursor()
    cursor.execute("SELECT namespace, name FROM downloads WHERE name=:emoji AND namespace=:team", {"emoji": name, "team": namespace})
    data = cursor.fetchall()
  if len(data) != 0:
    return True
  else:
    return False

def download(file_path, db_path='downloads.db'):
  init(db_path)
  with open(file_path) as fp:
    rawdict = loads(fp.read())
  
  emojidict = {k: v for (k, v) in rawdict["emoji"].items() if "alias" not in v}
  aliasdict = {k: v for (k, v) in rawdict["emoji"].items() if "alias" in v}

  for emoji, url_string in emojidict.items():
    try:
      url = urlparse(url_string)
      extension = splitext(basename(url.path))[1]
      print(f"{emoji}:{already_downloaded(emoji, 'hashicorp', db_path)}")
    except AttributeError as ae:
      if type(url_string) == dict:
        continue
      else:
        print(ae)
        break
    except Exception as e:
      print(e)



  


if __name__ == "__main__":
  Fire(download)