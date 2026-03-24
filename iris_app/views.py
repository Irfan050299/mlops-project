from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PredictionSerializer, PredictionLogSerializer
from .models import PredictionLog
import pickle
import os
import numpy as np
import time  # ✅ 1. yeh add karo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'iris_app', 'model.pkl')
print("Model Path:", model_path)
model = pickle.load(open(model_path, "rb"))
print("Model Loaded:", model)


class PredictView(APIView):

    def get(self, request):
        return Response({
            "message": "API is working 🚀. Use POST method with features."
        })

    def post(self, request):
        start_time = time.time()  # ✅ 2. yeh add karo
        try:
            serializer = PredictionSerializer(data=request.data)

            if serializer.is_valid():
                features = serializer.validated_data['features']

                if not features or len(features) != 4:
                    return Response({
                        "error": "Exactly 4 features required"
                    }, status=400)

                features = list(map(float, features))
                prediction = model.predict([features])[0]
                response_time = round((time.time() - start_time) * 1000, 2)  # ✅ 3. yeh add karo

                PredictionLog.objects.create(
                    features=str(features),
                    prediction=int(prediction),
                    response_time_ms=response_time  # ✅ 4. yeh add karo
                )

                return Response({
                    "prediction": int(prediction),
                    "response_time_ms": response_time  # ✅ 5. yeh add karo
                })

            return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class PredictionHistoryView(APIView):

    def get(self, request):
        try:
            logs = PredictionLog.objects.all().order_by('-created_at')
            serializer = PredictionLogSerializer(logs, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
