from django.contrib import admin
from MentionGraphs.firehose.models import Keyword, Metric, Datapoint

admin.site.register(Keyword)
admin.site.register(Metric)
admin.site.register(Datapoint)
