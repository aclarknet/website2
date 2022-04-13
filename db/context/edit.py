from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from ..utils import add_times, agg_income, get_form

from .delete import context_delete


def context_edit(
    context,
    doc_type=None,
    model_name=None,
    request=None,
    account_model=None,
    client_model=None,
    contact_model=None,
    company_model=None,
    form_model=None,
    invoice_model=None,
    model=None,
    project_model=None,
    time_model=None,
    note_model=None,
    user_model=None,
    new_time=None,
    pk=None,
    qs_checked=None,
    qs_invoice=None,
    qs_client=None,
    qs_project=None,
    qs_account=None,
    qs_user=None,
    qs_note=None,
    obj=None,
):
    if model_name:
        url_pattern = "%s_edit" % model_name
        template_name = "%s.html" % url_pattern
    if pk is None:
        ####################################################################
        # New
        ####################################################################
        form = get_form(
            request,
            account_model=account_model,
            client_model=client_model,
            contact_model=contact_model,
            company_model=company_model,
            form_model=form_model,
            invoice_model=invoice_model,
            model=model,
            project_model=project_model,
            user_model=user_model,
        )
    else:
        ####################################################################
        # Exists
        ####################################################################
        obj = model.objects.get(pk=pk)
        form = get_form(
            request,
            form_model=form_model,
            obj=obj,
            client_model=client_model,
            project_model=project_model,
        )
    if request.method == "POST":  # POST
        qs_copy = request.POST.get("copy")
        qs_delete = request.POST.get("delete")
        qs_referer = request.POST.get("referer")
        new_time = False
        if pk is None:
            ################################################################
            # New
            ################################################################
            if model_name == "time":
                new_time = True
            form = get_form(request, form_model=form_model, model_name=model_name)
        else:
            ################################################################
            # Exists
            ################################################################
            form = get_form(
                request, form_model=form_model, model_name=model_name, obj=obj
            )
        if qs_copy:
            ################################################################
            # Copy
            ################################################################
            obj_copy = obj
            obj_copy.pk = None
            obj_copy.save()  # Get a new pk
            url_pattern = "%s_edit" % model_name
            return HttpResponseRedirect(
                reverse(url_pattern, kwargs={"pk": obj_copy.pk})
            )
        if qs_delete:
            ################################################################
            # Delete
            ################################################################
            if model_name == "user":
                if request.user.is_staff:
                    return context_delete(request, obj=obj, model=model)
            elif model_name == "time":
                if request.user.is_staff:
                    return context_delete(
                        request,
                        obj=obj,
                        model=model,
                        referer=qs_referer,
                    )
                else:  # Don't let user delete old invoiced time entries
                    if not obj.invoiced:
                        return context_delete(request, obj=obj, model=model)
                    else:
                        messages.add_message(request, messages.INFO, settings.FOUR_O_3)
                        url_pattern = "dashboard"
                        return HttpResponseRedirect(reverse(url_pattern))
            else:
                return context_delete(
                    request,
                    obj=obj,
                    model=model,
                    request=request,
                    model_name=model_name,
                )
        if qs_checked["condition"]:
            ################################################################
            # Check
            ################################################################
            url_pattern = "%s_index" % model_name
            if qs_checked["invoiced"] == "true" or qs_checked["invoiced"] == "false":
                for time in obj.time_set.all():
                    if qs_checked["invoiced"] == "true":
                        time.invoiced = True
                    elif qs_checked["invoiced"] == "false":
                        time.invoiced = False
                    time.save()
                if qs_checked["invoiced"] == "true":
                    now = timezone.now()
                    obj.last_payment_date = now
                    messages.add_message(request, messages.INFO, "Paid!")
                    obj.save()
                elif qs_checked["invoiced"] == "false":
                    messages.add_message(request, messages.INFO, "Not paid!")
                    obj.last_payment_date = None
                    obj.save()
            elif qs_checked["active"] == "on" or qs_checked["active"] == "off":
                if model_name == "user":
                    if qs_checked["active"] == "on":
                        obj.profile.active = True
                    else:
                        obj.profile.active = False
                    obj.profile.save()
                else:
                    if qs_checked["active"] == "on":
                        obj.active = True
                    else:
                        obj.active = False
                    obj.save()
            elif qs_checked["subscribe"] == "on" or qs_checked["subscribe"] == "off":
                if qs_checked["subscribe"] == "on":
                    obj.subscribed = True
                else:
                    obj.subscribed = False
                obj.save()
            return HttpResponseRedirect(reverse(url_pattern))
        if form.is_valid():
            ################################################################
            # Set
            #
            # Assign field values from query string parameters, hours & income
            # calculations & other field values.
            #
            # E.g. Time entry invoice field set for member of project team.
            #
            ################################################################
            obj = form.save()
            if request.user.is_staff:  # Staff can see index
                url_pattern = "%s_view" % model_name
            else:
                url_pattern = "dashboard"
            if model_name == "invoice":
                if qs_project:
                    project = project_model.objects.get(pk=qs_project)
                    obj.client = project.client
                    obj.project = project
                    obj.save()
                if qs_client:
                    client = client_model.objects.get(pk=qs_client)
                    obj.client = client
                    obj.save()
                invoice = model.objects.get(pk=obj.pk)
                invoice = add_times(time_model, invoice)
            elif model_name == "report":
                if obj.invoices.all():
                    hours_report, gross, cost, net = agg_income(obj.invoices)
                    obj.hours = hours_report
                    obj.amount = gross
                    obj.cost = cost
                    obj.net = net
                    obj.save()
            elif model_name == "contact":
                if qs_client:
                    client = client_model.objects.get(pk=qs_client)
                    obj.client = client
                    obj.save()
            elif model_name == "note":
                if qs_client:
                    client = client_model.objects.get(pk=qs_client)
                    client.note.add(obj)
                    client.save()
                elif qs_invoice:
                    invoice = invoice_model.objects.get(pk=qs_invoice)
                    invoice.note.add(obj)
                    invoice.save()
                elif qs_project:
                    project = project_model.objects.get(pk=qs_project)
                    project.note.add(obj)
                    project.save()
                elif qs_account:
                    account = account_model.objects.get(pk=qs_account)
                    account.note.add(obj)
                    account.save()
                elif qs_user:
                    user = user_model.objects.get(id=qs_user)
                    user.profile.note.add(obj)
                    user.profile.save()
                elif qs_note:
                    note = note_model.objects.get(id=qs_note)
                    note.notes.add(obj)
                    note.save()
            elif model_name == "project":
                if qs_client:
                    client = client_model.objects.get(pk=qs_client)
                    obj.client = client
                    obj.save()
            elif model_name == "time":
                if not obj.user:
                    obj.user = request.user
                    obj.save()
                if qs_invoice:
                    invoice = invoice_model.objects.get(pk=qs_invoice)
                    obj.invoice = invoice
                    obj.save()
                if obj.invoice:
                    obj = add_times(time_model, obj.invoice, obj=obj)
                if new_time:
                    messages.add_message(request, messages.INFO, "Time entered!")
                    message = "%s/%s/edit" % ("https://aclark.net/db/time", obj.pk)
                    subject = "Time entered by %s" % request.user
                    send_mail(
                        subject,
                        message,
                        settings.MAIL_FROM,
                        [settings.MAIL_TO],
                        fail_silently=False,
                    )
            elif model_name == "task":
                qs_project = request.GET.get("project")
                if qs_project:
                    project = project_model.objects.get(pk=qs_project)
                    project.task = obj
                    project.save()
            if request.user.is_staff:
                if model_name == "user":
                    return HttpResponseRedirect(
                        reverse(url_pattern, kwargs={"pk": obj.user.pk})
                    )
                else:
                    return HttpResponseRedirect(
                        reverse(url_pattern, kwargs={"pk": obj.pk})
                    )
            else:
                return HttpResponseRedirect(reverse(url_pattern))
    context["doc_type"] = doc_type
    context["form"] = form
    context["item"] = obj
    context["model_name"] = model_name
    context["pk"] = pk
    return render(request, template_name, context)
