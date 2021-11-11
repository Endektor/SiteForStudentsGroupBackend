from django.apps import AppConfig


class CustomAuthAppConfig(AppConfig):
    name = 'custom_auth'

    def ready(self):
        from .serializers import DjoserUserSerializer
        import djoser.serializers as serializers

        serializers.UserCreateSerializer = DjoserUserSerializer
