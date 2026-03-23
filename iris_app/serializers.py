from rest_framework import serializers
from .models import PredictionLog

class PredictionSerializer(serializers.Serializer):
    features = serializers.ListField(
        child=serializers.FloatField(),
        min_length=4,
        max_length=4
    )


class PredictionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionLog
        fields = '__all__'