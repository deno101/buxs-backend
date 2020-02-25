from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
