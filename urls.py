from django.urls import path
from .views import PlaceholderModalView

urlpatterns = [
    path(
        "placeholders/",
        PlaceholderModalView.as_view(),
        name="placeholders-modal",
    )
]