from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PredictionSerializer, PredictionLogSerializer
from .models import PredictionLog
import pickle
import os
import numpy as np

# 👉 Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 👉 Model path
model_path = os.path.join(BASE_DIR, 'iris_app', 'model.pkl')

print("Model Path:", model_path)

# 👉 Load model
model = pickle.load(open(model_path, "rb"))
print("Model Loaded:", model)


class PredictView(APIView):

    # ✅ GET (health check / browser test)
    def get(self, request):
        return Response({
            "message": "API is working 🚀. Use POST method with features."
        })

    # ✅ POST (main prediction)
    def post(self, request):
        try:
            serializer = PredictionSerializer(data=request.data)

            if serializer.is_valid():
                features = serializer.validated_data['features']

                # 👉 validation
                if not features or len(features) != 4:
                    return Response({
                        "error": "Exactly 4 features required"
                    }, status=400)

                # 👉 convert to float (safe)
                features = list(map(float, features))

                # 👉 prediction
                prediction = model.predict([features])[0]

                # 👉 save in DB
                PredictionLog.objects.create(
                    features=str(features),
                    prediction=int(prediction)
                )

                return Response({
                    "prediction": int(prediction)
                })

            return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)


class PredictionHistoryView(APIView):

    def get(self, request):
        try:
            logs = PredictionLog.objects.all().order_by('-created_at')
            serializer = PredictionLogSerializer(logs, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)

