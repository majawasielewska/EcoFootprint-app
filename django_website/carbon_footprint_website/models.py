from django.db import models

class UserFootprint(models.Model):
    user_name = models.CharField(max_length=100)
    energy_consumption = models.FloatField(help_text="Energy consumption in kWh")
    meat_consumption = models.FloatField(help_text="Amount of meat consumed in kg per week")
    travel_distance = models.FloatField(help_text="Distance traveled by car in km per week")
    waste_production = models.FloatField(help_text="Waste produced in kg per week")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

