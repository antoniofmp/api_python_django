from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('', admin.site.urls),
    path('api/insertSequence', views.APISequenceView.insertSequence),
    path('api/getSequence/<int:uid>/', views.APISequenceView.getSequence),
    path('api/findSequence', views.APISequenceView.findSequence),
    path('api/overlapSequence', views.APISequenceView.overlapSequence),
]
