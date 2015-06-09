"""@package docstring
Extra template functions for posts.

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
    """
    It parses a string replacing hashtags and mentions with urls of those.

    @param content: string - content to be parsed.

    @return string - with the parsed hashtags and mentions
    """
    pattern = re.compile(r"#(\w+).*?", flags=re.IGNORECASE | re.UNICODE)
    parsed_content_with_hashtags = pattern.sub(createHashtagURL, content)
    pattern = re.compile(r"@(\w+).*?", flags=re.IGNORECASE | re.UNICODE)
    parsed_content_complete = pattern.sub(createMentionURL, parsed_content_with_hashtags)
    return parsed_content_complete


def createHashtagURL(matchobj):
    """
    Receives a matched object with a hashtag in the .group(0) and returns the url from it.

    @param matchobj: MatchObj - given through pattern.sub.

    @return hashtag between <a></a> HTML tags
    """
    return '<a class="hashtag" href="/posts/show/' + matchobj.group(0).lstrip('#') + '/">' + matchobj.group(0) + '</a>'


def createMentionURL(matchobj):
    """
    Receives a matched object with a mention in the .group(0) and returns the url from it.

    @param matchobj: MatchObj - given through pattern.sub.

    @return hashtag between <a></a> HTML tags
    """
    return '<a class="mention" href="/users/' + matchobj.group(0).lstrip('@') + '/">' + matchobj.group(0) + '</a>'