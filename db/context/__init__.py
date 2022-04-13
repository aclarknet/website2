import secrets
from random import random

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from faker import Faker

from ..signals import create_profile
from ..utils import get_checked, get_form, get_model_name, paginate, set_items
from .edit import context_edit
from .index import context_index
from .search import context_search
from .view import context_view

fake = Faker()


def get_context(request, **kwargs):
    ############################################################################
    # Args
    ############################################################################
    account_model = kwargs.get("account_model")
    accounts = None
    avatar = None
    client_model = kwargs.get("client_model")
    clients = None
    companies = None
    company_model = kwargs.get("company_model")
    company_name = fake.company()
    contact_model = kwargs.get("contact_model")
    contacts = None
    context_type = kwargs.get("context_type")
    dashboard = False
    display_mode = {"bg": "dark", "text": "light"}
    doc = request.GET.get("doc")
    doc_type = "Invoice"
    filter_by = kwargs.get("filter_by")
    form = kwargs.get("form")
    form_model = kwargs.get("form_model")
    invoice_model = kwargs.get("invoice_model")
    invoices = None
    invoice = None
    item = None
    items = None
    kw_context = kwargs.get("context")
    last_payment_date = None
    mail = request.GET.get("mail")
    mailpdf = request.GET.get("mailpdf")
    message = fake.text()
    model = kwargs.get("model")
    model_name = None
    models = kwargs.get("models")
    new_time = kwargs.get("new_time")
    note_model = kwargs.get("note_model")
    notes = None
    obj = kwargs.get("obj")
    order_by = kwargs.get("order_by")
    page_num = request.GET.get("page")
    pdf = request.GET.get("pdf")
    pk = kwargs.get("pk")
    project_model = kwargs.get("project_model")
    projects = None
    qs_account = request.GET.get("account")
    qs_checked = get_checked(request)
    paginated = qs_checked["paginated"]
    qs_client = request.GET.get("client")
    qs_invoice = request.GET.get("invoice")
    qs_note = request.GET.get("note")
    qs_project = request.GET.get("project")
    qs_user = request.GET.get("user")
    q = request.GET.get("q")
    referer = kwargs.get("referer")
    report_model = kwargs.get("report_model")
    reports = None
    statcard_hours = {}
    statcard_income = {}
    subject = fake.paragraph(nb_sentences=1)
    task_model = kwargs.get("task_model")
    tasks = None
    time_model = kwargs.get("time_model")
    times = None
    user_model = kwargs.get("user_model")
    users = None
    xls = request.GET.get("xls")
    if not kw_context:
        context = {}
    else:
        context = kw_context
    if not referer:
        referer = request.META.get("HTTP_REFERER")
    if model:
        model_name = get_model_name(model)
        items = model.objects.all()
        if filter_by:  # Filter "Items"
            items = items.filter(**filter_by[model_name])
        if order_by:  # Order "Items"
            items = items.order_by(*order_by[model_name])
        if paginated:  # Paginate "Items"
            items = paginate(items, page_num=page_num)
        items = set_items(model_name, items=items)
    elif obj:
        model_name = get_model_name(obj)
    ############################################################################
    # All Items
    ############################################################################
    if account_model:
        accounts = account_model.objects.all()
    if client_model:
        clients = client_model.objects.all()
    if company_model:
        companies = company_model.objects.all()
    if contact_model:
        contacts = contact_model.objects.all()
    if invoice_model:
        invoices = invoice_model.objects.all()
    if note_model:
        notes = note_model.objects.all()
    if project_model:
        projects = project_model.objects.all()
    if report_model:
        reports = report_model.objects.all()
    if task_model:
        tasks = task_model.objects.all()
    if time_model:
        times = time_model.objects.all()
    if user_model:
        users = user_model.objects.all()
    ############################################################################
    # Context
    ############################################################################
    context["accounts"] = accounts
    context["clients"] = clients
    context["companies"] = companies
    context["company_name"] = company_name
    context["contacts"] = contacts
    context["context_type"] = context_type
    context["display_mode"] = display_mode
    context["doc"] = doc
    context["doc_type"] = doc_type
    context["statcard_hours"] = statcard_hours
    context["statcard_income"] = statcard_income
    context["invoices"] = invoices
    context["items"] = items
    context["last_payment_date"] = last_payment_date
    context["mail"] = mail
    context["mailpdf"] = mailpdf
    context["message"] = message
    context["model_name"] = model_name
    context["notes"] = notes
    context["page"] = page_num
    context["paginated"] = paginated
    context["pdf"] = pdf
    context["projects"] = projects
    context["referer"] = referer
    context["request"] = request
    context["reports"] = reports
    context["subject"] = subject
    context["tasks"] = tasks
    context["times"] = times
    context["url_edit"] = "%s_edit" % model_name
    context["users"] = users
    context["xls"] = xls
    if user_model:
        user = user_model.objects.get(username=request.user)
        profile = user.profile
        if not profile.dark:
            display_mode["bg"] = "light"
            display_mode["text"] = "dark"
            context["display_mode"] = display_mode
    if context_type == "search":
        return context_search(context, request=request, models=models, q=q)
    elif context_type == "index":
        ########################################################################
        # Index
        ########################################################################
        return context_index(
            context,
            clients=clients,
            companies=companies,
            invoice_model=invoice_model,
            model_name=model_name,
            report_model=report_model,
            request=request,
            statcard_income=statcard_income,
        )
    elif context_type == "edit":
        ########################################################################
        # Edit
        ########################################################################
        return context_edit(
            context,
            account_model=account_model,
            client_model=client_model,
            company_model=company_model,
            contact_model=contact_model,
            doc_type=doc_type,
            form_model=form_model,
            invoice_model=invoice_model,
            model=model,
            model_name=model_name,
            new_time=new_time,
            note_model=note_model,
            obj=obj,
            pk=pk,
            project_model=project_model,
            qs_account=qs_account,
            qs_checked=qs_checked,
            qs_client=qs_client,
            qs_invoice=qs_invoice,
            qs_note=qs_note,
            qs_project=qs_project,
            qs_user=qs_user,
            request=request,
            time_model=time_model,
            user_model=user_model,
        )
    elif context_type == "new_user":
        ########################################################################
        # New user
        ########################################################################
        if request.user.is_staff:
            if model_name:
                url_pattern = "%s_edit" % model_name
            password = (
                secrets.token_urlsafe()
            )  # https://docs.djangoproject.com/en/3.0/topics/auth/default/#creating-users
            name = fake.name()
            first_name = name.split()[0]
            last_name = name.split()[1]
            email = fake.ascii_email()
            user = model.objects.create_user(first_name.lower(), email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            create_profile(user)
            rate = "%.1f" % (random() * 100)
            bio = fake.text()
            address = fake.address()
            user.profile.rate = rate
            user.profile.bio = bio
            user.profile.address = address
            user.profile.save()
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            messages.add_message(request, messages.INFO, settings.FOUR_O_3)
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        ########################################################################
        # View
        ########################################################################
        return context_view(
            context,
            avatar=avatar,
            company_name=company_name,
            dashboard=dashboard,
            doc_type=doc_type,
            invoice_model=invoice_model,
            item=item,
            items=items,
            last_payment_date=last_payment_date,
            message=message,
            model=model,
            model_name=model_name,
            note_model=note_model,
            order_by=order_by,
            page_num=page_num,
            paginate=paginate,
            paginated=paginated,
            pk=pk,
            project_model=project_model,
            request=request,
            statcard_hours=statcard_hours,
            statcard_income=statcard_income,
            subject=subject,
            time_model=time_model,
        )
