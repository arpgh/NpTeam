import datetime

from django.http import HttpResponse
from django.core.serializers import serialize

def fetch(request):
    if request.GET:
        ret_val = request.GET.get("echoValue")
        print ret_val
        return HttpResponse(datetime.datetime.now())
