import logging

import requests
from django.shortcuts import render, redirect
from DesafioAlpha import settings
from django.contrib.auth.decorators import login_required

from DesafioAlpha.controllers import run_continuously
from asset import models as asset_models


@login_required
def home_view(request):
    if not settings.IS_RUNNING:
        run_continuously()
        settings.IS_RUNNING = True

    if request.method == 'GET':
        return search_stock_view(request)


@login_required
def search_stock_view(request):
    context = {}
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

        for count, item in enumerate(data):
            stocks.append({'symbol': item['1. symbol'], 'name': item['2. name'], 'id': count})

        context = {'stocks': stocks, 'search': search}

    return render(request, 'home.html', context)


@login_required
def update_stock_observer(request):
    if request.method != 'POST':
        return redirect('home')

    user = request.user
    name = request.POST.get('name')
    symbol = request.POST.get('symbol')
    period = request.POST.get('period')
    bottom_tunnel = request.POST.get('bottom_tunnel')
    top_tunnel = request.POST.get('top_tunnel')

    values = [name, symbol, period, bottom_tunnel, top_tunnel]

    has_invalid_value = len(list(filter(lambda x: x is None or x == '', values))) > 0

    if has_invalid_value:
        return redirect('home')

    is_new_asset = False

    # Get or create for avoid multiple assets for same stock
    try:
        asset = asset_models.Asset.objects.get(
            user=user,
            name=name,
            symbol=symbol
        )

        asset.update_period = int(period)
        asset.tunnel_top = float(top_tunnel)
        asset.tunnel_bottom = float(bottom_tunnel)
        asset.save()

    except asset_models.Asset.DoesNotExist:
        asset = asset_models.Asset.objects.create(
            user=user,
            name=name,
            symbol=symbol,
            update_period=int(period),
            tunnel_top=float(top_tunnel),
            tunnel_bottom=float(bottom_tunnel)
        )
        is_new_asset = True

    asset.update_asset()

    if is_new_asset:
        logging.info('Stock #{} observer created'.format(asset.id))
    else:
        logging.info('Stock #{} observer update with new inputs'.format(asset.id))

    return redirect('home')


@login_required()
def get_user_assets(request):
    if request.method != 'GET':
        return render(request, 'my_assets.html', {'status': 'Fail', 'message': 'Endpoint must receive a GET request.'})

    assets = asset_models.Asset.objects.filter(user=request.user).order_by('name')
    return render(request, 'my_assets.html', {'assets': assets})
