"""@package docstring
Extra template functions

@author 7Pros
@copyright
"""
from django import template
from django.core.urlresolvers import reverse
from posts.views import PostsListView
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter
@stringfilter
def parse(content):
    pattern = re.compile(r"#(\w+).*?", flags=re.IGNORECASE | re.UNICODE)
    parsed_content_with_hashtags = pattern.sub(createHashtagURL, content)
    pattern = re.compile(r"@(\w+).*?", flags=re.IGNORECASE | re.UNICODE)
    parsed_content_complete = pattern.sub(createMentionURL, parsed_content_with_hashtags)
    return parsed_content_complete

def createHashtagURL(matchobj):
    return '<a class="hashtag" href="/posts/show/'+matchobj.group(0).lstrip('#')+'/">'+matchobj.group(0)+'</a>'

def createMentionURL(matchobj):
    return '<a class="mention" href="/users/'+matchobj.group(0).lstrip('@')+'/">'+matchobj.group(0)+'</a>'