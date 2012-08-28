import re

from django.template import Library

from ..utils import reverse_hotlink

register = Library()
hotlinks_regex = re.compile(r'\[(\w+.\w+.\d+[^\[\]]*)\]')

def replace_link(match):
    link = reverse_hotlink(match.group(1))
    if link is None:
        return match.group(0)
    else:
        return link

@register.filter
def hotlinks(content):
    return hotlinks_regex.sub(replace_link, content)

