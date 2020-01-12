from django import forms
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View

from byro.members.models import Member
from byro.office.views.members import MemberView

from .models import MailingList


class MailmanMemberForm(forms.Form):
    mailinglist = forms.ChoiceField()

    def __init__(self, *args, member, **kwargs):
        super().__init__(*args, **kwargs)
        names = MailingList.objects.exclude(subscribers__member=member).values_list('name', flat=True)
        self.fields['mailinglist'].choices = [(n, n) for n in names]


class MemberLists(MemberView, TemplateView):
    template_name = 'byro_mailman/member_lists.html'

    @property
    def object(self):
        return self.get_object()

    def get_object(self):
        return Member.all_objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        member = self.get_object()
        ctx['lists'] = member.mailinglists.all()
        ctx['form'] = MailmanMemberForm(member=member)
        return ctx


class MemberAdd(MemberLists):

    def post(self, request, pk):
        member = self.get_object()
        form = MailmanMemberForm(request.POST, member=member)
        if not form.is_valid():
            messages.error(request, _('Mailing list not found.'))
            return redirect(reverse('plugins:byro_mailman:members.mailman.lists', kwargs={'pk': self.kwargs['pk']}))
        try:
            mailing_list = MailingList.objects.filter(name=form.cleaned_data['mailinglist']).first()
            mailing_list.add(self.get_object())
            messages.success(request, _('Member added to mailing list.'))
        except Exception as e:
            messages.error(request, _('Error adding the member to the mailing list: ') + str(e))
        return redirect(reverse('plugins:byro_mailman:members.mailman.lists', kwargs={'pk': self.kwargs['pk']}))


class MemberRemove(MemberLists):

    def get(self, request, pk, list_id):
        mailing_list = MailingList.objects.filter(pk=list_id).first()
        if not mailing_list:
            messages.error(request, _('Mailing list not found.'))
            return redirect(reverse('plugins:byro_mailman:members.mailman.lists', kwargs={'pk': self.kwargs['pk']}))
        try:
            mailing_list.remove(self.get_object())
            messages.success(request, _('Member removed from mailing list.'))
        except Exception as e:
            messages.error(request, _('Error removing the member from the mailing list: ') + str(e))
        return redirect(reverse('plugins:byro_mailman:members.mailman.lists', kwargs={'pk': self.kwargs['pk']}))


class MailmanSync(View):

    def dispatch(self, *args, **kwargs):
        qs = MailingList.objects.all()
        if 'list_id' in self.request.GET:
            qs = qs.filter(name=self.request.GET.get('list_id'))
        total = [0, 0]
        for ml in qs:
            add, delete = ml.sync()
            total[0] += add
            total[1] += delete

        stats = _('There were {} additions and {} deletions in total.').format(*total)
        if 'list_id' in self.request.GET:
            messages.success(self.request, _('The mailing list has been synced. ') + stats)
        else:
            messages.success(self.request, _('The mailing lists have been synced. ') + stats)
        return redirect(reverse('plugins:byro_mailman:lists.dashboard'))


class MailmanView(TemplateView):
    template_name = 'byro_mailman/mailman.html'

    @property
    def formset(self):
        return forms.modelformset_factory(
            model=MailingList,
            fields=['id', 'name', 'add_when_joining', 'remove_when_leaving'],
            can_delete=True, extra=0,
        )(
            self.request.POST if self.request.method == 'POST' else None,
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['lists'] = MailingList.objects.all()
        ctx['formset'] = self.formset
        return ctx

    def post(self, request, *args, **kwargs):
        formset = self.formset
        if not formset.is_valid():
            messages.error(self.request, _('Invalid data.'))
            return redirect(reverse('plugins:byro_mailman:lists.dashboard'))

        for form in formset.initial_forms:
            if form in formset.deleted_forms:
                if not form.instance.pk:
                    continue
                form.instance.delete()
                form.instance.pk = None
            elif form.has_changed():
                form.save()

        for form in self.formset.extra_forms:
            if form.is_valid():
                if form.instance.name:
                    form.save()

        messages.success(request, _('Successfully saved.'))
        return redirect(reverse('plugins:byro_mailman:lists.dashboard'))
