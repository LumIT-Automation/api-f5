from django.urls import include, path

urlpatterns = [
    path('', include('f5.urls')),
]
