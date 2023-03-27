import requests
from django.shortcuts import render
from DesafioAlpha import settings
from django.contrib.auth.decorators import login_required

from DesafioAlpha.controllers import run_continuously
from asset import models as asset_models


@login_required
def home(request):
    if not settings.IS_RUNNING:
        run_continuously()
        settings.IS_RUNNING = True

    if request.method == 'GET':
        search = request.GET.get('search', '')

        if search:
            url = f'{settings.SEARCH_ALPHA}{search}'
        else:
            # Default search
            url = f'{settings.SEARCH_ALPHA}Meta'

        r = requests.get(url)
        data = r.json()['bestMatches']
        stocks = []

        for item in data:
            stocks.append({'symbol': item['1. symbol'], 'name': item['2. name']})

        context = {'stocks': stocks, 'search': search}
        return render(request, 'home.html', context)

    if request.method == 'POST':
        user = request.user
        selection = request.POST.getlist('selection')
        period = list(filter(lambda x:  len(x.strip()) > 0, request.POST.getlist('period')))
        bottom_tunnel = list(filter(lambda x:  len(x.strip()) > 0, request.POST.getlist('bottom_tunnel')))
        top_tunnel = list(filter(lambda x:  len(x.strip()) > 0, request.POST.getlist('top_tunnel')))

        for name in selection:
            asset = asset_models.Asset.objects.create(
                user=user,
                name=name,
                update_period=period,
                tunnel_top=top_tunnel,
                tunnel_bottom=bottom_tunnel
            )
            asset.update_asset()

        return render(request, 'home.html', {})

