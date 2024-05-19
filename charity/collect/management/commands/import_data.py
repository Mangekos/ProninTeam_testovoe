import csv
import os

from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from collect.models import Collect, Payment, User


class Command(BaseCommand):
    """Команда для импорта данных"""

    def import_collect_data(csv_file_name):
        """Импорт сборов"""
        csv_file_path = os.path.join(
            os.path.dirname(__file__), "data", csv_file_name
        )
        with open(csv_file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row["name"]
                author = User.objects.get(username=row["author"])
                first_name = row["first_name"]
                last_name = row["last_name"]
                occasion = row["occasion"]
                description = row["description"]
                target = int(row["target"]) if row["target"] else 0
                image_file = row["image"]
                collection_period = row["collection_period"]

                collect = Collect(
                    name=name,
                    author=author,
                    first_name=first_name,
                    last_name=last_name,
                    occasion=occasion,
                    description=description,
                    target=target,
                    collection_period=collection_period,
                )

                if image_file:
                    image_file_path = os.path.join(
                        os.path.dirname(__file__), "data", image_file
                    )
                    with open(image_file_path, "rb") as image:
                        content = ContentFile(image.read())
                        collect.image.save(image_file, content)

                collect.save()

    def import_payment_data(csv_file_name):
        """Импорт пожертвований"""
        csv_file_path = os.path.join(
            os.path.dirname(__file__), "data", csv_file_name
        )
        with open(csv_file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                type_payment = row["type_payment"]
                sum_payment = int(row["sum_payment"])
                first_name = row["first_name"]
                last_name = row["last_name"]
                email = row["email"]
                comment = row["comment"]
                collect_name = row["collect"]
                collect = Collect.objects.get(name=collect_name)
                pub_date = row["pub_date"]
                is_show = row["is_show"]

                payment = Payment(
                    type_payment=type_payment,
                    sum_payment=sum_payment,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    comment=comment,
                    collect=collect,
                    pub_date=pub_date,
                    is_show=is_show,
                )
                payment.save()

    def handle(self, *args, **options):
        self.import_collect_data("collect.csv")
        self.import_payment_data("payment.csv")
