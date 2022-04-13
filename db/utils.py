from functools import reduce
from hashlib import md5
from operator import or_ as OR
from random import random

from babel import numbers
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist as DoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, Q, Sum
from django.utils import timezone
from faker import Faker

fake = Faker()


def get_avatar(email):
    """
    MD5 hash of email address for use with Gravatar.
    """
    gravatar_url = "https://www.gravatar.com/avatar/%s"
    return (
        gravatar_url % md5(email.lower().encode("utf-8")).hexdigest()
    )  # https://stackoverflow.com/a/7585378/185820


def get_model_name(model_or_obj):
    model_name = model_or_obj._meta.verbose_name
    model_name = model_name.replace(" ", "_")
    return model_name


def get_search_results(q, **kwargs):
    models = kwargs.get("models")
    request = kwargs.get("request")
    results = {}
    for model in models:
        model_name = get_model_name(model)
        to_reduce = []
        for field in settings.SEARCH_FIELDS[model_name]:
            to_reduce.append(Q(**{field + "__icontains": q}))
            if request.user.is_staff:
                results[model_name] = model.objects.filter(reduce(OR, to_reduce))
            else:
                if model_name == "time":
                    results[model_name] = model.objects.filter(
                        reduce(OR, to_reduce), user=request.user
                    )
    return results


def get_form(request, **kwargs):
    client_model = kwargs.get("client_model")
    company_model = kwargs.get("company_model")
    contact_model = kwargs.get("contact_model")
    form_model = kwargs.get("form_model")
    invoice_model = kwargs.get("invoice_model")
    model = kwargs.get("model")
    model_name = kwargs.get("model_name")
    obj = kwargs.get("obj")
    project_model = kwargs.get("project_model")

    qs_client = request.GET.get("client")
    qs_project = request.GET.get("project")

    method = "GET"
    if request.method == "POST":  # POST
        method = "POST"

    if model:
        model_name = get_model_name(model)
    elif obj:
        model_name = get_model_name(obj)

    if method == "POST":  # POST
        ########################################################################
        # Exists
        ########################################################################
        if obj:
            if model_name == "user":
                obj = obj.profile  # Edit profile not user
            form = form_model(request.POST, instance=obj)
        ########################################################################
        # New
        ########################################################################
        else:
            form = form_model(request.POST)
    else:  # method == "GET"
        ########################################################################
        # Exists
        ########################################################################
        if obj:
            if model_name == "user":
                obj = obj.profile  # Edit profile not user
                form = form_model(instance=obj)
            else:
                form = form_model(instance=obj)
        ########################################################################
        # New
        ########################################################################
        else:
            if model_name == "report":
                month = (timezone.now() - timezone.timedelta(days=30)).strftime("%B")
                # year = (timezone.now() - timezone.timedelta(days=365)).strftime("%Y")
                year = timezone.now().strftime("%Y")
                name = "%s %s" % (month, year)
                _invoices = invoice_model.objects.filter(last_payment_date=None)
                _projects = project_model.objects.filter(invoice__in=_invoices)
                _clients = client_model.objects.filter(project__in=_projects)
                _contacts = contact_model.objects.filter(client__in=_clients)

                # Calculate "Income" for report form
                _hours, gross, cost, net = agg_income(_invoices)
                obj = model(name=name, hours=_hours, amount=gross, cost=cost, net=net)
                form = form_model(
                    instance=obj,
                    initial={
                        "invoices": _invoices,
                        "projects": _projects,
                        "clients": _clients,
                        "contacts": _contacts,
                    },
                )
            elif model_name == "invoice":
                _project = None
                _client = None
                if qs_project:
                    _project = project_model.objects.get(pk=qs_project)
                    _client = _project.client

                if _client:
                    subject = "%s %s" % (_client, timezone.now().strftime("%B %Y"))
                else:
                    subject = "%s" % (timezone.now().strftime("%B %Y"))

                _company = None
                _companies = company_model.objects.all()
                if len(_companies) > 0:
                    _company = _companies[0]

                start_date = timezone.now()
                end_date = timezone.now() + timezone.timedelta(days=30)
                issue_date = timezone.now() + timezone.timedelta(days=30)
                due_date = timezone.now() + timezone.timedelta(days=60)
                obj = model(
                    subject=subject,
                    start_date=start_date,
                    end_date=end_date,
                    issue_date=issue_date,
                    client=_client,
                    company=_company,
                    project=_project,
                    due_date=due_date,
                )
                form = form_model(instance=obj)
            elif model_name == "project":
                try:
                    client = client_model.objects.get(pk=qs_client)
                except DoesNotExist:
                    client = None
                name = fake.text()
                description = fake.text()
                start_date = timezone.now()
                end_date = timezone.now() + timezone.timedelta(days=30)
                obj = model(
                    client=client,
                    name=name,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                )
                form = form_model(instance=obj)
            elif model_name == "client" or model_name == "company":
                name = fake.text()
                address = fake.address()
                description = fake.text()
                url = "https://%s" % fake.ipv4_private()
                obj = model(
                    name=name, address=address, description=description, url=url
                )
                form = form_model(instance=obj)
            elif model_name == "contact":
                first_name = fake.first_name()
                last_name = fake.last_name()
                address = fake.address()
                client = None
                if qs_client:
                    client = client_model.objects.get(pk=qs_client)
                obj = model(
                    first_name=first_name,
                    last_name=last_name,
                    client=client,
                    address=address,
                )
                form = form_model(instance=obj)
            elif model_name == "task":
                name = fake.text()
                rate = "%.1f" % (random() * 100)
                obj = model(name=name, rate=rate)
                form = form_model(instance=obj)
            elif model_name == "note":
                title = fake.text()
                obj = model(title=title)
                form = form_model(instance=obj)
            else:
                form = form_model()
    return form


def get_checked(request):
    qs_checked = {}
    qs_active = request.POST.get("checkbox-active")
    qs_subscribe = request.POST.get("checkbox-subscribe")
    qs_invoiced = request.POST.get("invoiced")
    qs_paginated = request.GET.get("paginated")
    condition = (  # if any of these exist
        qs_active == "on"
        or qs_active == "off"
        or qs_subscribe == "on"
        or qs_subscribe == "off"
        or qs_invoiced == "true"
        or qs_invoiced == "false"
    )
    if qs_paginated == "false":
        paginated = False
    else:
        paginated = True
    qs_checked["active"] = qs_active
    qs_checked["invoiced"] = qs_invoiced
    qs_checked["subscribe"] = qs_subscribe
    qs_checked["condition"] = condition
    qs_checked["paginated"] = paginated
    return qs_checked


def set_items(model_name, items=None, _items={}):
    """
    Returning dictionary of items e.g.
        for item in items.reports
    instead of:
        for item in reports
    """
    i = {}
    i["%ss" % model_name] = items
    for key in _items.keys():
        i[key] = _items[key]
    return i


def paginate(items, orphans=None, page_num=None):
    try:
        paginator = Paginator(items, 10, orphans=orphans)
    except TypeError:
        try:
            paginator = Paginator(items, 10, orphans=0)
        except TypeError:
            paginator = Paginator(items, 10, orphans=0)
    try:
        items = paginator.page(page_num)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items


def add_times(time_model, invoice, obj=None):
    _times = time_model.objects.filter(invoiced=False, invoice=invoice)
    invoice.amount = 0  # Invoice line item "Amount" and total amount
    invoice.cost = 0
    invoice.hours = 0
    for time in _times:
        if not time.task and invoice.project:
            if invoice.project.task:
                time.task = invoice.project.task
                if obj.pk == time.pk:
                    obj.task = invoice.project.task
                    obj.save()
        time.amount = 0
        if not invoice.doc_type == "Task Order":
            if time.task:
                if time.task.rate and time.hours:
                    time.amount = time.task.rate * time.hours
        else:  # Task Order
            if invoice.user.profile.rate and time.hours:
                time.amount = invoice.user.profile.rate * time.hours

        invoice.amount += time.amount
        if time.hours:
            invoice.hours += time.hours
        try:  # Calculate "Income" for invoice
            time.cost = time.user.profile.rate * time.hours
        except TypeError:
            time.cost = 0
        invoice.cost += time.cost
        time.net = time.amount - time.cost
        time.save()
    invoice.net = invoice.amount - invoice.cost
    invoice.save()
    if obj:
        return obj
    else:
        return invoice


def agg_income(queryset):
    hours = gross = cost = net = 0
    _hours = queryset.aggregate(hours=Sum(F("hours")))["hours"]
    if _hours:
        hours = _hours
    _gross = queryset.aggregate(amount=Sum(F("amount")))["amount"]
    if _gross:
        gross = _gross
    _cost = queryset.aggregate(cost=Sum(F("cost")))["cost"]
    if _cost:
        cost = _cost
    _net = queryset.aggregate(net=Sum(F("net")))["net"]
    if _net:
        net = _net
    return hours, gross, cost, net


def get_message(item, model_name, times=None):
    if model_name == "invoice":
        sendto = None  # Send Invoice or Statement of Work to Client, Task Order to User
        if item.doc_type == "Invoice" or item.doc_type == "Statement of Work":
            sendto = item.client
        elif item.doc_type == "Task Order":
            if item.user:
                sendto = "%s %s" % (item.user.first_name, item.user.last_name)
        if sendto:
            subject = "%s for %s" % (item.doc_type, sendto)
        else:
            subject = item.doc_type
        message = "%s\n" % subject
        message += "Project: %s\n" % item.project
        message += "Period of Performance: %s — %s.\n" % (
            item.start_date.strftime("%B %d, %Y"),
            item.end_date.strftime("%B %d, %Y"),
        )
        if item.project:  # https://stackoverflow.com/a/16892825/185820
            if item.doc_type == "Task Order" and item.user:
                message += "Rate: %s per hour.\n" % numbers.format_currency(
                    item.user.profile.rate, "USD", locale="en"
                )
            else:
                if item.project.task:
                    message += "Rate: %s per hour.\n" % numbers.format_currency(
                        item.project.task.rate, "USD", locale="en"
                    )
        message += "Hours: %s\n" % format(item.hours, ",f")
        message += "Amount: %s\n" % numbers.format_currency(
            item.amount, "USD", locale="en"
        )
        message += "Tasks:\n"
        message += "\n".join(["- %s" % i.description for i in item.time_set.all()])
    elif model_name == "note":  # Mail
        subject = item.title
        message = item.text
        message += "\n"
        message += "\n".join(
            ["- %s" % i.title for i in item.notes.all().order_by("-updated")]
        )
    elif model_name == "report":
        report_cost = item.cost
        if not report_cost:
            report_cost = 0
        message = "Gross: %s\nCost: %s\nNet: %s\n" % (
            numbers.format_currency(item.amount, "USD", locale="en"),
            numbers.format_currency(report_cost, "USD", locale="en"),
            numbers.format_currency(item.net, "USD", locale="en"),
        )
        subject = item.name
    elif model_name == "user":
        hours, gross, cost, net = agg_income(times)
        month = (timezone.now() - timezone.timedelta(days=30)).strftime("%B")
        year = (timezone.now() - timezone.timedelta(days=365)).strftime("%Y")
        if item.first_name and item.last_name:
            subject = "Hours for %s %s, %s %s" % (
                item.first_name,
                item.last_name,
                month,
                year,
            )
        else:
            subject = "Hours for %s, %s %s" % (item.username, month, year)
        message = "Hours: %s\nGross: %s\nCost: %s\nNet: %s\n" % (
            hours,
            numbers.format_currency(gross, "USD", locale="en"),
            numbers.format_currency(cost, "USD", locale="en"),
            numbers.format_currency(net, "USD", locale="en"),
        )
    return message, subject
