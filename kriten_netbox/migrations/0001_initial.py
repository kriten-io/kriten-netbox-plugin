# Generated by Django 5.0.7 on 2024-09-10 13:07

import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0115_convert_dashboard_widgets'),
    ]

    operations = [
        migrations.CreateModel(
            name='KritenCluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('kriten_url', models.CharField(max_length=100)),
                ('api_token', models.CharField(max_length=64)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='KritenRunner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('giturl', models.URLField()),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('secrets', models.JSONField(blank=True, default=dict, null=True)),
                ('kriten_cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runners', to='kriten_netbox.kritencluster')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='KritenTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100)),
                ('command', models.CharField(max_length=200)),
                ('schema', models.JSONField(blank=True, default=dict, null=True)),
                ('synchronous', models.BooleanField(blank=True, default=False)),
                ('kriten_cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='kriten_netbox.kritencluster')),
                ('runner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='kriten_netbox.kritenrunner')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('kriten_cluster', 'name'),
                'unique_together': {('kriten_cluster', 'name')},
            },
        ),
        migrations.CreateModel(
            name='KritenJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(blank=True, default='not_launched', max_length=100)),
                ('owner', models.CharField(blank=True, max_length=100, null=True)),
                ('extra_vars', models.JSONField(blank=True, default=dict, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('completion_time', models.DateTimeField(blank=True, null=True)),
                ('failed', models.SmallIntegerField(blank=True, default=0)),
                ('completed', models.SmallIntegerField(blank=True, default=0)),
                ('stdout', models.CharField(blank=True, max_length=50000, null=True)),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('kriten_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kritenjobs', to='kriten_netbox.kritentask')),
            ],
            options={
                'ordering': ('-start_time',),
                'unique_together': {('kriten_task', 'name')},
            },
        ),
    ]
