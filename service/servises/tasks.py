import datetime
from celery import shared_task
from django.db import transaction
from django.db.models import F
from celery_singleton import Singleton


@shared_task(base=Singleton)
def set_price(subscription_id: int):
    from .models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotetad_price=F('service__full_price') -
            F('service__full_price') * F('plan__discount_percent') / 100.00
        ).first()
        subscription.price = subscription.anntated_price
        subscription.save()


@shared_task(base=Singleton)
def set_comment(subscription_id: int):
    from .models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)
        subscription.comment = str(datetime.datetime.now())
        subscription.save()