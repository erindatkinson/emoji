from json import loads
from os.path import splitext
from pprint import pprint
from urllib.parse import urlparse
from jinja2 import Template


with open("emoji.list.json") as fp:
  list = loads(fp.read())

emojis = []
for name, url in list["emoji"].items():
    if type(url) == dict:
        continue
    else:
        path = urlparse(url).path
        fname, ext = splitext(path)
        emojis.append((name, f"output/{name}{ext}"))

tpl_str ="""
## Emojis

{% for emoji, url in emojis %}
  * {{emoji}}: ![{{emoji}}]({{url}})
{% endfor %}

"""

template = Template(tpl_str)
out = template.render(emojis=emojis)

with open("README.md", 'w') as fp_o:
    fp_o.write(out)