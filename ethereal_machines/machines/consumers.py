import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import FieldUpdate

class MachineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'machines_real_time'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        field_updates = FieldUpdate.objects.filter(update_time__gte=timezone.now() - timezone.timedelta(minutes=15))
        updates_json = json.dumps([{
            'entity_type': update.entity_type,
            'field_name': update.field_name,
            'field_value': update.field_value
        } for update in field_updates])
        await self.send(text_data=updates_json)
