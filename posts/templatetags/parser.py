"""@package docstring
Extra template functions

@author 7Pros
@copyright
"""
from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter
@stringfilter
def parse_post_content(content):
    pattern = re.compile(r"#(\w+).*?", flags=re.IGNORECASE | re.UNICODE)
    parsed_content = pattern.sub(create_hashtag_url, content)

    return parsed_content


def create_hashtag_url(matchobj):
    url = reverse('posts:hashtags', kwargs={'hashtag_name': matchobj.group(0).lstrip('#')})
    return '<a class="hashtag" href="' + url + '">' + matchobj.group(0) + '</a>'
