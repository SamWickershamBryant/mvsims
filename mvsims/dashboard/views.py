from django.shortcuts import render
from django.http import JsonResponse
from .models import Usages
from datetime import datetime

def index(request):
    all_usage = Usages.objects.all().values()
    context = {'usages':all_usage}
    return render(request, 'dashboard/dashboard.html', context)

def usages(request):
    all_usage = Usages.objects.all().values()
    usage_list = []

    for usage in all_usage:
        usage_dict = dict(usage)
        if 'ts' in usage_dict and isinstance(usage_dict['ts'], datetime):
            usage_dict['ts'] = usage_dict['ts'].isoformat()
        usage_list.append(usage_dict)

    return JsonResponse(usage_list, safe=False)