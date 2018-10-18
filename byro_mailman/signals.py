from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from byro.members.signals import new_member
from byro.office.signals import member_view, nav_event

from .models import MailingList


@receiver(member_view)
def mailman_member_view(sender, signal, **kwargs):
    member = sender
    count = MailingList.objects.filter(subscribers__member=member).count()
    return {
        'label': _('Mailing lists ({count})').format(count=count),
        'url': reverse('plugins:byro_mailman:members.mailman.lists', kwargs={'pk': member.pk}),
        'url_name': 'plugins:byro_mailman:members.mailman.lists',
    }


@receiver(nav_event)
def mailman_sidebar(sender, **kwargs):
    request = sender
    if hasattr(request, 'user') and not request.user.is_anonymous:
        return {
            'icon': 'envelope-o',
            'label': _('Mailing lists'),
            'url': reverse('plugins:byro_mailman:lists.dashboard'),
            'active': 'byro_mailman' in request.resolver_match.namespace and 'member' not in request.resolver_match.url_name,
        }


@receiver(new_member)
def add_new_member(sender, **kwargs):
    member = sender
    if member.email:
        for ml in MailingList.objects.filter(add_when_joining=True):
            ml.add(member)
