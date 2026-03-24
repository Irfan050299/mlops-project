from django.db import models

class PredictionLog(models.Model):
    features = models.CharField(max_length=200)
    prediction = models.IntegerField()
    response_time_ms = models.FloatField(default=0)  # ✅ yeh add karo
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.features} -> {self.prediction}"

class ErrorLog(models.Model):  # ✅ yeh add karo
    error_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.error_message