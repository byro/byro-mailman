import json
from urllib.parse import urljoin

import requests
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class MailmanConfiguration(SingletonModel):

    url = models.CharField(
        null=True, blank=True,
        max_length=300,
        verbose_name=_('Mailman API URL'),
        help_text=_('e.g. https://foo.bar.de/api')
    )
    user = models.CharField(
        null=True, blank=True,
        max_length=300,
        verbose_name=_('Mailman API Username'),
    )
    password = models.CharField(
        null=True, blank=True,
        max_length=300,
        verbose_name=_('Mailman API Password'),
    )


class MailingList(models.Model):
    name = models.CharField(max_length=100)
    add_when_joining = models.BooleanField(
        default=True,
        verbose_name=_('Add new members automatically'),
    )
    remove_when_leaving = models.BooleanField(
        default=True,
        verbose_name=_('Remove leaving members automatically'),
    )

    @property
    def url(self):
        base = MailmanConfiguration.get_solo().url
        if not base.endswith('/'):
            base += '/'
        return base + self.name

    @transaction.atomic
    def sync(self):
        config = MailmanConfiguration.get_solo()
        response = requests.get(self.url, auth=(config.user, config.password))
        if not response.status_code == 200:
            raise Exception(response.content.decode())

        from byro.members.models import Member
        new_addresses = set(json.loads(response.content.decode()))
        old_addresses = set(self.subscribers.all().values_list('email', flat=True))

        delete = old_addresses - new_addresses
        add = new_addresses - old_addresses
        self.subscribers.filter(member__email__in=delete).delete()
        for email in add:
            MailingListEntry.objects.create(mailing_list=self, member=Member.objects.filter(email=email).first(), email=email)
        return (len(add), len(delete))


class MailingListEntry(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(
        to='members.Member',
        on_delete=models.CASCADE,
        related_name='mailinglists',
        null=True, blank=True,
    )
    mailing_list = models.ForeignKey(
        to=MailingList,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )
    email = models.EmailField(
        max_length=200,
        verbose_name=_('E-Mail'),
        null=True, blank=True,
    )