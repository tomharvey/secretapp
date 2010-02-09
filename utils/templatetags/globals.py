from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.inclusion_tag('templatetags/forms/form.html')
def form(form):
    """
    Shortcut to initialize a standard form.
    Implements Meta data stored on form instance, applies in forms.py
    
    Template Usage:
        {% form form %}
    
    Example form use:
        class Meta:
            url = 'some/url/to/'
            method = 'GET'
    """
    print dir(form)
    return { 'form': form }


@register.inclusion_tag('templatetags/forms/field.html')
def field(field, classes=None):
    """
    Shortcut for using a standard field
    
    Template Usage:
        {% field form.title 'left short' %}
    
    The 'left short' are classes which you want to apply to
    the containing div class
    """
    print dir(field)
    return { 'field': field, 'classes': classes }


@register.inclusion_tag('templatetags/forms/endform.html')
def endform(text=_('Submit'), classes=None):
    """
    Shortcut to close a form
    
    Template Usage:
        {% endform _('Go') 'right small' %}
    
    The 'right small' are classes which you want to apply to
    the containing div class
    
    The _('Go') is the translated action word you
    want to appear in the button
    """
    return { 'text': text, 'classes': classes }