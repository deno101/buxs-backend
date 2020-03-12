from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import _thread
import time
from django.forms.models import model_to_dict

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
            db_inst.image_url1 = product_id + "-1." + request.FILES['img1'].name.split('.')[-1]

            # _thread.start_new_thread(savefile, (db_inst.image_url1, request.FILES['img1']))
            save_file(db_inst.image_url1, request.FILES['img1'])
            db_inst.image_url2 = product_id + "-2." + request.FILES['img2'].name.split('.')[-1]
            # _thread.start_new_thread(savefile, (db_inst.image_url2, request.FILES['img2']))

            save_file(db_inst.image_url2, request.FILES['img2'])
            db_inst.image_url3 = product_id + "-3." + request.FILES['img3'].name.split('.')[-1]
            # _thread.start_new_thread(savefile, (db_inst.image_url3, request.FILES['img3']))
            save_file(db_inst.image_url3, request.FILES['img3'])
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


def save_file(file_name, data):
    path = 'img/' + file_name
    with open(path, 'wb') as infile:
        for chunks in data.chunks():
            infile.write(chunks)


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
        print(data_dict)

        return HttpResponse(data_dict)
    else:
        return HttpResponse('{}')
