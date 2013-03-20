from django.views.generic.simple import direct_to_template
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    #url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^$', direct_to_template, { 'template': 'index.html' },),
)
