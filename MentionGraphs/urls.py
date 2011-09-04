from django.conf.urls.defaults import patterns, include, url
import os
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import MentionGraphs.frontend.admin
import MentionGraphs.firehose.admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MentionGraphs.views.home', name='home'),
    # url(r'^MentionGraphs/', include('MentionGraphs.foo.urls')),
    url(r'^$', 'MentionGraphs.frontend.views.index', name='index'),
    url(r'^api$', 'MentionGraphs.frontend.views.api', name='api'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': os.path.join(os.path.dirname(__file__), 'static') }),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
