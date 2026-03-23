
from django.contrib import admin
from django.urls import path
from iris_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', views.PredictView.as_view()),
    path('history/', views.PredictionHistoryView.as_view()),
]
