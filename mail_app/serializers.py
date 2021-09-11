from rest_framework import serializers

from .models import Letter, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file', 'letter')


class LetterSerializer(serializers.ModelSerializer):
    letter = AttachmentSerializer(many=True)
    date_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Letter
        fields = ('id', 'mailer', 'topic', 'text', 'date_time', 'letter')
