from django.db import models

class UserFootprint(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='accounts_userfootprints')
    energy_consumption = models.FloatField()
    meat_consumption = models.FloatField()
    travel_distance = models.FloatField()
    waste_production = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Footprint"
