import re

from rest_framework.serializers import ValidationError


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('https://youtube.com')
        tnp_val = dict(value).get(self.field)
        if not bool(reg.match(tnp_val)):
            raise ValidationError('Video is not ok')
