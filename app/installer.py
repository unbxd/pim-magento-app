import logging
# from PAS.models import AppCred, AppUser, PimProp, App


logger = logging.getLogger("shopify_catalog.helpers")

CUSTOM_APP_NAME = "custom"


class Installer(object):

    def __init__(self):
        # TODO USE PAS-SDK
        # self.app_credentials = AppCred.get_credentials_by_app(app=CUSTOM_APP_NAME)
        self.api = None
        self.session = None

    def api_client(self, shop):
        pass

    def authorize_redirect(self, shop):
        pass

    def fetch_token(self, install_response):
        pass

    def uninstall(self, account):
        pass

    def install(self, app_data):

        # pass
        return {}
