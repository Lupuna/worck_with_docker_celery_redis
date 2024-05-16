from rest_framework.viewsets import ReadOnlyModelViewSet
from servises.models import Subscription
from servises.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

