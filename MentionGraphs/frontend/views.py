from django.shortcuts import render_to_response
from django.http import HttpResponse
from MentionGraphs.firehose.models import Datapoint, Keyword, Metric
import datetime
import json
import time
def index(request):
    return render_to_response('index.html', {})

from django import template
register = template.Library()
@register.filter
def epoch(value):
    try:
        return int(time.mktime(value.timetuple())*1000)
    except AttributeError:
        return ''

def api(request):
    for k,v in request.GET.items():
        if k == 'stream':
            q = v
        else:
            metric_name = k
            metric_value = v 
    
    keyword_model = Keyword.objects.filter(name=q)
    metric_model = Metric.objects.filter(name=metric_name, value=metric_value)
    dataset = Datapoint.objects.filter(keyword=keyword_model, metric=metric_model)
    
    print dataset
    response = []
    for item in dataset:
       entry={}
       entry[epoch(item.time)]=item.count
       response.append(entry)
    return HttpResponse(json.dumps(response), mimetype="application/json")
