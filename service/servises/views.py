from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from clients.models import Client
from servises.models import Subscription
from servises.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related('client', 'client__user') достает ненужные поля
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name', 'user__email'))
    )
    serializer_class = SubscriptionSerializer
