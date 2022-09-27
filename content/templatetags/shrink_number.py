from django import template

register = template.Library()

@register.filter(name='shrink_number')
def shrink_number(value):
    
    value_int = int(value)

    if value_int > 1000000000:
        value = "%.2f%s" % (value_int/1000000000.00, ' B')
        return value

    if value_int > 1000000:
        value = "%.2f%s" % (value_int/1000000.00, ' M')
        return value

    if value_int > 1000:
        value = "%.2f%s" % (value_int/1000.00, ' K')
        return value
