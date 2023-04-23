from django import template


register = template.Library()

censored_words = ['редиска', 'редиски']


@register.filter()
def censor(value):
    for w in censored_words:
        asterisk = '*' * len(w)
        value = value.replace(w, asterisk)
        value = value.replace(w.title(), asterisk)
    return value
