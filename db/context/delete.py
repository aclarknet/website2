from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def context_delete(
    context, model_name=None, time_model=None, obj=None, model=None, request=None
):
    url_pattern = "%s_index" % model_name
    invoice = None
    if model_name == "time":  # Save reference to invoice before delete obj
        if obj.invoice:
            invoice = obj.invoice
    if model_name == "profile":  # Delete obj.user
        obj.user.delete()
    else:
        obj.delete()
    if invoice:  # Invoice line item "Amount" and total amount
        invoice.amount = 0
        for time in model.objects.filter(
            invoice=invoice, task__isnull=False, invoiced=False
        ):
            if time.amount:
                invoice.amount += time.amount
        invoice.net = invoice.amount - invoice.cost
        invoice.save()
    messages.add_message(request, messages.INFO, "%s deleted!" % model_name.title())
    if not request.user.is_staff:
        url_pattern = "dashboard"
    return HttpResponseRedirect(reverse(url_pattern))
