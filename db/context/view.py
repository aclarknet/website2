from babel import numbers
from django.db.models import F, Sum
from django.utils.text import slugify

from ..utils import agg_income, get_avatar, get_message, set_items


def context_view(
    context,
    request=None,
    model=None,
    invoice_model=None,
    pk=None,
    statcard_income=None,
    statcard_hours=None,
    note_model=None,
    model_name=None,
    time_model=None,
    order_by=None,
    avatar=None,
    dashboard=None,
    paginated=None,
    paginate=None,
    page_num=None,
    company_name=None,
    doc_type=None,
    item=None,
    items=None,
    last_payment_date=None,
    message=None,
    subject=None,
    project_model=None,
):
    if model:
        item = model.objects.get(pk=pk)
    else:  # Home
        dashboard = True
        times_entered = time_model.objects.filter(invoiced=False, user=request.user)
        times_approved = times_entered.filter(invoice__isnull=False)
        statcard_hours["entered"] = times_entered.aggregate(hours=Sum(F("hours")))[
            "hours"
        ]
        statcard_hours["approved"] = times_approved.aggregate(hours=Sum(F("hours")))[
            "hours"
        ]
        times_user = time_model.objects.filter(user=request.user, invoiced=False)
        invoices_overview = invoice_model.objects.filter(last_payment_date=None)
        if order_by:
            times_user = times_user.order_by(*order_by["time"])
            invoices_overview = invoices_overview.order_by(*order_by["invoice"])
        if paginated:
            times_user = paginate(times_user, page_num=page_num)
            invoices_overview = paginate(invoices_overview, page_num=page_num)
        items = set_items("time", items=times_user)
        items = set_items("invoice", items=invoices_overview, _items=items)
    if invoice_model:
        invoices = invoice_model.objects.filter(last_payment_date=None)
        hours_income, gross, cost, net = agg_income(invoices)
        gross = numbers.format_currency(gross, "USD", locale="en")
        cost = numbers.format_currency(cost, "USD", locale="en")
        net = numbers.format_currency(net, "USD", locale="en")
        statcard_income["hours"] = hours_income
        statcard_income["gross"] = gross
        statcard_income["cost"] = cost
        statcard_income["net"] = net
    if note_model:
        notes_pinned = note_model.objects.filter(pin=True)
        context["notes_pinned"] = notes_pinned
    if model_name == "note":
        message, subject = get_message(item, model_name)  # Mail
    elif model_name == "report":
        message, subject = get_message(item, model_name)  # Mail
    elif model_name == "invoice":
        message, subject = get_message(item, model_name)  # Mail
        times_invoice = time_model.objects.filter(invoice=item)
        if order_by:
            times_invoice = times_invoice.order_by(*order_by["time"])
        last_payment_date = item.last_payment_date
        if item.doc_type:
            doc_type = item.doc_type
        items = set_items("time", items=times_invoice)
        hours_invoice, gross, cost, net = agg_income(invoices)
        gross = numbers.format_currency(gross, "USD", locale="en")
        cost = numbers.format_currency(cost, "USD", locale="en")
        net = numbers.format_currency(net, "USD", locale="en")
        statcard_income["hours"] = hours_invoice
        statcard_income["gross"] = gross
        statcard_income["cost"] = cost
        statcard_income["net"] = net
        if item.client:
            company_name = slugify(item.client.name)
    elif model_name == "user":
        times_user = time_model.objects.filter(user=item, invoiced=False)
        message, subject = get_message(item, model_name, times=times_user)  # Mail
        if item.email:
            avatar = get_avatar(item.email)
        times_entered = times_user.aggregate(hours=Sum(F("hours")))["hours"]
        times_approved = times_user.filter(invoice__isnull=False)
        statcard_hours["entered"] = times_entered
        statcard_hours["approved"] = times_approved.aggregate(hours=Sum(F("hours")))[
            "hours"
        ]
        user_hours, user_gross, user_cost, user_net = agg_income(times_user)
        if item.profile.rate:
            user_cost = user_hours * item.profile.rate
        user_hours = "%.1f" % user_hours
        user_gross = numbers.format_currency(user_gross, "USD", locale="en")
        user_cost = numbers.format_currency(user_cost, "USD", locale="en")
        user_net = numbers.format_currency(user_net, "USD", locale="en")
        statcard_income["hours"] = user_hours
        statcard_income["gross"] = user_gross
        statcard_income["cost"] = user_cost
        statcard_income["net"] = user_net
        if paginated:
            times_user = paginate(times_user, page_num=page_num)
        items = set_items("time", items=times_user)
    elif model_name == "project":
        if order_by and invoice_model:
            invoices = invoice_model.objects.filter(project=item)
            invoices = invoices.order_by(*order_by["invoice"])
            items = set_items("invoice", items=invoices, _items=items)
    elif model_name == "client":
        if order_by and project_model:
            projects = project_model.objects.filter(client=item)
            projects = projects.order_by(*order_by["project"])
            items = set_items("project", items=projects, _items=items)
    context["avatar"] = avatar
    context["company_name"] = company_name
    context["dashboard"] = dashboard
    context["doc_type"] = doc_type
    context["item"] = item
    context["items"] = items
    context["last_payment_date"] = last_payment_date
    context["message"] = message
    context["subject"] = subject
    context["statcard_income"] = statcard_income
    context["statcard_hours"] = statcard_hours
    return context
