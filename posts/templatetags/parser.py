"""@package posts.templatetags.parser
Extra template functions for posts.

@author 7Pros
@copyright
"""
import re

from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def parse_post_content(content):
    """
    It parses a string replacing hashtags and mentions with urls of those.

    @param content: string - content to be parsed.

    @return string - with the parsed hashtags and mentions
    """
    pattern = re.compile(r"#(\w+).*?", flags=re.IGNORECASE | re.UNICODE)
    parsed_content_with_hashtags = pattern.sub(create_hashtag_url, content)
    pattern = re.compile(r"@(\w+).*?", flags=re.IGNORECASE | re.UNICODE)
    parsed_content_complete = pattern.sub(create_mention_url, parsed_content_with_hashtags)

    return parsed_content_complete


def create_hashtag_url(matchobj):
    """
    Receives a matched object with a hashtag in the .group(0) and returns the url from it.

    @param matchobj: MatchObj - given through pattern.sub.

    @return hashtag between <a></a> HTML tags
    """
    url = reverse('posts:hashtags', kwargs={'hashtag_name': matchobj.group(0).lstrip('#')})
    return '<a class="hashtag" href="' + url + '">' + matchobj.group(0) + '</a>'


def create_mention_url(matchobj):
    """
    Receives a matched object with a mention in the .group(0) and returns the url from it.

    @param matchobj: MatchObj - given through pattern.sub.

    @return mention between <a></a> HTML tags
    """
    url = reverse('users:profile_username', kwargs={'username': matchobj.group(0).lstrip('@')})
    return '<a class="mention" href="' + url + '">' + matchobj.group(0) + '</a>'
