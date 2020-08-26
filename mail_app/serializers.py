from rest_framework import serializers
from .models import Letter


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ('id', 'mailer', 'topic', 'text')
