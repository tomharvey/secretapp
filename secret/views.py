from django.http import HttpResponseRedirect, QueryDict
from discussion.models import Discussion
from secret.forms import SecretSearchForm
from utils.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise, login_required
from forms import *
from models import *


def search(request):
    # TODO: make solr call
    template = request.GET.get('template', 'list')
    
    # if has been requested
    if request.GET:
        form = SecretSearchForm(request.GET)
    # otherwise default settings
    else:
        form = SecretSearchForm({
            'page': 1
        })
    
    # get the results
    if form.is_valid():
        results = form.save()
    else:
        results = []

    return context_response(request, 'secret/search.html', {
                'form': form,
                'results': results,
                'template': template,
                
                # this may need to become a context_processor
                'template_types': SECRET_RENDER_TEMPLATES,
                
                # loose this later (keep for now - testing purposes)
                'secrets': Secret.viewable.all(),
            })


def view(request, pk):
    return context_response(request, 'secret/view.html', {
                'secret': get_viewable_or_raise(Secret, request.user, pk=pk),
            })

@login_required
def edit(request, pk=None, discussion_id=None):
    user = request.user
    # get object
    secret = get_editable_or_raise(Secret, user, pk=pk) if pk else Secret()
    
    if request.method == 'POST':
        form = SecretForm(request.POST, instance=secret)
        if form.is_valid():
            secret = form.save(request)
            # success and ajax
            if request.is_ajax():
                # if creating a secret as part of a discussion reply (need to return different template)
                if discussion_id:
                    return context_reponse(request, 'secret/snippets/comment.html', {'secret': secret })
                # otherwise creating it randomly somewhere else
                else:
                    return context_reponse(request, 'secret/snippets/list.html', {'secret': secret })
            # success redirect to instance page
            else:
                # if creating as part of a discussion, redirect back to discussion
                if discussion_id:
                    # this is a serious failure if this happeneds - but try best to recover
                    return HttpResponseRedirect(reverse('view_discussion', kwargs={'pk': discussion_id }))
                # otherwise send to new page
                else:
                    return HttpResponseRedirect(secret.get_absolute_url())
    else:
        form = SecretForm(instance=secret)
        
    # set the urlG
    form.set_url(secret=secret, discussion=discussion_id)
    
    context = {
        'form': form,
        'secret': secret,
    }
    # is ajax creating / editing / failure
    if request.is_ajax():
        return context_response(request, 'secret/ajax.html', context)
    # otherwise
    else:
        return context_response(request, 'secret/edit.html', context)



