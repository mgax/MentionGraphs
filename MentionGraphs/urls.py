from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import MentionGraphs.frontend.admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MentionGraphs.views.home', name='home'),
    # url(r'^MentionGraphs/', include('MentionGraphs.foo.urls')),

    url(r'^$', 'MentionGraphs.frontend.views.index', name='index'),

    url(r'^api$', 'MentionGraphs.frontend.views.api', name='api'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
