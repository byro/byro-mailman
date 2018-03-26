from urllib.parse import urljoin

import requests
from django.db import models
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
        return urljoin(MailmanConfiguration.get_solo().url, self.name)


class MailingListEntry(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(to='members.Member', on_delete=models.CASCADE, related_name='mailinglists')
    mailing_list = models.ForeignKey(to=MailingList, on_delete=models.CASCADE, related_name='subscribers')
