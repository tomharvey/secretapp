from django import forms
from django.core.urlresolvers import reverse
from perm.forms import UserContentForm
from models import *


class SecretCommentForm(UserContentForm):
    class Meta:
        model = SecretComment
        fields = ('text',)
    
    def set_url(secret, discussion=None):
        if discussion:
            self.Meta.url = reverse('create_discussion_secret_comment', kwargs={'discussion_id': discussion.id, 'secret_id': secret.id })
        else:
            self.Meta.url = reverse('create_secret_comment', kwargs={'secret_id': secret.id })
        return self

class DiscussionCommentForm(UserContentForm):
    secrets = forms.CharField(required=False, help_text="Comma seperated list of secret ids. e.g. 1,5,8,9 ")
    
    class Meta:
        model = DiscussionComment
        fields = ('text',)
    
    def set_url(self, discussion):
        self.Meta.url = reverse('create_discussion_comment', kwargs={'discussion_id': discussion.id })
        return self
    
    def save(self, request, discussion):
        instance = super(DiscussionCommentForm, self).save(request, commit=False)
        instance.discussion = discussion
        instance.save()
        lst = []
        for i in self.cleaned_data['secrets'].split(','):
            try:
                x = int(i)
            except:
                pass
            else:
                lst.append(x)
        secrets = Secret.viewable.filter(pk__in=lst)
        for s in secrets:
            p = Proposal()
            p.secret = s
            p.discussion_comment = instance
            p.save()
        return instance

