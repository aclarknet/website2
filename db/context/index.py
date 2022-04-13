from babel import numbers
from django.utils import timezone

from ..utils import agg_income


def context_index(
    context,
    request=None,
    invoice_model=None,
    model_name=None,
    statcard_income=None,
    clients=None,
    report_model=None,
    companies=None,
):
    if not request.user.is_authenticated:
        context["items"] = []
    if invoice_model:
        invoices_index = invoice_model.objects.filter(last_payment_date=None)
        hours_index, gross, cost, net = agg_income(invoices_index)
        gross = numbers.format_currency(gross, "USD", locale="en")
        cost = numbers.format_currency(cost, "USD", locale="en")
        net = numbers.format_currency(net, "USD", locale="en")
        statcard_income["hours"] = hours_index
        statcard_income["gross"] = gross
        statcard_income["cost"] = cost
        statcard_income["net"] = net
        context["statcard_income"] = statcard_income
    if model_name == "invoice":
        invoices_income = invoice_model.objects.filter(active=True)
        hours_invoice, gross, cost, net = agg_income(invoices_income)
        gross = numbers.format_currency(gross, "USD", locale="en")
        cost = numbers.format_currency(cost, "USD", locale="en")
        net = numbers.format_currency(net, "USD", locale="en")
        statcard_income["hours"] = hours_invoice
        statcard_income["gross"] = gross
        statcard_income["cost"] = cost
        statcard_income["net"] = net
        context["statcard_income"] = statcard_income
    elif model_name == "report":
        _reports = report_model.objects.filter(active=True)
        hours_report, gross, cost, net = agg_income(_reports)
        gross = numbers.format_currency(gross, "USD", locale="en")
        cost = numbers.format_currency(cost, "USD", locale="en")
        net = numbers.format_currency(net, "USD", locale="en")
        statcard_income["hours"] = hours_report
        statcard_income["gross"] = gross
        statcard_income["cost"] = cost
        statcard_income["net"] = net
        context["statcard_income"] = statcard_income
        now = timezone.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        context["subject"] = "Report %s-%s-%s" % (year, month, day)
        context["message"] = "\n\nHours: %s\nGross: %s\nCost: %s\nNet: %s\n" % (  # Mail
            hours_report,
            gross,
            cost,
            net,
        )
    elif model_name == "company":
        context["subject"] = "Companies"
        context["message"] = "\n".join(["- %s" % i.name for i in companies])  # Export
    elif model_name == "client":
        context["subject"] = "Clients"
        context["message"] = "\n".join(["- %s" % i.name for i in clients])  # Export
    return context
