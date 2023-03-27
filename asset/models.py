import math

import schedule
from django.db import models
from django.contrib.auth.models import User

from DesafioAlpha.controllers import update_asset, send_email_tunnel_breach


class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')

    # Name of the asset, every asset must be one unique name
    name = models.CharField(max_length=40, unique=True)

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
            schedule.every().minutes(self.update_period).do(update_asset, self.id).tag(self.id)
            self.schedule_running = True

        # Logic to send e-mails
        if self.current_price >= self.tunnel_top:
            # Check if top value has already been reached before, if not, send the e-mail.
            # Avoiding multiple e-mails for the current breach
            if not self.top_breach:
                send_email_tunnel_breach(self.user, True)
                self.top_breach = True
        else:
            self.top_breach = False

        if self.current_price <= self.tunnel_bottom:
            if not self.bottom_breach:
                send_email_tunnel_breach(self.user, False)
                self.tunnel_bottom = True
        else:
            self.bottom_breach = False

        return super().save(self, **kwargs)

    def delete(self, **kwargs):
        # Remove schedule for the deleted asset
        schedule.clear(self.id)

        return super().delete(self, **kwargs)
