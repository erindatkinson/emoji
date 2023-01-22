select_query = "SELECT count(*) FROM downloads WHERE emoji=? and namespace=?"
insert_query = "INSERT INTO downloads VALUES (?, ?)"

tpl_str ="""
## Emojis (Page {{count}})

{% if z_prev != "" -%}
[Previous Page](/docs/{{ns}}/page-{{f_prev}}-{{z_prev}}.md)  
{%- endif -%}

{% if z_next != "" %}
  | [Next Page](/docs/{{ns}}/page-{{f_next}}-{{z_next}}.md)  
{%- endif %}

<hr />

|Emoji Name|Image|
| :-: | :-: |
{%- for emoji in emojis %}
|{{emoji[0]}}| ![{{emoji[0]}}]({{dir | replace('./', '/')}}/{{emoji[0]}}{{emoji[1]}})|
{%- endfor %}

<hr/>

{% if z_prev != "" -%}
[Previous Page](/docs/{{ns}}/page-{{f_prev}}-{{z_prev}}.md)  
{%- endif -%}

{% if z_next != "" %}
  | [Next Page](/docs/{{ns}}/page-{{f_next}}-{{z_next}}.md)  
{%- endif -%}
"""


readme_tpl_str = """

# Emojis


{% for count in range(total) -%}
* [{{pages[count] | replace('.md', '') | replace('-', ' ')|title}}](/docs/{{ns}}/{{pages[count]}})
{% endfor %}
"""

