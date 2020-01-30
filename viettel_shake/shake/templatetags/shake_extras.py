from django import template

register = template.Library()


@register.filter
def phone_censor(value):
    """Censor phone number"""
    phone = str(value)
    prefix = phone[:3]
    postfix = phone[-2:]
    censor = '{}*****{}'.format(prefix, postfix)
    return censor
