from django.utils import translation


class TranslatedField(object):
    def __init__(self, en_field, de_field):
        self.en_field = en_field
        self.de_field = de_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'de':
            return getattr(instance, self.de_field)
        else:
            return getattr(instance, self.en_field)
