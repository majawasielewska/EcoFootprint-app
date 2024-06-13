# from django.db import models

# class UserFootprint(models.Model):
#     user_name = models.CharField(max_length=100)
#     energy_consumption = models.FloatField(help_text="Energy consumption in kWh")
#     meat_consumption = models.FloatField(help_text="Amount of meat consumed in kg per week")
#     travel_distance = models.FloatField(help_text="Distance traveled by car in km per week")
#     waste_production = models.FloatField(help_text="Waste produced in kg per week")
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user_name

from django.db import models
from django.contrib.auth.models import User

class UserFootprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carbon_footprint_userfootprints')
    energy_consumption = models.FloatField(help_text="Energy consumption in kWh per week")
    meat_consumption = models.FloatField(help_text="Amount of meat consumed in kg per week")
    travel_distance = models.FloatField(help_text="Distance traveled by car in km per week")
    waste_production = models.FloatField(help_text="Waste produced in kg per week")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



