"""@package docstring
Extra template functions

@author 7Pros
@copyright
"""
from django import template
from django.core.urlresolvers import reverse
import re
register = template.Library()

@register.filter
@stringfilter
def parser(content):


def createHashtagURL(matchobj):
    url = reverse()
    return '<a class="hashtag" href="'+
