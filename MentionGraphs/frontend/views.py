from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET

@require_GET
def index(request):
    context = {}
    return render_to_response('index.html',
     context, context_instance=RequestContext(request))

def api(request):
    return HttpResponse('Hello World')
