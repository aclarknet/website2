from django.core.management.base import BaseCommand
from sphinxcontrib.websupport import WebSupport


class Command(BaseCommand):
    def handle(self, *args, **options):
        support = WebSupport(srcdir="db/doc/", builddir="db/doc/_websupport")
        support.build()
