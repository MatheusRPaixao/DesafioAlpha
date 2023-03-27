import logging

import requests

from asset import models
from DesafioAlpha import settings


def update_asset(asset_id):
    """
    Update an asset with external information

    :param asset_id: ID for the asset to be updated
    """

    try:
        asset = models.Asset.objects.get(id=asset_id)
    except models.Asset.DoesNotExist:
        logging.error('Asset #{} does not exists.')
        return

    url = f'{settings.UPDATE_ALPHA}{asset.name}'
    data = requests.get(url).json()

    asset.highest_price = data.get('high', asset.highest_price)
    asset.lowest_price = data.get('low', asset.lowest_price)
    asset.current_price = data.get('price', asset.current_price)
    asset.save()


