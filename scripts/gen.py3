#!/usr/bin/env python3
from json import loads
from os.path import splitext
from os import listdir
from pprint import pprint
from urllib.parse import urlparse
from jinja2 import Template
from fire import Fire

def doc_gen(list_path):
  with open(list_path) as fp:
    list = loads(fp.read())

  emojis = []
  for name, url in list["emoji"].items():
      if type(url) == dict:
          continue
      else:
          path = urlparse(url).path
          fname, ext = splitext(path)
          emojis.append((name, f"/output/{name}{ext}"))

  tpl_str ="""
  ## Emojis (Page {{page}})
  |Emoji Name|Image|
  | :-: | :-: |
  {%- for emoji, url in emojis %}
  |{{emoji}}| ![{{emoji}}]({{url}})|
  {%- endfor %}
  """
  emoji_s = sorted(emojis)

  template = Template(tpl_str)
  count = 0
  for i in range(0, len(emoji_s), 100):
    chunk = emoji_s[i:i+100]
    out = template.render(emojis=chunk, page=count)
    first_letter = chunk[0][0][0]
      
    with open(f"docs/page-{first_letter}-{count}.md", 'w') as fp:
        fp.write(out)
    count+=1


  readme_tpl_str = """

  # Emojis


  {% for count in range(total) -%}
  * [{{pages[count] | replace('.md', '') | replace('-', ' ')|title}}](/docs/{{pages[count]}})
  {% endfor %}
  """
  with open("docs/index.md", 'w') as fp:
    files = sorted(listdir('docs/'))
    pages = [file for file in files if "page" in file]
    pprint(pages)
    fp.write(Template(readme_tpl_str).render(pages=pages, total=count))

if __name__ == '__main__':
  Fire({
      'docs': doc_gen,
  })