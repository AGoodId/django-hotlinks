import re

from django.template import Library

from ..utils import reverse_hotlinks

register = Library()
hotlinks_regex = re.compile(r'\[(\w+.\w+.\d+[^\[\]]*)\]')

@register.filter
def hotlinks(content):
    # First fetch all substitutions
    hotlinks = hotlinks_regex.findall(content)
    substitutions = reverse_hotlinks(hotlinks)

    def replace_link(match):
        link = substitutions[ hotlinks.index(match.group(1)) ]
        if link is None:
            return match.group(0)
        else:
            return link

    # Replace all links
    return hotlinks_regex.sub(replace_link, content)

