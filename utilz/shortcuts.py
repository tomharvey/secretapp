from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def context_response(request, template, context, *args, **kwargs):
    """
    helper for
        http://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(template, context, *args, **kwargs)


def redirect_back(request):
    """
    Returns you back 
    """
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('home'))


def login_required(func):
    """
    http://docs.djangoproject.com/en/dev/topics/auth/#the-login-required-decorator

    But uses reverse('login') and automatically redirects back to incoming page.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            request.session['next'] = request.path
            return HttpResponseRedirect(reverse('socialauth_login_page'))
        return func(request, *args, **kwargs)
    return wrapper


def select_related_object_or_404(select_related, Model, *args, **kwargs):
    "Wanted to add select_related functionality to django.shortcuts.get_object_or_404"
    try:
        if select_related:
            return Model.objects.select_related().get(*args, **kwargs)
        else:
            return Model.objects.get(*args, **kwargs)
    except Model.DoesNotExist:
        raise Http404


def get_editable_or_raise(Model, user, select_related=True, *args, **kwargs):
    "similar to django.shortcuts.get_object_or_404 with permission checks"
    if not isinstance(user, (User, AnonymousUser)):
        raise TypeError, "Please supply a user as the second argument"
    instance = select_related_object_or_404(select_related, Model, *args, **kwargs)
    if instance.user_can_edit(user):
        return instance
    else:
        raise PermissionDenied


def get_viewable_or_raise(Model, user, select_related=True, *args, **kwargs):
    "similar to above but does viewablility check"
    if not isinstance(user, (User, AnonymousUser)):
        raise TypeError, "Please supply a user as the second argument"
    instance = select_related_object_or_404(select_related, Model, *args, **kwargs)
    if instance.user_can_view(user):
        return instance
    else:
        raise Http404




