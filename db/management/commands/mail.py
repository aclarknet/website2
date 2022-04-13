from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth.models import User
from db.config import MAIL_FROM
from django.utils import timezone
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.filter(profile__mail=True):
            if user.email:
                hour = random.choice(range(24))
                now = timezone.now().strftime("%H")
                if hour == int(now):
                    MAIL_TO = user.email
                    send_mail(
                        "Timesheet reminder from ACLARKNET",
                        "Please enter time weekly. Thanks. Pre'ciate it.",
                        MAIL_FROM,
                        [MAIL_TO],
                        fail_silently=False,
                    )
