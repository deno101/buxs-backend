from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import forms, models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
import json
from django.core.serializers.json import DjangoJSONEncoder

def test(request):
    source = request.META.get('HTTP_X_FORWARDED_FOR')
    if not source:
        source = request.META.get('REMOTE_ADDR')

    port = request.get_port()
    return HttpResponse(f'sucess got request from {source} on port {port}')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        password = request.POST.get('Password')
        username = request.POST.get('Username')

        return HttpResponse(f'Your credentials are {password}, {username}')
    else:
        return HttpResponse(f'Request method {request.method}')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # hash the plain text password
            user.password = make_password(request.POST.get('password'))
            user.save()
            return render(request, 'auth.json', {
                'source': '/signup',
                'statuscode': 200,
            })
        else:
            print('error form not valid')
            print(form)
    else:
        return render(request, 'auth.json', {
            'source': '/signup',
            'statuscode': 200,
        })

def get_mp(request):
    if request.method == 'GET':
        data = models.MarketPlaceProducts.objects.all()
        values = data.values()
        dic = {}
        for i in values:
            dic[i["id"]] = i

        print(dic)

        data = json.dumps(dic, cls=DjangoJSONEncoder)
        return HttpResponse(data, content_type='json')
    else:
        return HttpResponseNotFound()
