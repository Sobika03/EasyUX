import random
from django.core.management.base import BaseCommand
from faker import Faker
from openui.models import Person  # Adjust if model path is different

class Command(BaseCommand):
    help = "Seed Person table with dummy data"

    def add_arguments(self, parser):
        parser.add_argument('--records', type=int, default=49000, help='Number of dummy records to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['records']
        batch_size = 49000
        objects = []

        self.stdout.write(self.style.SUCCESS(f"Creating {total} dummy records..."))

        for i in range(total):
            person = Person(
                name=fake.name(),
                age=random.randint(18, 80),
                email=fake.email(),
                phone=fake.phone_number(),
                gender=random.choice(['Male', 'Female', 'Other'])
            )
            objects.append(person)

            if len(objects) >= batch_size:
                Person.objects.bulk_create(objects)
                objects = []

        if objects:
            Person.objects.bulk_create(objects)

        self.stdout.write(self.style.SUCCESS("Dummy data creation complete!"))
