import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aurora.settings")
django.setup()


class CheckboxHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_checkbox_value(request):
        checkbox_value = str(request.POST.get('onoffswitch'))
        print checkbox_value
        return checkbox_value
