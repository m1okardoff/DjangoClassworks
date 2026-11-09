from django import template

register = template.Library()


@register.filter
def uk_pluralize(value, forms):
    """
    forms: однина, 2-4, 5-0
    Наприклад: картка, картки, карток
    """
    try:
        n = abs(int(value))
    except (ValueError, TypeError):
        return ''

    forms = forms.split(',')

    if len(forms) != 3:
        return ''

    if 11 <= n % 100 <= 14:
        return forms[2]

    if n % 10 == 1:
        return forms[0]

    if 2 <= n % 10 <= 4:
        return forms[1]

    return forms[2]
