from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from clients.models import Client
from django.conf import settings
from servises.models import Subscription
from servises.serializers import SubscriptionSerializer
from django.core.cache import cache


class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related('client', 'client__user') достает ненужные поля
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name', 'user__email'))
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        # не рекомендуется (фактически, чисто в учебных целях)
        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            # кладем в кэш на 60 секунд
            cache.set(settings.PRICE_CACHE_NAME, total_price, 3600)
        response_data = {
            'result': response.data,
            "total_amount": total_price
        }
        response.data = response_data
        return response
