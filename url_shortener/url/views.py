from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import uuid
import validators

from .models import URL



def url_view(request):

    if request.method == 'POST': 
        long_url = request.POST.get('long_url')

        if not check_url_format(long_url):
            context = {'error message': 'Url non valide'}
            return render(request, 'url/home.html',context)
        
        if check_long_url_exist(long_url):
            return handle_existing_url(request, long_url)
        else:
            return handle_new_url(request, long_url)
     
    return render(request, 'url/home.html')




def handle_existing_url(request, long_url):
    queryset = get_url(long_url)
    context = {
        'short_url': queryset.short_url,
        'message': 'URL déjà raccourcie'
    }
    return render(request, 'url/home.html', context)



def handle_new_url(request, long_url):
    new_url = generate_short_url(long_url)
    context = {
        'new_url': new_url,
        'message': 'URL raccourcie avec succès !'
    }
    return render(request, 'url/home.html', context)



def redirect_view(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    return redirect(url.long_url)


def generate_short_url(long_url):
    new_domain = uuid.uuid4().hex[:10]
    new_url = create_new_url(long_url, f"{new_domain}")
    return new_url.short_url


def check_url_format(url):
    return validators.url(url)


def check_long_url_exist(url): 
    return URL.objects.filter(long_url=url).exists()


def get_url(url):
    return URL.objects.get(long_url=url)


def create_new_url(long_url, short_url):
    new_url = URL.objects.create(long_url=long_url,
                                 short_url=short_url)
    return new_url
