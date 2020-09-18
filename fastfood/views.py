import time
from django.contrib.auth import login, authenticate, logout

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect

# Create your views here.
from fastfood import models, forms
from market_place.image_compression import Compression
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.forms.models import model_to_dict
import json
from buxsbackend.forms import Login


def queryset_to_dict(queryset):
    dic = {}
    for x in queryset:
        dic[x['id']] = x

    return dic


def upload_data(request):
    if not request.user.is_authenticated:
        return render(request, 'FFupload.html', {
            'error_msg': ' you are not logged in; login first'
        })

    if request.method == 'POST':
        form = forms.FoodUpload(request.POST, request.FILES)

        if form.is_valid():
            db_inst = models.FastFoodProducts.objects.create()
            db_inst.save()
            product_id = str(db_inst.id)

            db_inst.name = form.cleaned_data.get('name')
            db_inst.price = form.cleaned_data.get('price')
            db_inst.category = form.cleaned_data.get('category')
            db_inst.date_epoch = time.time()
            db_inst.delivery_time = form.cleaned_data.get("delivery_time")

            origin1 = product_id + "-1." + request.FILES['img1'].name.split('.')[-1]
            print(origin1)
            db_inst.image_url1 = product_id + "-1." + 'jpg'
            Compression(origin=origin1, destination=db_inst.image_url1, data=request.FILES['img1'],
                        const=Compression.FASTFOOD).compress()

            origin2 = product_id + "-2." + request.FILES['img2'].name.split('.')[-1]
            db_inst.image_url2 = product_id + "-2." + 'jpg'
            Compression(origin=origin2, destination=db_inst.image_url2, data=request.FILES['img2'],
                        const=Compression.FASTFOOD).compress()

            origin3 = product_id + "-3." + request.FILES['img3'].name.split('.')[-1]
            db_inst.image_url3 = product_id + "-3." + 'jpg'
            Compression(origin=origin3, destination=db_inst.image_url3, data=request.FILES['img3'],
                        const=Compression.FASTFOOD).compress()

            db_inst.description = form.cleaned_data.get('description')

            db_inst.save()

            return render(request, 'FFupload.html', {
                'error_msg': 'Successsssssssssss'
            })
    else:
        return render(request, 'FFupload.html')


def get_img(request):
    path = request.GET.get('path')

    with open(f'img/fastfood/compressed/{path}', 'rb') as f:
        data = f.read()

    return HttpResponse(data, content_type="image/jpeg")


def get_product_by_id(request, pid):
    if request.method == 'GET':
        product_id = int(pid)

        data = models.FastFoodProducts.objects.get(id=product_id)
        print(data)
        data_dict = model_to_dict(data)

        return HttpResponse(json.dumps(data_dict), content_type=json)
    else:
        return HttpResponseBadRequest()


def get_product(request):
    if request.method == 'GET':
        data = models.FastFoodProducts.objects.all().values('id', 'name', 'price', 'image_url1')

        dic = queryset_to_dict(data)
        data = json.dumps(dic, cls=DjangoJSONEncoder)

        response = HttpResponse(data, content_type='json')
        return response
    else:
        return HttpResponseNotFound()


def log_in(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = Login(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get("password")

                user = authenticate(username=username, password=password)
                try:
                    login(request, user)
                except AttributeError as q:
                    return render(request, 'login.html', {
                        'error': 'invalid credentials'
                    })

                return redirect('upload_data_fastfood')
            else:
                return render(request, 'MPPupload.html', {
                    'error_msg': 'invalid form',
                    'form': form
                })

        else:
            redirect('upload')
    else:
        return render(request, 'login.html')
