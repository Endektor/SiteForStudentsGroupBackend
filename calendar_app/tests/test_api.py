# from ..models import Day, Event, Info
# from ..serializers import DaySerializer, EventSerializer, InfoSerializer
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
#
# class CalendarApiTestCase(APITestCase):
#     def test_days(self):
#         day_1 = Day.objects.create(date='2020-09-01', topic='Day1')
#         day_2 = Day.objects.create(date='2020-09-02', topic='Day2')
#         day_3 = Day.objects.create(date='2020-09-03', topic='Day3')
#         url = '/api/calendar/days/202009'
#         response = self.client.get(url)
#         expected_data = DaySerializer([day_1, day_2, day_3], many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(expected_data, response.data)
#
#     def test_info(self):
#         info_1 = Info.objects.create(topic='Day1', color='#FF0000')
#         info_2 = Info.objects.create(topic='Day2', color='#FF0001')
#         info_3 = Info.objects.create(topic='Day3', color='#FF0002')
#         url = '/api/calendar/info/'
#         response = self.client.get(url)
#         expected_data = InfoSerializer([info_1, info_2, info_3], many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(expected_data, response.data)
