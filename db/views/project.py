from django.contrib.admin.views.decorators import staff_member_required

# from django.contrib.auth.models import User
from django.shortcuts import render

from project.models import User

from ..context import get_context
from ..forms import ProjectForm
from ..models import (
    Account,
    Client,
    Company,
    Contact,
    Invoice,
    Note,
    Project,
    Report,
    Task,
    Time,
    # User,
)


@staff_member_required
def project_view(request, pk=None):
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
        model=Project,
        invoice_model=Invoice,
        order_by={
            "project": (),
            "time": ("-active", "-date"),
            "invoice": ("-issue_date",),
        },
        pk=pk,
        project_model=Project,
        task_model=Task,
    )
    return render(request, "project_view.html", context)


@staff_member_required
def project_edit(request, pk=None):
    return get_context(
        request,
        report_model=Report,
        user_model=User,
        time_model=Time,
        note_model=Note,
        contact_model=Contact,
        company_model=Company,
        account_model=Account,
        form_model=ProjectForm,
        model=Project,
        client_model=Client,
        invoice_model=Invoice,
        project_model=Project,
        pk=pk,
        context_type="edit",
        task_model=Task,
    )


@staff_member_required
def project_index(request, pk=None):
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
        model=Project,
        order_by={"project": ("-active", "name")},
        project_model=Project,
        task_model=Task,
    )
    return render(request, "project_index.html", context)
