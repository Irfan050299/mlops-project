from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PredictionSerializer, PredictionLogSerializer
from .models import PredictionLog
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, 'iris_app', 'model.pkl')

print("Model Path:", model_path)  # debug ke liye

model = pickle.load(open(model_path, "rb"))
print(model)

class PredictView(APIView):

    def post(self, request):
        serializer = PredictionSerializer(data=request.data)

        if serializer.is_valid():
            features = serializer.validated_data['features']

            # prediction
            prediction = model.predict([features])[0]

            # save in DB
            log = PredictionLog.objects.create(
                features=str(features),
                prediction=int(prediction)
            )

            return Response({
                "prediction": int(prediction)
            })

        return Response(serializer.errors, status=400)


class PredictionHistoryView(APIView):

    def get(self, request):
        logs = PredictionLog.objects.all().order_by('-created_at')
        serializer = PredictionLogSerializer(logs, many=True)
        return Response(serializer.data)


