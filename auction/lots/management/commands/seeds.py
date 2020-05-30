import datetime
import json
import os
import random
from io import BytesIO

from PIL import Image
from django.core.management import BaseCommand
from django.conf import settings

from lots.models import Lot
from users.models import User

LOTS_DIR = os.path.join(
    settings.BASE_DIR,
    'lots',
    'management',
    'data',
    'lots'
)

IMG_DIR = os.path.join(
    settings.BASE_DIR,
    'lots',
    'management',
    'data',
    'images'

)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--truncate', help='Clear the database before loading',
            action='store_true'
        )

    def handle(self, *args, **options):
        if options['truncate']:
            Lot.objects.all().delete()

        user = User.objects.create(
            username='test_user',
            password='test',
        )
        for file, img in zip(os.listdir(LOTS_DIR), os.listdir(IMG_DIR)):
            image = Image.open(
                os.path.join(IMG_DIR, img)
            )
            image.thumbnail((100, 100), Image.ANTIALIAS)
            image.save(os.path.join(IMG_DIR, img), quality=60)

            with open(os.path.join(LOTS_DIR, file)) as f:
                data = json.load(f)
                lot = Lot.objects.create(
                    heading=data['heading'],
                    text_description=data['text'],
                    base_price=random.randint(1, 1000) * 10,
                    created_at=datetime.datetime.now(),
                    image=image,
                    author = user
                )

