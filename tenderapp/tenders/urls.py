from django.urls import path
from .views import TenderListView, LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='home'),
    path('tenders/', TenderListView.as_view(), name='tender_list'),
]
