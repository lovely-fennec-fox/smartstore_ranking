from django import template

register = template.Library()


@register.filter
def nth_keyword(keywords, num):

    try:
        return keywords[num-1]

    except:
        return ""


