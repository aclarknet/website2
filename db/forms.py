from django import forms
from django.conf import settings
from django.utils import timezone

from .models import (
    Account,
    Client,
    Company,
    Contact,
    Expense,
    Invoice,
    Note,
    Profile,
    Project,
    Report,
    Task,
    Time,
)


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("dark", "rate", "bio", "address")


class AdminTimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ("invoiced", "date", "hours", "description", "invoice", "user")
        widgets = {"hours": forms.widgets.NumberInput(attrs={"class": "col-2"})}

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("active", "name", "number", "url", "note")

    note = forms.ModelMultipleChoiceField(
        required=False, queryset=Note.objects.all().order_by("title")
    )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "active",
            "publish",
            "name",
            "address",
            "description",
            "url",
            "company",
            "tags",
        )


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name", "address", "description", "url", "publish")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "active",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "client",
        )


class InvoiceForm(forms.ModelForm):
    """
    Issue Date, Last Payment Date, Invoice ID, PO Number, Client, Subject,
    Invoice Amount, Paid Amount, Balance, Subtotal, Discount, Tax, Tax2,
    Currency, Currency Symbol, Document Type
    """

    class Meta:
        model = Invoice
        fields = (
            "active",
            "subject",
            "doc_type",
            "company",
            "client",
            "user",
            "project",
            "note",
            "issue_date",
            "start_date",
            "end_date",
            "due_date",
            "last_payment_date",
            "ein",
            "po_number",
            "sa_number",
        )
        widgets = {
            "ein": forms.widgets.NumberInput(attrs={"class": "col-2"}),
            "po_number": forms.widgets.NumberInput(attrs={"class": "col-2"}),
            "sa_number": forms.widgets.NumberInput(attrs={"class": "col-2"}),
            # "note": forms.widgets.SelectMultiple(),
        }

    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )

    last_payment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )

    doc_type = forms.CharField(
        widget=forms.Select(choices=settings.DOC_TYPES), required=False
    )


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("active", "html", "pin", "title", "text", "notes")
        labels = {"notes": "Notes"}

    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "tinymce", "rows": 30})
    )
    notes = forms.ModelMultipleChoiceField(
        required=False, queryset=Note.objects.all().order_by("title")
    )


class NoteFormText(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("active", "html", "pin", "title", "text", "notes")
        labels = {"notes": "Notes"}

    notes = forms.ModelMultipleChoiceField(
        required=False, queryset=Note.objects.all().order_by("title")
    )


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("name", "description", "amount")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("dark", "rate", "bio", "address")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "active",
            "name",
            "description",
            "client",
            "task",
            "team",
            "note",
            "start_date",
            "end_date",
        )
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "col-2"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = (
            "active",
            "name",
            "date",
            "hours",
            "amount",
            "net",
            "invoices",
            "projects",
            "clients",
            "contacts",
            "notes",
        )

    invoices = forms.ModelMultipleChoiceField(
        required=False, queryset=Invoice.objects.all().order_by("-issue_date")
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("active", "name", "rate", "unit")


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ("date", "hours", "description")
        widgets = {"hours": forms.widgets.NumberInput(attrs={"class": "col-2"})}

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now,
    )
