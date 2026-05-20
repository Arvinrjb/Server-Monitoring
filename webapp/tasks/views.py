from django.shortcuts import render
from django.http import HttpResponse, Http404
import datetime
import psutil


def notfound():
    raise Http404('Page dose not exist')


async def current_datetime(request):
    now = datetime.datetime.now()
    html = f'<html lang="en"><body>It is now {now}.</body></html>'
    return HttpResponse(html)


async def cpu_usage(request):
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_count = psutil.cpu_count(logical=True)
    data = {
        "cpu_percent":cpu_percent,
        "cpu_count":cpu_count
    }
    return render(request, 'cpu_info.html',data)



