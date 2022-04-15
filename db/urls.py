from django.urls import include, path, re_path

from . import views
from .views import project as project_views

urlpatterns = [
    path("account", views.account_index, name="account_index"),
    path("account/add", views.account_edit, name="account_edit"),
    re_path("^account/(?P<pk>\d+)$", views.account_view, name="account_view"),
    re_path("^account/(?P<pk>\d+)/edit$", views.account_edit, name="account_edit"),
    re_path("^account/(?P<pk>\d+)/delete$", views.account_view, name="account_delete"),
    re_path("^account/(?P<pk>\d+)/copy$", views.account_view, name="account_copy"),
    path("auth/", include("django.contrib.auth.urls")),
    path("client", views.client_index, name="client_index"),
    path("client/add", views.client_edit, name="client_edit"),
    re_path("^client/(?P<pk>\d+)$", views.client_view, name="client_view"),
    re_path("^client/(?P<pk>\d+)/edit$", views.client_edit, name="client_edit"),
    re_path("^client/(?P<pk>\d+)/delete$", views.client_view, name="client_delete"),
    re_path("^client/(?P<pk>\d+)/copy$", views.client_view, name="client_copy"),
    path("company", views.company_index, name="company_index"),
    path("company/add", views.company_edit, name="company_edit"),
    re_path("^company/(?P<pk>\d+)$", views.company_view, name="company_view"),
    re_path("^company/(?P<pk>\d+)/edit$", views.company_edit, name="company_edit"),
    re_path("^company/(?P<pk>\d+)/delete$", views.company_view, name="company_delete"),
    re_path("^company/(?P<pk>\d+)/copy$", views.company_view, name="company_copy"),
    path("contact", views.contact_index, name="contact_index"),
    path("contact/add", views.contact_edit, name="contact_edit"),
    re_path("^contact/(?P<pk>\d+)$", views.contact_view, name="contact_view"),
    re_path("^contact/(?P<pk>\d+)/edit$", views.contact_edit, name="contact_edit"),
    re_path("^contact/(?P<pk>\d+)/delete$", views.contact_view, name="contact_delete"),
    re_path("^contact/(?P<pk>\d+)/copy$", views.contact_view, name="contact_copy"),
    path("", views.home, name="dashboard"),
    # path("doc", views.doc, name="doc"),
    path("500", views.error, name="error"),
    path("invoice", views.invoice_index, name="invoice_index"),
    path("invoice/add", views.invoice_edit, name="invoice_edit"),
    re_path("^invoice/(?P<pk>\d+)$", views.invoice_view, name="invoice_view"),
    re_path("^invoice/(?P<pk>\d+)/edit$", views.invoice_edit, name="invoice_edit"),
    re_path("^invoice/(?P<pk>\d+)/delete$", views.invoice_view, name="invoice_delete"),
    re_path("^invoice/(?P<pk>\d+)/copy$", views.invoice_view, name="invoice_copy"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("lounge", views.lounge, name="lounge"),
    path("note", views.note_index, name="note_index"),
    path("note/add", views.note_edit, name="note_edit"),
    re_path("^note/(?P<pk>\d+)$", views.note_view, name="note_view"),
    re_path("^note/(?P<pk>\d+)/edit$", views.note_edit, name="note_edit"),
    re_path("^note/(?P<pk>\d+)/delete$", views.note_view, name="note_delete"),
    re_path("^note/(?P<pk>\d+)/copy$", views.note_view, name="note_copy"),
    path("project", project_views.project_index, name="project_index"),
    path("project/add", project_views.project_edit, name="project_edit"),
    re_path("^project/(?P<pk>\d+)$", project_views.project_view, name="project_view"),
    re_path(
        "^project/(?P<pk>\d+)/edit$", project_views.project_edit, name="project_edit"
    ),
    re_path(
        "^project/(?P<pk>\d+)/delete$",
        project_views.project_view,
        name="project_delete",
    ),
    re_path(
        "^project/(?P<pk>\d+)/copy$", project_views.project_view, name="project_copy"
    ),
    path("report", views.report_index, name="report_index"),
    path("report/add", views.report_edit, name="report_edit"),
    re_path("^report/(?P<pk>\d+)$", views.report_view, name="report_view"),
    re_path("^report/(?P<pk>\d+)/edit$", views.report_edit, name="report_edit"),
    re_path("^report/(?P<pk>\d+)/delete$", views.report_view, name="report_delete"),
    re_path("^report/(?P<pk>\d+)/copy$", views.report_view, name="report_copy"),
    path("search", views.search_index, name="search_index"),
    path("task", views.task_index, name="task_index"),
    path("task/add", views.task_edit, name="task_edit"),
    re_path("^task/(?P<pk>\d+)$", views.task_view, name="task_view"),
    re_path("^task/(?P<pk>\d+)/edit$", views.task_edit, name="task_edit"),
    re_path("^task/(?P<pk>\d+)/delete$", views.task_view, name="task_delete"),
    re_path("^task/(?P<pk>\d+)/copy$", views.task_view, name="task_copy"),
    path("time", views.time_index, name="time_index"),
    path("time/add", views.time_edit, name="time_edit"),
    re_path("^time/(?P<pk>\d+)$", views.time_view, name="time_view"),
    re_path("^time/(?P<pk>\d+)/edit$", views.time_edit, name="time_edit"),
    re_path("^time/(?P<pk>\d+)/delete$", views.time_view, name="time_delete"),
    re_path("^time/(?P<pk>\d+)/copy$", views.time_view, name="time_copy"),
    path("user", views.user_index, name="user_index"),
    path("user/add", views.user_edit, name="user_edit"),
    re_path("^user/(?P<pk>\d+)$", views.user_view, name="user_view"),
    re_path("^user/(?P<pk>\d+)/edit$", views.user_edit, name="user_edit"),
    re_path("^user/(?P<pk>\d+)/delete$", views.user_view, name="user_delete"),
    re_path("^user/(?P<pk>\d+)/copy$", views.user_view, name="user_copy"),
]

# expenses
urlpatterns = urlpatterns + [
    path("expense", views.expense_index, name="expense_index"),
    path("expense/add", views.expense_edit, name="expense_edit"),
    re_path("^expense/(?P<pk>\d+)$", views.expense_view, name="expense_view"),
    re_path("^expense/(?P<pk>\d+)/edit$", views.expense_edit, name="expense_edit"),
    re_path("^expense/(?P<pk>\d+)/delete$", views.expense_view, name="expense_delete"),
    re_path("^expense/(?P<pk>\d+)/copy$", views.expense_view, name="expense_copy"),
]

# CBVs
urlpatterns = urlpatterns + [
    path("client-list/", views.client.ClientListView.as_view(), name="client-list")
]
