import logging

from django.test import TestCase

from db.forms import ClientForm, InvoiceForm, ProjectForm, TaskForm, TimeForm
from db.models import Client, Invoice, Project, Task, Time

logger = logging.getLogger(__name__)


class FirstTestCase(TestCase):
    def setUp(self):
        self.client = Client(
            name="Rapidiously incubate optimal channels before pandemic web-readiness."
        )
        self.project = Project(
            name="Dramatically re-engineer user friendly benefits.", client=self.client
        )
        self.task = Task(
            name="Enthusiastically leverage existing emerging manufactured.",
            project=self.project,
            rate=150,
        )
        self.invoice = Invoice(
            subject="Dynamically redefine long-term high-impact infrastructures.",
            project=self.project,
        )
        self.time = Time(
            description="Conveniently strategize team building technologies.",
            invoice=self.invoice,
        )

    def test_client(self):
        self.assertEqual(
            self.client.name,
            "Rapidiously incubate optimal channels before pandemic web-readiness.",
        )

    def test_project(self):
        self.assertEqual(self.client, self.project.client)

    def test_task(self):
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.rate, 150)

    def test_invoice(self):
        self.assertEqual(self.invoice.project, self.project)

    def test_time(self):
        self.assertEqual(self.time.invoice, self.invoice)
