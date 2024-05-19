from django.db.models import Sum
from rest_framework import serializers

from collect.models import Collect, Payment


class CollectSerializer(serializers.ModelSerializer):
    collection_tape = serializers.SerializerMethodField()
    collected = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = (
            "id",
            "name",
            "first_name",
            "last_name",
            "occasion",
            "description",
            "target",
            "image",
            "collection_period",
            "collection_tape",
            "collected",
            "author",
        )

    def get_collection_tape(self, obj):
        return PaymentSerializer(obj.payments.filter(), many=True).data

    def get_collected(self, obj):
        sum_payment = obj.payments.aggregate(total=Sum("sum_payment"))["total"]
        return sum_payment

    def get_author(self, obj):
        return obj.author.first_name


class PaymentSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(
        format="%H:%M %d %m %Y", read_only=True
    )
    collect = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "type_payment",
            "sum_payment",
            "first_name",
            "last_name",
            "email",
            "comment",
            "collect",
            "pub_date",
        )

    def get_sum_payment(self, obj):
        if obj.is_show is True:
            return obj.sum_payment

    def get_collect(self, obj):
        return obj.collect.name

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_show is False:
            representation["sum_payment"] = None
        return representation
