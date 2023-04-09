import logging
import math
from datetime import timedelta

import requests
import schedule

from django.db import models
from django.contrib.auth.models import User

from DesafioAlpha.controllers import send_email_tunnel_breach
from DesafioAlpha import settings


class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')

    # Name of the asset
    symbol = models.CharField(max_length=40)
    name = models.CharField(max_length=256)

    # Price
    current_price = models.FloatField(default=0)
    lowest_price = models.FloatField(null=True)
    highest_price = models.FloatField(null=True)

    # Update time period
    update_period = models.IntegerField()

    # Tunnel variables
    tunnel_top = models.FloatField(default=0)
    tunnel_bottom = models.FloatField(default=0)

    # Asset flags
    schedule_running = models.BooleanField(default=False)
    top_breach = models.BooleanField(default=False)
    bottom_breach = models.BooleanField(default=False)

    def save(self, **kwargs):
        if not self.update_period:
            raise Exception('Period for the asset update must be valid.')

        if not self.schedule_running:
            # Create schedule for new asset
            minutes = math.floor(timedelta(minutes=int(self.update_period)).total_seconds() / 60)
            schedule.every(minutes).minutes.do(self.update_asset, self).tag(self.get_schedule_token())
            self.schedule_running = True

        if self.id:
            # Logic to send e-mails
            if self.current_price >= self.tunnel_top:
                # Check if top value has already been reached before, if not, send the e-mail.
                # Avoiding multiple e-mails for the current breach
                if not self.top_breach:
                    send_email_tunnel_breach(self.user, self.name, True)
                    self.top_breach = True
            else:
                self.top_breach = False

            if self.current_price <= self.tunnel_bottom:
                if not self.bottom_breach:
                    send_email_tunnel_breach(self.user, self.name, False)
                    self.tunnel_bottom = True
            else:
                self.bottom_breach = False

        return super().save(**kwargs)

    def delete(self, **kwargs):
        # Remove schedule for the deleted asset
        schedule.clear(self.get_schedule_token())

        return super().delete(self, **kwargs)

    def update_asset(self):
        """
        Update an asset with external information
        """

        url = f'{settings.UPDATE_ALPHA}{self.name}'
        data = requests.get(url).json()

        self.highest_price = data.get('high', self.highest_price)
        self.lowest_price = data.get('low', self.lowest_price)
        self.current_price = data.get('price', self.current_price)
        self.save()

    def get_schedule_token(self):
        return f'{self.user_id}-{self.symbol}'

