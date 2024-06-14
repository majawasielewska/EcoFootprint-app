from django.db import models
from django.contrib.auth.models import User


class UserFootprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carbon_footprint_userfootprints')
    energy_consumption = models.FloatField(help_text="Energy consumption in kWh")
    energy_consumption_footprint = models.FloatField(help_text="Carbon footprint from energy consumption", default=0)
    meat_consumption = models.FloatField(help_text="Amount of meat consumed in kg")
    meat_consumption_footprint = models.FloatField(help_text="Carbon footprint from meat consumption", default=0)
    travel_distance = models.FloatField(help_text="Distance traveled by car in km")
    travel_distance_footprint = models.FloatField(help_text="Carbon footprint from travel distance", default=0)
    waste_production = models.FloatField(help_text="Waste produced in kg")
    waste_production_footprint = models.FloatField(help_text="Carbon footprint from waste production", default=0)
    total_footprint = models.FloatField(help_text="total Carbon footprint generated", default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserFootprintAggregation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carbon_footprint_userfootprints_aggregated')
    mean_energy_consumption_footprint = models.FloatField(help_text="weekly Carbon footprint from energy consumption",
                                                          default=0)
    mean_meat_consumption_footprint = models.FloatField(help_text="weekly Carbon footprint from meat consumption",
                                                        default=0)
    mean_travel_distance_footprint = models.FloatField(help_text="weekly Carbon footprint from travel distance",
                                                       default=0)
    mean_waste_production_footprint = models.FloatField(help_text="weekly Carbon footprint from waste production",
                                                        default=0)
    mean_total_footprint = models.FloatField(help_text="weekly total Carbon footprint generated", default=0)
    week = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
