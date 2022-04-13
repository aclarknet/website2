import django_tables2

from ..models import Client


class ClientTable(django_tables2.Table):
    class Meta:
        model = Client
        fields = ("name", "active", "publish")
        attrs = {"class": "table table-light text-dark"}


class ClientTableDark(django_tables2.Table):
    class Meta:
        model = Client
        fields = ("name", "active", "publish")
        attrs = {"class": "table table-dark text-light"}


class ClientListView(django_tables2.SingleTableView):
    model = Client
    template_name = "client_table.html"
    table_class = ClientTable

    # https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["model_name"] = "client"
        return context

    # https://stackoverflow.com/a/11448882
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.dark:
            self.table_class = ClientTableDark
        return super(ClientListView, self).dispatch(request, *args, **kwargs)
