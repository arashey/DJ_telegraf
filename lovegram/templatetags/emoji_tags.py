
from django import template
import emoji

register = template.Library()

@register.filter
def emoji_filter(value):
    return emoji.emojize(value)

