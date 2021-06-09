from django.conf import settings

def get_pim_app_domain():
    return getattr(settings, "PIM_APP_BASE_URL")

def get_pas_domain():
    return getattr(settings, "PAS_URL")

def get_pim_domain():
    return getattr(settings, "PIM_BASE_URL")
