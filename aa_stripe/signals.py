# -*- coding: utf-8 -*-
import django.dispatch

stripe_charge_succeeded = django.dispatch.Signal(providing_args=["instance"])