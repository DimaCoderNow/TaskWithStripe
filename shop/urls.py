from django.urls import path
from shop import views


urlpatterns = [
    path('', views.index, name="index"),
    path('item/<int:item_id>', views.show_item, name="show_item"),
    path('buy/<int:item_id>', views.get_session_id, name="get_session"),
]