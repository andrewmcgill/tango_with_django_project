from django import template
from rango.models import Category

register = template.Library()

# refers to categories.html
# dict from get_category_list passed to template
# -> which renders using this "context" dict
# can then be injected into the template which initially called the template tag
@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),'current_category':current_category}
