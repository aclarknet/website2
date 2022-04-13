from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from aclarknet import views as aclarknet_views
from db import urls as db_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("about/", aclarknet_views.about, name="about"),
    path("team/", aclarknet_views.team, name="team"),
    path("clients/", aclarknet_views.clients, name="clients"),
    path("contact/", aclarknet_views.contact, name="contact"),
    path("careers/", aclarknet_views.careers, name="careers"),
    path("services/", aclarknet_views.services, name="services"),
    path("db/", include(db_urls)),
    # path("", include("social_django.urls", namespace="social")),
    path("accounts/", include("allauth.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
