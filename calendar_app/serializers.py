from rest_framework import serializers
from .models import Day, Event, Info


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id', 'color', 'topic')


class EventSerializer(serializers.ModelSerializer):
    event_info = InfoSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'day', 'description', 'time', 'event_info')


class DaySerializer(serializers.ModelSerializer):
    event = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Day
        fields = ('id', 'date', 'topic', 'event')
