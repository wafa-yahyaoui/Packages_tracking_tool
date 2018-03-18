# Create your tasks here
from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from celery import task
from .models import Order, OrderCSV
from ..accounts.models import StatusDelivery, Client, Courier, Member, Store
from django.conf import settings
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from celery.decorators import periodic_task
from .track_number.check_numbers import *

import json
import csv
import os




logger = get_task_logger(__name__)



@task
def create_orders_from_order_csv(path, owner_email, store_id, order_file_id):
    with open(os.path.join(settings.MEDIA_ROOT, path)) as csv_file:
        input_file = csv.DictReader(csv_file)
        for row in input_file:
            order = Order()
            order.store = Store.objects.get(id=store_id)
            order.tracking_id = row['Tracking_ID']
            order.file_csv = OrderCSV.objects.get(id=order_file_id)
            order.courier = Courier.objects.get(code=row['Courier'])
            order.source = row['Source']
            order.destination = row['Destination']
            order.owner = Member.objects.get(email=owner_email)
            # TODO: to change when status is fixed
            # order.status = StatusDelivery.objects.get(code='RTG')
            order.status = "Ready to go"
            try:
                logger.info("**************** test if client exists ***********************")
                client_instance = Client.objects.get(email=str(row['Client_Mail']))
            except ObjectDoesNotExist:
                logger.info("**************** creating a client    ***********************")
                client_instance = Client.objects.create(email=str(row['Client_Mail']),
                                                        first_name=str(row['Client_First_Name']),
                                                        last_name=str(row['Client_Last_Name']))
            order.client = client_instance
            order.save()

# A periodic task that will run every minute (the symbol "*" means every)
# @periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))


@periodic_task(run_every=timedelta(seconds=5))
def a():
    logger.info("Start task ----------------------------------")
    for store in Store.objects.all():
        for order in store.orders.values():
            order_info = track(order['tracking_id'])
            if order_info != 'Incorrect ID' and order["accept_test_flag"] == True:
                order["status"] = json.loads(order_info)["scan_event_list"][0]["status"]
                order["destination"] = json.loads(order_info)["scan_event_list"][0]["location"]

                logger.info("************    testing    *********************")
                logger.info("************    testing    *********************")
                order["courier"] = Courier.objects.get(code=json.loads(order_info)["shipper"])
                order["events_history"] = json.loads(order_info)["scan_event_list"]
                logger.info(order["events_history"])
                Order(**order).save()

            else:
                logger.info("************    Incorrect ID    *********************")
    logger.info("end of task ----------------------------------")
