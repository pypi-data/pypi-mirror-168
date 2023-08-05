
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManufacturersAppConfig(AppConfig):

    name = 'manufacturers'
    verbose_name = _('Manufacturers')


default_app_config = 'manufacturers.ManufacturersAppConfig'
