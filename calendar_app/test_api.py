from custom_auth.test_api import CustomAuthApiTest
from rest_framework import status


class CalendarApiTest(CustomAuthApiTest):

    def test_api(self):
        self.user_create(username='name1', id=1)
        self.login(username='name1')
        self.group_create()
        self.day_create()
        self.info_create()
        self.event_create()

    def day_create(self):
        url = '/api/calendar/days/'
        response = self.client.post(url, {'date': '2020-02-20',
                                          'topic': 'day_test',
                                          'group': 'group_name'})
        expected_data = {'id': 1, 'date': '2020-02-20', 'topic': 'day_test', 'event': []}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)

    def info_create(self):
        url = '/api/calendar/infos/'
        response = self.client.post(url, {'topic': 'test_day',
                                          'color': '#FF0000',
                                          'group': 'group_name'})
        expected_data = {'id': 1, 'color': '#FF0000', 'topic': 'test_day'}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)

    def event_create(self):
        url = '/api/calendar/events/'
        response = self.client.post(url, {'description': 'test_description',
                                          'day': 1,
                                          'event_info': 1,
                                          'time': '12:34:56',
                                          'group': 'group_name'})
        expected_data = {'id': 1,
                         'day': 1,
                         'description': 'test_description',
                         'time': '12:34:56',
                         'event_info': 1}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)
