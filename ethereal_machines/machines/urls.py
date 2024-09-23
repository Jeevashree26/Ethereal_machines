from django.urls import path
from .views import MachineListCreateView, MachineRetrieveUpdateView, MachineHistoryView

urlpatterns = [
    path('', MachineListCreateView.as_view(), name='machine-list-create'),
    path('<int:pk>/', MachineRetrieveUpdateView.as_view(), name='machine-retrieve-update'),
    path('<int:machine_id>/history/<str:axis_name>/', MachineHistoryView.as_view(), name='machine-history'),
]