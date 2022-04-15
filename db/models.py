from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager



class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    publish = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Client(BaseModel):
    tags = TaggableManager(blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField("Website", blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]

    company = models.ForeignKey(
        "Company", blank=True, null=True, on_delete=models.CASCADE
    )


class Contact(BaseModel):
    """
    Client, First Name, Last Name, Title, Email, Office Phone, Mobile Phone,
    Fax
    """

    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField("E-Mail Address", blank=True, null=True)
    mobile_phone = PhoneNumberField("Mobile Phone", blank=True, null=True)
    office_phone = PhoneNumberField("Office Phone", blank=True, null=True)
    phone = models.CharField(max_length=300, blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    uuid = models.UUIDField("UUID", max_length=300, default=uuid4)

    def __str__(self):
        if self.email and self.first_name and self.last_name:
            return " ".join([self.first_name, self.last_name, "<%s>" % self.email])
        elif self.first_name and self.last_name:
            return " ".join([self.first_name, self.last_name])
        elif self.first_name:
            return " ".join([self.first_name])
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Expense(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)

    def __str__(self):
        return "-".join([self._meta.verbose_name, str(self.pk)])


class Company(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField("Website", blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"


class Invoice(BaseModel):
    """
    Issue Date, Last Payment Date, Invoice ID, PO Number, Client, Subject,
    Invoice Amount, Paid Amount, Balance, Subtotal, Discount, Tax, Tax2,
    Currency, Currency Symbol
    """

    subject = models.CharField(max_length=300, blank=True, null=True)
    issue_date = models.DateField(
        "Issue Date", blank=True, default=timezone.now, null=True
    )
    due_date = models.DateField("Due", blank=True, null=True)
    last_payment_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(
        "Start Date", blank=True, default=timezone.now, null=True
    )
    end_date = models.DateField("End Date", blank=True, default=timezone.now, null=True)
    po_number = models.CharField("PO Number", max_length=300, blank=True, null=True)
    sa_number = models.CharField(
        "Subcontractor Agreement Number", max_length=300, blank=True, null=True
    )
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(
        "Invoice Amount", blank=True, null=True, max_digits=12, decimal_places=2
    )
    paid_amount = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    balance = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    subtotal = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    discount = models.IntegerField(blank=True, null=True)
    ein = models.IntegerField("EIN", blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True)
    tax2 = models.IntegerField(blank=True, null=True)
    project = models.ForeignKey(
        "Project", blank=True, null=True, on_delete=models.CASCADE
    )
    currency = models.CharField(
        default="United States Dollar - USD", max_length=300, blank=True, null=True
    )
    currency_symbol = models.CharField(
        default="$", max_length=300, blank=True, null=True
    )
    note = models.ManyToManyField("Note", blank=True)

    def __str__(self):
        if self.subject:
            return self.subject
        else:
            return "invoice-%s" % self.pk

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["subject"]

    doc_type = models.CharField(max_length=300, blank=True, null=True)
    gross = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    net = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    cost = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    hours = models.DecimalField(
        "Hours", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )
    company = models.ForeignKey(
        "Company", blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )


class Note(BaseModel):
    notes = models.ManyToManyField("Note", blank=True)
    html = models.BooleanField("HTML", default=False)
    pin = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Profile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    page_size = models.PositiveIntegerField(blank=True, null=True)
    rate = models.DecimalField(
        "Hourly Rate (United States Dollar - USD)",
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
    )
    unit = models.DecimalField(
        "Unit", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )
    avatar_url = models.URLField("Avatar URL", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)
    twitter_username = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    note = models.ManyToManyField("Note", blank=True)
    lounge_password = models.CharField(max_length=150, blank=True, null=True)
    lounge_username = models.CharField(max_length=150, blank=True, null=True)
    mail = models.BooleanField(default=False)
    dark = models.BooleanField(default=True)

    def __str__(self):
        return "-".join([self._meta.verbose_name, str(self.pk)])

    def is_staff(self):
        if self.user:
            if self.user.is_staff:
                return True


class Project(BaseModel):
    """
    Client, Project, Project Code, Start Date, End Date,
    Total Hours, Billable Hours, Billable Amount, Budget, Budget Spent,
    Budget Remaining, Total Costs, Team Costs, Expenses
    """

    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=300, blank=True, null=True)
    task = models.OneToOneField(
        "Task", blank=True, null=True, on_delete=models.SET_NULL
    )
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    code = models.IntegerField("Project Code", blank=True, null=True)
    total_hours = models.FloatField(blank=True, null=True)
    billable_hours = models.FloatField(blank=True, null=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    budget = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    budget_spent = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    budget_remaining = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    total_costs = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    team_costs = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    cost = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    expenses = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    note = models.ManyToManyField("Note", blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    class Meta:  # https://stackoverflow.com/a/6062320/185820
        ordering = ["name"]


class Report(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    hours = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    amount = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    cost = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    net = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    invoices = models.ManyToManyField("Invoice", blank=True)
    projects = models.ManyToManyField("Project", blank=True)
    clients = models.ManyToManyField("Client", blank=True)
    contacts = models.ManyToManyField("Contact", blank=True)
    notes = models.ManyToManyField("Note", blank=True)

    def __str__(self):
        return "report-%s" % self.date


class Task(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    rate = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    unit = models.DecimalField(
        "Unit", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]


class Time(BaseModel):
    """
    Date, Client, Project, Project Code, Task, Hours, Billable?,
    Invoiced?, First Name, Last Name, Department, Employee?, Billable
    Rate, Billable Amount, Cost Rate, Cost Amount, Currency,
    External Reference URL
    """

    invoiced = models.BooleanField(default=False)
    client = models.ForeignKey(
        Client,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    project = models.ForeignKey(
        Project,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    task = models.ForeignKey(
        Task,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"active": True},
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    invoice = models.ForeignKey(
        Invoice,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"last_payment_date": None},
    )
    date = models.DateField(default=timezone.now, blank=True, null=True)
    hours = models.DecimalField(
        "Hours", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )
    description = models.TextField(blank=True, null=True)

    amount = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)

    # IGCE
    quantity = models.DecimalField(
        "Quantity", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )
    unit = models.CharField(max_length=2, blank=True, null=True)
    unit_price = models.DecimalField(
        "Unit Price",
        default=1.0,
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
    )
    total_price = models.DecimalField(
        "Total Price",
        default=1.0,
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
    )
    cost = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    net = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)

    def __str__(self):
        if self.description:
            return self.description
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://docs.djangoproject.com/en/1.9/ref/models/instances/#get-absolute-url
    def get_absolute_url(self, hostname):
        return "%s/%s" % (hostname, reverse("time_view", args=[str(self.id)]))


class Account(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    number = models.CharField(max_length=300, blank=True, null=True)
    url = models.URLField("URL", max_length=300, blank=True, null=True)
    note = models.ManyToManyField("Note", blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Testimonial(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    issue_date = models.DateField(
        "Issue Date", blank=True, null=True, default=timezone.now
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Service(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]
