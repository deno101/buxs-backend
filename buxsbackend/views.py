from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from . import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
import datetime
import json
from django.conf import settings


def test(request):
    source = request.META.get('HTTP_X_FORWARDED_FOR')
    if not source:
        source = request.META.get('REMOTE_ADDR')

    port = request.get_port()
    return HttpResponse(f'sucess got request from {source} on port {port}')


@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')

        user = authenticate(username=username, password=password)
        try:
            login(request, user)
        except AttributeError as q:
            response_str = "{'code':400, 'error':'Invalid Credentials'}"
            return HttpResponse(json.dumps(eval(response_str)), content_type='json')

        response = render_to_response("auth.json", {
            'statuscode': 200,
        })

        max_age = 365 * 24 * 60 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie("username", username, max_age=max_age, expires=expires,
                            domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

        return response
    else:
        response_str = "{'code':400, 'error':'Invalid HTTP method'}"
        return HttpResponse(json.dumps(eval(response_str)), content_type='json')


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
            response_str = "{'code':400, 'error':'invalid form data'}"
            return HttpResponse(json.dumps(eval(response_str)), content_type='json')
    else:
        response_str = "{'code':400, 'error':'Wrong HTTP method'}"
        return HttpResponse(json.dumps(eval(response_str)), content_type='json')
