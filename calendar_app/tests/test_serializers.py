from django.test import TestCase

from calendar_app.models import Day, Event, Info
from calendar_app.serializers import DaySerializer, EventSerializer, InfoSerializer


class CalendarSerializerTestCase(TestCase):
    def test_day(self):
        day_1 = Day.objects.create(date='2020-01-01', topic='Day1')
        day_2 = Day.objects.create(date='2020-01-02', topic='Day2')
        day_3 = Day.objects.create(date='2020-01-03', topic='Day3')
        data = DaySerializer([day_1, day_2, day_3], many=True).data
        expected_data = [
            {
                'id': day_1.id,
                'date': '2020-01-01',
                'topic': 'Day1',
                'event': data[0]['event'],
            },
            {
                'id': day_2.id,
                'date': '2020-01-02',
                'topic': 'Day2',
                'event': data[1]['event'],

            },
            {
                'id': day_3.id,
                'date': '2020-01-03',
                'topic': 'Day3',
                'event': data[2]['event'],
            },
        ]
        self.assertEqual(expected_data, data)

    def test_event(self):
        event_1 = Event.objects.create(description='2020', time='00:00:00')
        event_2 = Event.objects.create(description='2021', time='00:00:00')
        event_3 = Event.objects.create(description='2022', time='00:00:00')
        data = EventSerializer([event_1, event_2, event_3], many=True).data
        expected_data = [
            {
                'id': event_1.id,
                'description': '2020',
                'day': data[0]['day'],
                'event_info': data[0]['event_info'],
                'time': event_1.time,
            },
            {
                'id': event_2.id,
                'description': '2021',
                'day': data[1]['day'],
                'event_info': data[1]['event_info'],
                'time': event_2.time,
            },
            {
                'id': event_3.id,
                'description': '2022',
                'day': data[2]['day'],
                'event_info': data[2]['event_info'],
                'time': event_3.time,
            },
        ]
        self.assertEqual(expected_data, data)

    def test_info(self):
        info_1 = Info.objects.create(topic='Day1', color='#FF0000')
        info_2 = Info.objects.create(topic='Day2', color='#FF0001')
        info_3 = Info.objects.create(topic='Day3', color='#FF0002')
        data = InfoSerializer([info_1, info_2, info_3], many=True).data
        expected_data = [
            {
                'id': info_1.id,
                'color': '#FF0000',
                'topic': 'Day1',
            },
            {
                'id': info_2.id,
                'color': '#FF0001',
                'topic': 'Day2',
            },
            {
                'id': info_3.id,
                'color': '#FF0002',
                'topic': 'Day3',
            },
        ]
        self.assertEqual(expected_data, data)
