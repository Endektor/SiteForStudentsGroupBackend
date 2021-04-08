from rest_framework import serializers
from .models import Day, Event, Info


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id', 'color', 'topic')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'day', 'description', 'time', 'info')


class DaySerializer(serializers.ModelSerializer):
    day_event = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Day
        fields = ('id', 'date', 'topic', 'day_event')
