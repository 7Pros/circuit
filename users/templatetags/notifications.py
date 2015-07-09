"""@package posts.templatetags.parser
Extra template functions for posts.

@author 7Pros
@copyright
"""
from django import template
from users.models import Notification

register = template.Library()

@register.assignment_tag
def set_notifications_attributes(user):
    setattr(user, 'notifications', user.notification_set.all().order_by('-created_at')[:20])
    setattr(user, 'unseen_notifications', Notification.get_number_of_unseen_notifications(user=user))
    return user
