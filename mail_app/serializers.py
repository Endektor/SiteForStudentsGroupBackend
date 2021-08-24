from rest_framework import serializers

from .models import Letter, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file', 'letter')


class LetterSerializer(serializers.ModelSerializer):
    letter = AttachmentSerializer(many=True)

    class Meta:
        model = Letter
        fields = ('id', 'mailer', 'topic', 'text', 'letter')
