from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET
from filter_names import filters, streams

from MentionGraphs.firehose.models import Datapoint, Keyword, Metric
import datetime
import json
import time

from django import template
register = template.Library()
@register.filter
def epoch(value):
    try:
        return int(time.mktime(value.timetuple())*1000)
    except AttributeError:
        return ''

@require_GET

def index(request):
    context = {}
    context['filters'] = filters
    context['streams'] = streams
    return render_to_response('index.html', context, context_instance=RequestContext(request))

from django import template
register = template.Library()
@register.filter
def epoch(value):
    try:
        return int(time.mktime(value.timetuple())*1000)
    except AttributeError:
        return ''

@require_GET
def api(request):
    try:
        metric_name = None
        metric_value = None
        for k,v in request.GET.items():
            if k == 'stream':
                q = v
            else:
                metric_name = k
                metric_value = v

        keyword_model = Keyword.objects.filter(name=q)
        if not metric_name == None and not metric_value == None:
            metric_model = Metric.objects.filter(name=metric_name, value=metric_value)
            dataset = Datapoint.objects.filter(keyword=keyword_model, metric=metric_model).order_by('time')
        else:
            dataset = Datapoint.objects.filter(keyword=keyword_model).order_by('time')

        response = []
        for item in dataset.reverse()[:24*30*3]:
            response.insert(0,[epoch(item.time), item.count])
        return HttpResponse(json.dumps(response), mimetype="application/json")
        
    except Exception, e:
        return HttpResponse(str(e))
