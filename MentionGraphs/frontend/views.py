from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET
from filter_names import filters, streams

@require_GET
def index(request):
    context = {}
    context['filters'] = filters
    context['streams'] = streams
    return render_to_response('index.html',
     context, context_instance=RequestContext(request))

@require_GET
def api(request):
    return HttpResponse('Hello World')
