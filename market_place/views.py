from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from . import forms, models
import json
from django.core.serializers.json import DjangoJSONEncoder


def get_mp(request):
    if request.method == 'GET':
        data = models.MarketPlaceProducts.objects.all()
        values = data.values()
        dic = {}
        for i in values:
            dic[i["id"]] = i

        # print(dic)

        data = json.dumps(dic, cls=DjangoJSONEncoder)
        return HttpResponse(data, content_type='json')
    else:
        return HttpResponseNotFound()


def get_img(request):
    path = request.GET.get('path')

    with open(f'img/{path}', 'rb') as f:
        data = f.read()

    return HttpResponse(data, content_type="image/jpeg")

