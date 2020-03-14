from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import time
from django.forms.models import model_to_dict

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound

from buxsbackend import settings
from . import forms, models, image_compression
import json
from django.core.serializers.json import DjangoJSONEncoder
import threading

from .image_compression import Compression


def get_mp(request):
    source = request.META.get('HTTP_X_FORWARDED_FOR')
    if not source:
        source = request.META.get('REMOTE_ADDR')

    if request.method == 'GET':
        data = models.MarketPlaceProducts.objects.all()
        values = data.values()
        dic = {}
        print(f' cookies -> {request.COOKIES}')
        try:
            for i in values:
                dic[i["id"]] = i
        except KeyError:
            pass
        data = json.dumps(dic, cls=DjangoJSONEncoder)

        response = HttpResponse(data, content_type='json')
        response.set_cookie("name", f'source -> {source}')
        return response
    else:
        return HttpResponseNotFound()


def get_img(request):
    path = request.GET.get('path')

    with open(f'img/compressed/{path}', 'rb') as f:
        data = f.read()

    return HttpResponse(data, content_type="image/jpeg")


def get_desc(request):
    pass


def upload_data(request):
    if not request.user.is_authenticated:
        return render(request, 'MPPupload.html', {
            'error_msg': ' you are not logged in; login first'
        })

    if request.method == 'POST':
        form = forms.ProductUploadForm(request.POST, request.FILES)

        if form.is_valid():
            db_inst = models.MarketPlaceProducts.objects.create(owner=request.user)
            db_inst.save()
            product_id = str(db_inst.id)

            db_inst.name = form.cleaned_data.get('name')
            db_inst.price = form.cleaned_data.get('price')
            db_inst.category = form.cleaned_data.get('category')
            db_inst.date_epoch = time.time()

            origin1 = product_id + "-1." + request.FILES['img1'].name.split('.')[-1]
            db_inst.image_url1 = product_id + "-1." + 'jpg'
            Compression(origin=origin1, destination=db_inst.image_url1, data=request.FILES['img1']).compress()

            origin2 = product_id + "-2." + request.FILES['img2'].name.split('.')[-1]
            db_inst.image_url2 = product_id + "-2." + 'jpg'
            Compression(origin=origin2, destination=db_inst.image_url2, data=request.FILES['img2']).compress()

            origin3 = product_id + "-3." + request.FILES['img3'].name.split('.')[-1]
            db_inst.image_url3 = product_id + "-3." + 'jpg'
            Compression(origin=origin3, destination=db_inst.image_url3, data=request.FILES['img3']).compress()

            db_inst.description = form.cleaned_data.get('description')
            db_inst.stock = form.cleaned_data.get('stock')
            db_inst.brand = form.cleaned_data.get('brand')

            db_inst.save()

            return render(request, 'MPPupload.html', {
                'error_msg': 'Successsssssssssss'
            })

        else:
            return render(request, 'MPPupload.html', {
                'error_msg': 'invalid form data'
            })
    else:
        return render(request, 'MPPupload.html')


def log_in(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = forms.Login(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get("password")

                user = authenticate(username=username, password=password)
                try:
                    login(request, user)
                except AttributeError:
                    return render(request, 'login.html', {
                        'error': 'invalid credentials'
                    })

                return redirect('uplaod')
            else:
                return render(request, 'MPPupload.html', {
                    'error_msg': 'invalid form',
                    'form': form
                })

        else:
            redirect('uplaod')
    else:
        return render(request, 'login.html')


def get_product_desc_by_id(request):
    if request.method == 'GET':
        pid = int(request.GET.get('pid'))

        data = models.MarketPlaceProducts.objects.get(id=pid)
        data_dict = model_to_dict(data)

        return HttpResponse(json.dumps(data_dict))
    else:
        return HttpResponse('{}')


