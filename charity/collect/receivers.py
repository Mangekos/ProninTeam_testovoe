from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(post_save, sender=None)
def delete_cache_on_save(sender, instance, **kwargs):
    cache.delete(settings.COLLECT)
    cache.delete(settings.PAYMENT)


@receiver(post_delete, sender=None)
def delete_cache_on_delete(sender, instance, **kwargs):
    cache.delete(settings.COLLECT)
    cache.delete(settings.PAYMENT)
