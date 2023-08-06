
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


def setup_settings(settings, is_prod, **kwargs):

    settings['MIDDLEWARE'] += ['wishlist.middleware.WishListMiddleware']


class WishListAppConfig(AppConfig):

    name = 'wishlist'
    verbose_name = _('WishList')


default_app_config = 'wishlist.WishListAppConfig'
