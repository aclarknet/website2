import io

from crispy_forms.helper import FormHelper
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import viewsets
# from sphinxcontrib.websupport import WebSupport
from xhtml2pdf import pisa

from project.models import User

from ..context import get_context
from ..export import render_doc, render_pdf
from ..forms import (
    AccountForm,
    AdminProfileForm,
    AdminTimeForm,
    ClientForm,
    CompanyForm,
    ContactForm,
    ExpenseForm,
    InvoiceForm,
    NoteForm,
    NoteFormText,
    ProfileForm,
    ReportForm,
    TaskForm,
    TimeForm,
)
from ..models import (
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
    # User,
)
from ..serializers import ClientSerializer
from . import client


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(publish=True).order_by("name")
    serializer_class = ClientSerializer


@staff_member_required
def account_view(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        company_model=Company,
        context_type="view",
        account_model=Account,
        contact_model=Contact,
        client_model=Client,
        invoice_model=Invoice,
        note_model=Note,
        model=Account,
        pk=pk,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "account_view.html", context)


@staff_member_required
def account_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        form_model=AccountForm,
        model=Account,
        pk=pk,
        project_model=Project,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def account_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=Account,
        order_by={"account": ("-active", "name")},
        project_model=Project,
        task_model=Task,
    )
    return render(request, "account_index.html", context)


@staff_member_required
def client_view(request, pk=None):
    order_by = {
        "time": (),
        "client": (),
        "contact": (),
        "project": ("-start_date",),
        "invoice": ("-issue_date",),
    }
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        context_type="view",
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        model=Client,
        order_by=order_by,
        pk=pk,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "client_view.html", context)


@staff_member_required
def client_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        form_model=ClientForm,
        model=Client,
        pk=pk,
        project_model=Project,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def client_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        model=Client,
        client_model=Client,
        invoice_model=Invoice,
        order_by={"client": ("-active", "name")},
        project_model=Project,
        task_model=Task,
    )
    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        send_mail(
            subject,
            message,
            settings.MAIL_FROM,
            [settings.MAIL_TO],
            fail_silently=False,
        )
        messages.add_message(request, messages.INFO, "Mail sent!")
    return render(request, "client_index.html", context)


def competency(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        project_model=Project,
        task_model=Task,
    )
    if context["pdf"]:
        filename = "%s-%s.pdf" % (context["company_name"], "competency")
        return render_pdf(context, filename=filename, template="competency.html")
    return render(request, "competency_view.html", context)


@staff_member_required
def company_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        form_model=CompanyForm,
        model=Company,
        pk=pk,
        project_model=Project,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def company_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=Company,
        order_by={"company": ("-active", "name")},
        project_model=Project,
        task_model=Task,
    )
    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        send_mail(
            subject,
            message,
            settings.MAIL_FROM,
            [settings.MAIL_TO],
            fail_silently=False,
        )
        messages.add_message(request, messages.INFO, "Mail sent!")
    return render(request, "company_index.html", context)


@staff_member_required
def company_view(request, pk=None):
    context = get_context(
        request,
        account_model=Account,
        client_model=Client,
        company_model=Company,
        contact_model=Contact,
        context_type="view",
        invoice_model=Invoice,
        model=Company,
        note_model=Note,
        pk=pk,
        project_model=Project,
        report_model=Report,
        task_model=Task,
        time_model=Time,
        user_model=User,
    )
    return render(request, "company_view.html", context)


@staff_member_required
def contact_view(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        context_type="view",
        account_model=Account,
        model=Contact,
        client_model=Client,
        invoice_model=Invoice,
        pk=pk,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "contact_view.html", context)


@staff_member_required
def contact_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        form_model=ContactForm,
        model=Contact,
        pk=pk,
        project_model=Project,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def contact_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=Contact,
        order_by={"contact": ("-active", "last_name", "first_name")},
        project_model=Project,
        task_model=Task,
    )
    return render(request, "contact_index.html", context)


# def doc(request):
#     context = {}
#     support = WebSupport(datadir="db/doc/_websupport/data")
#     document = support.get_document("index")
#     context["document"] = document
#     return render(request, "doc.html", context)


def error(request):
    raise


@login_required
def home(request):
    if request.user.is_staff:  # show everyone's times
        filter_by = {"time": {"invoiced": False}}
    else:  # show user's times
        filter_by = {"time": {"invoiced": False, "user": request.user}}
    order_by = {
        "invoice": ("client",),
        "time": ("-active", "-date"),
    }
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        context_type="home",
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        filter_by=filter_by,
        order_by=order_by,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "dashboard.html", context)


@staff_member_required
def invoice_view(request, pk=None):
    order_by = {"invoice": (), "time": ("date",)}
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        context_type="view",
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        model=Invoice,
        order_by=order_by,
        project_model=Project,
        pk=pk,
        task_model=Task,
    )

    filename = "%s-%s-%s" % (
        context["company_name"],
        slugify(context["doc_type"].lower()),
        pk,
    )

    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        send_mail(
            subject,
            message,
            settings.MAIL_FROM,
            [settings.MAIL_TO],
            fail_silently=False,
        )
        messages.add_message(request, messages.INFO, "Mail sent!")

    if context["pdf"]:
        filename = ".".join((filename, "pdf"))
        return render_pdf(context, filename=filename, template="invoice_table.html")

    if context["mailpdf"]:
        context["pdf"] = True
        # https://docs.djangoproject.com/en/3.1/topics/email/#emailmessage-objects
        # https://docs.djangoproject.com/en/3.1/topics/templates/#django.template.loader.render_to_string
        # https://docs.djangoproject.com/en/3.1/howto/outputting-pdf/
        # https://gist.github.com/nitinbhojwani/a5f9bab74185b04ad6e73e37a970ad37
        # https://xhtml2pdf.readthedocs.io/en/latest/usage.html#using-with-python-standalone
        subject = context["subject"]
        email = EmailMessage(subject, "", settings.MAIL_FROM, [settings.MAIL_TO], [])
        source_html = render_to_string("invoice_table.html", context=context)
        buf = io.BytesIO()
        pisa.CreatePDF(source_html, dest=buf)
        email.attach(filename, buf.getvalue(), "application/pdf")
        email.send(fail_silently=False)
        messages.add_message(request, messages.INFO, "Mail sent!")
    return render(request, "invoice_view.html", context)


@staff_member_required
def invoice_edit(request, pk=None):
    invoice = None
    if pk:
        invoice = Invoice.objects.get(pk=pk)
    time_extra = request.GET.get("time-extra")
    time_plus = request.GET.get("time-plus")
    time_minus = request.GET.get("time-minus")
    if time_plus:
        time_extra = int(time_extra) + 1
    elif time_minus:
        time_extra = int(time_extra) - 1
    else:
        time_extra = 0
    context = {}
    context["time_extra"] = time_extra
    context["time_plus"] = time_plus
    context["time_minus"] = time_minus
    formset_helper_time = TimeFormSetHelper()

    TimeFormSet = inlineformset_factory(
        Invoice,
        Time,
        fields=("hours", "date", "description"),
        can_order=False,
        can_delete=True,
        extra=time_extra,
    )

    if request.method == "POST":
        time_formset = TimeFormSet(
            request.POST, request.FILES, instance=invoice, prefix="time"
        )

        if time_formset.is_valid():
            time_formset.save()
            return redirect(reverse("invoice_view", kwargs={"pk": pk}))
    else:
        time_formset = TimeFormSet(instance=invoice, prefix="time")
    context["time_formset"] = time_formset
    context["formset_helper_time"] = formset_helper_time
    return get_context(
        request,
        account_model=Account,
        client_model=Client,
        company_model=Company,
        contact_model=Contact,
        context=context,
        context_type="edit",
        form_model=InvoiceForm,
        invoice_model=Invoice,
        model=Invoice,
        note_model=Note,
        pk=pk,
        project_model=Project,
        report_model=Report,
        task_model=Task,
        time_model=Time,
        user_model=User,
    )


@staff_member_required
def invoice_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=Invoice,
        order_by={
            "invoice": ("-last_payment_date", "-active", "-issue_date", "client")
        },
        project_model=Project,
        task_model=Task,
    )
    return render(request, "invoice_index.html", context)


def login(request):
    context = {}
    context["login"] = True
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # https://stackoverflow.com/a/39316967/185820
            auth_login(request, user)
            messages.add_message(request, messages.INFO, "Logged in!")
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            messages.add_message(request, messages.WARNING, "Login failed!")
            return HttpResponseRedirect(reverse("dashboard"))
    return render(request, "login.html", context)


def logout(request):
    auth_logout(request)
    # Redirect to a success page.
    messages.add_message(request, messages.INFO, "Logged out!")
    return HttpResponseRedirect("/")


@login_required
def lounge(request):
    context = {}
    context["lounge_away"] = settings.LOUNGE_AWAY
    return render(request, "lounge.html", context)


@staff_member_required
def note_view(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        context_type="view",
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        model=Note,
        pk=pk,
        project_model=Project,
        task_model=Task,
    )
    item = context["item"]
    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        html_message = None
        if item.html:
            html_message = message
        send_mail(
            subject,
            message,
            settings.MAIL_FROM,
            [settings.MAIL_TO],
            fail_silently=False,
            html_message=html_message,
        )
        messages.add_message(request, messages.INFO, "Mail sent!")
    elif context["pdf"]:
        filename = ".".join(("note-%s" % item.pk, "pdf"))
        return render_pdf(context, filename=filename, template="note_export.html")
    elif context["doc"]:
        filename = ".".join((filename, "doc"))
        return render_doc(context, filename=filename, template="note_export.html")
    return render(request, "note_view.html", context)


@staff_member_required
def note_edit(request, pk=None):
    form_model = NoteFormText
    if pk:
        note = Note.objects.get(id=pk)
        if note.html:
            form_model = NoteForm
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        form_model=form_model,
        model=Note,
        client_model=Client,
        project_model=Project,
        task_model=Task,
        invoice_model=Invoice,
        pk=pk,
        context_type="edit",
    )


@staff_member_required
def note_index(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        project_model=Project,
        model=Note,
        order_by={"note": ("-active", "-created")},
        task_model=Task,
    )
    return render(request, "note_index.html", context)


@staff_member_required
def expense_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        form_model=ExpenseForm,
        model=Expense,
        client_model=Client,
        project_model=Project,
        task_model=Task,
        invoice_model=Invoice,
        pk=pk,
        context_type="edit",
    )


@staff_member_required
def expense_index(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        project_model=Project,
        model=Expense,
        task_model=Task,
    )
    return render(request, "expense_index.html", context)


@staff_member_required
def expense_view(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        context_type="view",
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        model=Expense,
        pk=pk,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "expense_view.html", context)


@staff_member_required
def report_view(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        context_type="view",
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        project_model=Project,
        model=Report,
        pk=pk,
        task_model=Task,
    )
    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        send_mail(
            subject,
            message,
            settings.MAIL_FROM,
            [settings.MAIL_TO],
            fail_silently=False,
        )
        messages.add_message(request, messages.INFO, "Mail sent!")
        return render(request, "report_view.html", context)
    elif context["pdf"]:
        filename = "%s-%s-%s.pdf" % (context["company_name"], "report", pk)
        return render_pdf(context, filename=filename, template="report.html")
    else:
        return render(request, "report_view.html", context)


@staff_member_required
def report_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        form_model=ReportForm,
        model=Report,
        pk=pk,
        project_model=Project,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def report_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=Report,
        order_by={"report": ("-date",)},
        project_model=Project,
        task_model=Task,
    )
    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        send_mail(
            subject,
            message,
            settings.MAIL_FROM,
            [settings.MAIL_TO],
            fail_silently=False,
        )
        messages.add_message(request, messages.INFO, "Mail sent!")
    return render(request, "report_index.html", context)


@login_required
def search_index(request):
    models = (
        Account,
        Client,
        Company,
        Contact,
        Invoice,
        Note,
        Profile,
        Project,
        Report,
        Task,
        Time,
        User,
    )
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="search",
        models=models,
        client_model=Client,
        invoice_model=Invoice,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "search_index.html", context)


@staff_member_required
def task_view(request, pk=None):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        company_model=Company,
        contact_model=Contact,
        context_type="view",
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        model=Task,
        pk=pk,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "task_view.html", context)


@staff_member_required
def task_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        client_model=Client,
        invoice_model=Invoice,
        form_model=TaskForm,
        project_model=Project,
        model=Task,
        pk=pk,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def task_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=Task,
        order_by={"task": ("-active", "name")},
        project_model=Project,
        task_model=Task,
    )
    return render(request, "task_index.html", context)


@login_required
def time_view(request, pk=None):
    """
    Authenticated users can only view their own time entries unless
    they are staff.
    """
    time = get_object_or_404(Time, pk=pk)
    if not request.user.is_staff and not time.user:  # No user
        messages.add_message(request, messages.WARNING, settings.FOUR_O_3)
        return HttpResponseRedirect(reverse("dashboard"))
    elif (
        not request.user.is_staff and not time.user.username == request.user.username
    ):  # Time entry user does not match user
        messages.add_message(request, messages.WARNING, settings.FOUR_O_3)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        context = get_context(
            request,
            report_model=Report,
            user_model=User,
            time_model=Time,
            note_model=Note,
            company_model=Company,
            contact_model=Contact,
            context_type="view",
            account_model=Account,
            client_model=Client,
            invoice_model=Invoice,
            model=Time,
            pk=pk,
            project_model=Project,
            task_model=Task,
        )
        return render(request, "time_view.html", context)


@login_required
def time_edit(request, pk=None):
    """
    Authenticated users can only edit their own time entries unless
    they are staff.
    """
    if pk is not None:
        time = get_object_or_404(Time, pk=pk)
        if not request.user.is_staff and not time.user:  # No user
            messages.add_message(request, messages.WARNING, settings.FOUR_O_3)
            return HttpResponseRedirect(reverse("home"))
        elif (
            not request.user.is_staff
            and not time.user.username == request.user.username
        ):  # Time entry user does not match user
            messages.add_message(request, messages.WARNING, settings.FOUR_O_3)
            return HttpResponseRedirect(reverse("home"))
    if request.user.is_staff:
        time_form = AdminTimeForm
    else:
        time_form = TimeForm
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        client_model=Client,
        form_model=time_form,
        model=Time,
        invoice_model=Invoice,
        project_model=Project,
        task_model=Task,
        pk=pk,
        context_type="edit",
    )


@staff_member_required
def time_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=Time,
        filter_by={"time": {"user__isnull": False}},
        order_by={"time": ("invoiced", "-date")},
        project_model=Project,
        task_model=Task,
    )
    return render(request, "time_index.html", context)


@login_required
def user_view(request, pk=None):

    if not request.user.pk == int(pk) and not request.user.is_staff:
        messages.add_message(request, messages.WARNING, settings.FOUR_O_3)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        order_by = {
            "time": ("invoiced", "-date"),
            "project": (),
            "user": (),
            "invoice": (),
        }
        context = get_context(
            request,
            report_model=Report,
            user_model=User,
            time_model=Time,
            note_model=Note,
            company_model=Company,
            contact_model=Contact,
            context_type="view",
            account_model=Account,
            client_model=Client,
            invoice_model=Invoice,
            model=User,
            order_by=order_by,
            profile_model=Profile,
            project_model=Project,
            task_model=Task,
            pk=pk,
        )
        if context["pdf"]:
            item = context["item"]
            filename = ".".join(
                (
                    "aclarknet-user-%s"
                    % "-".join([item.first_name.lower(), item.last_name.lower()]),
                    "pdf",
                )
            )
            return render_pdf(context, filename=filename, template="user_export.html")
        if context["mail"]:
            message = context["message"]
            subject = context["subject"]
            send_mail(
                subject,
                message,
                settings.MAIL_FROM,
                [settings.MAIL_TO],
                fail_silently=False,
            )
            messages.add_message(request, messages.INFO, "Mail sent!")
        return render(request, "user_view.html", context)


@login_required
def user_edit(request, pk=None):
    if request.user.is_staff:
        profile_form = AdminProfileForm
    else:
        profile_form = ProfileForm
    if pk is not None:
        if hasattr(request.user, "profile"):
            if not request.user.pk == int(pk) and not request.user.is_staff:
                messages.add_message(request, messages.WARNING, settings.FOUR_O_3)
                return HttpResponseRedirect(reverse("dashboard"))
    else:  # new user
        return get_context(
            request,
            report_model=Report,
            user_model=User,
            time_model=Time,
            note_model=Note,
            contact_model=Contact,
            company_model=Company,
            account_model=Account,
            client_model=Client,
            invoice_model=Invoice,
            form_model=profile_form,
            model=User,
            pk=pk,
            profile_model=Profile,
            project_model=Project,
            context_type="new_user",
            task_model=Task,
        )
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        client_model=Client,
        invoice_model=Invoice,
        form_model=profile_form,
        model=User,
        pk=pk,
        profile_model=Profile,
        project_model=Project,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def user_index(request):
    context = get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        context_type="index",
        client_model=Client,
        invoice_model=Invoice,
        model=User,
        order_by={"user": ("-profile__active", "last_name", "first_name")},
        filter_by={"user": {"is_active": True}},
        project_model=Project,
        task_model=Task,
    )
    return render(request, "user_index.html", context)


class TimeFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
