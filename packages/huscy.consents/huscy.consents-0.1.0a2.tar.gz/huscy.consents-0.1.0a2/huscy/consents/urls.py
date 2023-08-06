from django.urls import path
from huscy.consents import views

urlpatterns = [
    path('', views.CreateConsentView.as_view(), name="create-consent"),
    path('<int:consent_id>', views.SignConsentView.as_view(), name="sign-consent"),
]
