from django.urls import path
from .views import NewContactAPIView, ContactListingAPIView, ContactCountClientAPIView, ContactCountContactAPIView,ContactSingleAPIView
 
urlpatterns = [
    path('create', NewContactAPIView.as_view()),
    path('list', ContactListingAPIView.as_view({'get': 'list'})),
    path('countclient', ContactCountClientAPIView.as_view()),
    path('countcontact', ContactCountContactAPIView.as_view()),
    path('<int:id>', ContactSingleAPIView.as_view()),
]
