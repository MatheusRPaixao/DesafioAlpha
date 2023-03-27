import requests
from django.shortcuts import render
from DesafioAlpha import settings
from django.contrib.auth.decorators import login_required

from DesafioAlpha.controllers import run_continuously


@login_required
def home(request):
    if not settings.IS_RUNNING:
        run_continuously()
        settings.IS_RUNNING = True

    if request.method == 'GET':
        search = request.GET.get('search')

        if search:
            url = f'{settings.SEARCH_ALPHA}{search}'
        else:
            # Default search
            url = f'{settings.SEARCH_ALPHA}Meta'

        r = requests.get(url)
        stocks = r.json()

        context = {'stocks': stocks, 'search': search}
        return render(request, 'home.html', context)

    # if request.method == 'POST':
