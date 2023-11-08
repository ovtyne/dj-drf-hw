from rest_framework.serializers import ValidationError


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value is None:
            return

        if 'youtube.com' not in value:
            raise ValidationError('Video is not ok')


