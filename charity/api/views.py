from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from collect.models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from .tasks import send_email_task


@extend_schema(
    tags=["Сбор средств"],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    description=(
        "Авторизованные пользователи могут создавать, "
        "все пользователи могут видеть"
    ),
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список сборов",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о сборе",
    ),
    create=extend_schema(
        summary="Создать сбор",
    ),
    update=extend_schema(
        summary="Обновить сбор",
    ),
    partial_update=extend_schema(
        summary="Частичное обновление сбора",
    ),
    destroy=extend_schema(
        summary="Удалить сбор",
    ),
)
class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated],
        "partial_update": [IsAuthenticated],
        "destroy": [IsAuthenticated],
        "list": [AllowAny],
    }

    def list(self, request, *args, **kwargs):
        collect_cash = cache.get(settings.COLLECT)
        if collect_cash:
            queryset = collect_cash
        else:
            queryset = self.filter_queryset(self.get_queryset())
            cache.set(settings.COLLECT, queryset, 30)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        collect = get_object_or_404(Collect, id=serializer.data["id"])
        subject = "Сбор успешно создан!"
        message = (
            f"Уважаемый {collect.first_name} {collect.last_name}! \n"
            f"Ваше сбор {collect.name} был успешно создан. "
            f"Цель сбора: {collect.occasion}, нужная сумма {collect.target}."
        )
        send_email_task(subject, message, collect.author.email)

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[
                    self.action
                ]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]


@extend_schema(
    tags=["Сделание пожертвование"],
    methods=["GET", "POST"],
    description="Все пользователи могут видеть и создать пожертвования",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список пожертвований",
    ),
    create=extend_schema(
        summary="Сделать пожертвование",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о пожертвовании",
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        collect_id = self.kwargs.get("collect_id")
        new_queryset = get_object_or_404(Collect, id=collect_id)
        return new_queryset.payments.all()

    def perform_create(self, serializer):
        collect_id = self.kwargs.get("collect_id")
        collect = get_object_or_404(Collect, id=collect_id)
        serializer.save(collect=collect)
        payment = get_object_or_404(Payment, id=serializer.data["id"])
        subject = "Спасибо за пожертвование!"
        message = (
            f"Уважаемый {payment.first_name} {payment.last_name}! \n"
            f"Ваше пожертвование {payment.sum_payment} успешно отправлено "
            f"на сбор {payment.collect}"
        )
        send_email_task(subject, message, payment.email)


@extend_schema(
    tags=["Пользователь"],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    description="Авторизованный пользователь",
)
@extend_schema_view(
    list=extend_schema(
        summary="Получить список пользователей",
    ),
    retrieve=extend_schema(
        summary="Детальная информация о пользователе",
    ),
    create=extend_schema(
        summary="Создать пользователя",
    ),
    update=extend_schema(
        summary="Обновить пользователя",
    ),
    partial_update=extend_schema(
        summary="Частичное обновление пользователя",
    ),
    destroy=extend_schema(
        summary="Удалить пользователя",
    ),
    me=extend_schema(
        summary="Мой профиль",
    ),
    activation=extend_schema(
        summary="Активация аккаунта",
    ),
    resend_activation=extend_schema(
        summary="Отправить повторное письмо активации",
    ),
    set_password=extend_schema(
        summary="Сменить пароль",
    ),
    reset_password=extend_schema(
        summary="Сбросить пароль",
    ),
)
class CustomUserViewSet(UserViewSet):
    pass
