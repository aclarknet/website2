from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from db.models import Client

from .forms import ContactForm


def about(request):
    context = {}
    context["about_nav"] = True
    return render(request, "about.html", context)


def blog(request):
    return HttpResponseRedirect("https://blog.aclark.net")


def clients(request):
    context = {}
    clients_government = Client.objects.filter(
        tags__name__in=["government"], publish=True
    )
    clients_non_profit = Client.objects.filter(
        tags__name__in=["non-profit"], publish=True
    )
    clients_private_sector = Client.objects.filter(
        tags__name__in=["private-sector"], publish=True
    )
    clients_colleges_universities = Client.objects.filter(
        tags__name__in=["colleges-universities"], publish=True
    )
    context["clients_government"] = clients_government
    context["clients_non_profit"] = clients_non_profit
    context["clients_private_sector"] = clients_private_sector
    context["clients_colleges_universities"] = clients_colleges_universities
    context["clients_nav"] = True
    return render(request, "clients.html", context)


def contact(request):
    context = {}
    email_from = "aclark@aclark.net"
    msg = "Message sent"
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            company_name = form.cleaned_data["company_name"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            message = "\n\n".join(
                [first_name, last_name, company_name, message, sender]
            )
            recipients = [email_from]
            subject = "Contact Us"
            send_mail(subject, message, email_from, recipients)
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect("/")
    else:
        form = ContactForm()
    context["form"] = form
    context["contact_nav"] = True
    return render(request, "contact.html", context)


def team(request):
    context = {}
    context["about_nav"] = True
    return render(request, "team.html", context)


def careers(request):
    context = {}
    context["careers_nav"] = True
    return render(request, "careers.html", context)


def services(request):
    context = {}
    context["services_nav"] = True
    return render(request, "services.html", context)
