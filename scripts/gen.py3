#!/usr/bin/env python3
from json import loads
from os.path import splitext
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

  template = Template(tpl_str)
  count = 0
  for i in range(0, len(emojis), 100):
      out = template.render(emojis=emojis[i:i+100], page=count)
      
      with open(f"docs/page{count}.md", 'w') as fp:
          fp.write(out)
      count+=1


  readme_tpl_str = """

  # Emojis

  {% for count in range(pages) -%}
  * [Page {{count}}](docs/page{{count}}.md)
  {% endfor %}
  """
  with open("docs/index.md", 'w') as fp:
      fp.write(Template(readme_tpl_str).render(pages=count))

if __name__ == '__main__':
  Fire({
      'docs': doc_gen,
  })