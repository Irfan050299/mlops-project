from django.db import models

# Create your models here.

from django.db import models

class PredictionLog(models.Model):
    features = models.CharField(max_length=200)
    prediction = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.features} -> {self.prediction}"
