from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('registration.urls')),
    url(r'', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
