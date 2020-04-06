from django.conf.urls import url
from api.views import slot_view, registration_view
from rest_framework.authtoken import views

app_name = 'api'

urlpatterns = [
    url(r'v1/users/register/?', registration_view.RegistrationView.as_view(), name='registration'),
    url(r'v1/slots/book/?', slot_view.BookSlotView.as_view(), name='slot'),
    url(r'v1/slots/?', slot_view.SlotView.as_view(), name='slot'),
    url(r'^api-token-auth/?', views.obtain_auth_token)
]