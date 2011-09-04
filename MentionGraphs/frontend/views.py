from django.shortcuts import render_to_response
from django.http import HttpResponse
from MentionGraphs.firehose.models import Datapoint
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
    params = request.GET
#    since = params['since']
#    until = params['until']
#    query = params['q']
    vmetric = params['metric']
    
#    import pdb;pdb.set_trace()
    dataset = Datapoint.objects.filter(
#	time__gte=since
#    ).filter(
#	time__lt=until
#    ).filter(
        metric.name=vmetric
    )
    response = []
    for item in dataset:
       entry={}
#       entry['DATE']=item.time.strftime('%d-%m-%Y')
#       entry['TIME']=item.time.strftime('%H:%M:%S')
#       entry['VOLUME']=item.value
       entry[epoch(item.time)]=item.count
       print(item.time.strftime('%Y'))
       response.append(entry)
    return HttpResponse(json.dumps(response), mimetype="application/json")
