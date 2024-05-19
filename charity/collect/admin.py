from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Collect, Payment

User = get_user_model()


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
