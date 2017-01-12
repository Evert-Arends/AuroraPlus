import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class CheckboxHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_checkbox_value(request):
        checkbox_value = 'active_monitoring' in request.POST
        return checkbox_value
