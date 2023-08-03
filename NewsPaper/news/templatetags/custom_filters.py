from django import template

register = template.Library()


@register.filter()
def cencor(value):
    bad_words = ['article', 'news']

    if not isinstance(value, str):
        raise TypeError(f"Unresolved type {type(value)} expected type 'str'")

    for word in value.split():
        if word.lower() in bad_words:
            value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
    return value
