from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'byro_mailman'
    verbose_name = 'The byro Mailman plugin'

    class ByroPluginMeta:
        name = ugettext_lazy('The byro Mailman plugin')
        author = 'rixx'
        description = ugettext_lazy('Mailing list integration for byro')
        visible = True
        version = '1.0.1'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'byro_mailman.PluginApp'
