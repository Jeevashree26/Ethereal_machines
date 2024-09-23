from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Machine, Axis, FieldUpdate
from .serializers import MachineSerializer, AxisSerializer
from .permissions import IsSuperAdmin, IsManager, IsSupervisor, IsOperator
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class MachineListCreateView(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsSuperAdmin | IsManager]
        else:
            permission_classes = [IsAuthenticated, IsSuperAdmin | IsManager | IsSupervisor | IsOperator]
        return [permission() for permission in permission_classes]

class MachineRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            # Special logic for updating the 'tool_in_use' field
            if 'tool_in_use' in self.request.data:
                if self.request.user.role not in ['SUPERADMIN', 'Operator']:
                    raise PermissionDenied("Only SUPERADMIN and Operator can update 'tool_in_use'.")
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_update(self, serializer):
        # Special handling for 'tool_in_use' field
        if 'tool_in_use' in serializer.validated_data:
            if self.request.user.role == 'Operator':
                serializer.save()
            else:
                raise PermissionDenied("Only Operators can update 'tool_in_use'.")
        else:
            super().perform_update(serializer)
    
class MachineHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self, request, machine_id, axis_name):
        time_threshold =timezone.now() - timezone.timedelta(minutes=15)
        field_updates = FieldUpdate.objects.filter(
            entity_id=machine_id,
            field_name=[axis_name],
            update_time__gte=time_threshold
        )

        data = field_updates.values('field_name', 'field_value', 'update_time')
        return Response(data)