# Generated by Django 5.1 on 2024-09-21 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FieldUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_type', models.CharField(max_length=255)),
                ('entity_id', models.IntegerField()),
                ('field_name', models.CharField(max_length=255)),
                ('field_value', models.FloatField()),
                ('update_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_name', models.CharField(max_length=255)),
                ('tool_capacity', models.IntegerField()),
                ('tool_offset', models.FloatField()),
                ('feedrate', models.IntegerField()),
                ('tool_in_use', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Axis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('axis_name', models.CharField(max_length=5)),
                ('max_acceleration', models.FloatField()),
                ('max_velocity', models.FloatField()),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machines.machine')),
            ],
        ),
    ]
