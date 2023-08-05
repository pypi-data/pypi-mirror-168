
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


def setup_settings(settings, is_prod, **kwargs):

    if 'solo' not in settings['INSTALLED_APPS']:
        settings['INSTALLED_APPS'] += ['solo']

    for template in settings['TEMPLATES']:
        template['OPTIONS']['context_processors'].append(
            'exchange.context_processors.currencies')


class ExchangeAppConfig(AppConfig):

    name = 'exchange'
    verbose_name = _('Exchange')


default_app_config = 'exchange.ExchangeAppConfig'
