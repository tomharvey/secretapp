from django.core.urlresolvers import reverse
from django.db import models

from perm.models import UserContent
from discussion.models import Discussion
from secret.models import Secret


class AbstractComment(UserContent):
    """ Helper abstract model. Pretty useless now. May add more later. """
    text = models.TextField()
    
    # see perm.models for details
    edit_permission = 'Keeper'
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return u"%s" % self.pk


class SecretComment(AbstractComment):
    """ A comment on a secret. Could be assosiciated with a discussion. """
    secret      = models.ForeignKey(Secret)

    def get_delete_url(self):
        return reverse('delete_secret_comment', kwargs={'pk': self.pk})


class DiscussionComment(AbstractComment):
    """ A comment on a discussion. Could have secrets associated with it. """
    discussion  = models.ForeignKey(Discussion)
    secrets     = models.ManyToManyField(Secret, through="Proposal")
    
    def viewable_secrets(self):
        return [p.secret for p in Proposal.viewable.filter(discussion_comment=self).select_related()]
    
    def get_delete_url(self):
        return reverse('delete_discussion_comment', kwargs={'pk': self.pk})

class ProposalManager(models.Manager):
    def get_query_set(self):
        return super(ProposalManager, self).get_query_set() \
            .filter(discussion_comment__deleted=False, \
                                secret__deleted=False)

class Proposal(models.Model):
    """ When you suggest a secret in a discussion """
    discussion_comment = models.ForeignKey(DiscussionComment)
    secret      = models.ForeignKey(Secret)
    
    viewable    = ProposalManager()
    objects     = models.Manager() 

class ProposalComment(AbstractComment):
    """ A comment on a Proposal. """
    proposal        = models.ForeignKey(Proposal)

class ProposalEndorsement(UserContent):
    """ An endorsment on a secret proposal """
    proposal        = models.ForeignKey(Proposal)
        
