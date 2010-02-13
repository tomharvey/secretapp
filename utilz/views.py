from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from secret.models import Secret
from discussion.models import Discussion
from shortcuts import context_response


def random_secret(request):
    " Redirects you to a random secret "
    import random
    # TODO: cache this
    ids = Secret.viewable.values_list('id', flat=True)
    choice = random.choice(ids)
    return HttpResponseRedirect(Secret.objects.get(pk=choice).get_absolute_url())


def home(request):
    " Landing page to site. Much more to come... "
    # TODO: cache this and randomize
    context = {
        'secrets': Secret.viewable.all().order_by('-created_at'),
        'discussions': Discussion.viewable.all().order_by('-created_at'),
    }
    return context_response(request, 'layout/base.html', context)


def render(request, template):
    " Displays any misc pages "
    try:
        return context_response(request, 'render/%s.html' % template, {})
    except:
        raise Http404
    