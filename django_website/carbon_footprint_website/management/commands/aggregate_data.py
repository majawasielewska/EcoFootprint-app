from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from django.db.models.functions import TruncWeek
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

from carbon_footprint_website.models import UserFootprint, UserFootprintAggregation


class Command(BaseCommand):
    help = "aggregate users' carbon footprint data"

    def handle(self, *args, **options):
        aggregation = (
            UserFootprint.objects
            .annotate(week=TruncWeek('date_created'))
            .values('user', 'week')
            .annotate(mean_energy_consumption_footprint=Avg('energy_consumption_footprint'))
            .annotate(mean_meat_consumption_footprint=Avg('meat_consumption_footprint'))
            .annotate(mean_travel_distance_footprint=Avg('travel_distance_footprint'))
            .annotate(mean_waste_production_footprint=Avg('waste_production_footprint'))
            .annotate(mean_total_footprint=Avg('total_footprint'))
        )
        today = timezone.localdate()
        one_week_ago = today - timedelta(days=7)
        print(one_week_ago)
        # data retention and inserting aggregation to DB
        objects_to_delete_ufa = UserFootprintAggregation.objects.exclude(date_created__week_day=0).exclude(
            date_created__lt=one_week_ago)
        objects_to_delete_ufa.delete()
        for entry in aggregation:
            UserFootprintAggregation.objects.create(
                user=User.objects.get(id=entry['user']),
                mean_energy_consumption_footprint=entry['mean_energy_consumption_footprint'],
                mean_meat_consumption_footprint=entry['mean_meat_consumption_footprint'],
                mean_travel_distance_footprint=entry['mean_travel_distance_footprint'],
                mean_waste_production_footprint=entry['mean_waste_production_footprint'],
                mean_total_footprint=entry['mean_total_footprint'],
                week=entry['week']
            )
        objects_to_delete_uf = UserFootprint.objects.filter(date_created__lt=one_week_ago)
        objects_to_delete_uf.delete()
        self.stdout.write(self.style.SUCCESS('Successfully aggregated data and saved the results'))
