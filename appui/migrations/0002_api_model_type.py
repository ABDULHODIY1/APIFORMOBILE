# Generated by Django 5.0.7 on 2024-07-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appui', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_model',
            name='type',
            field=models.CharField(choices=[('Get', 'Get'), ('put', 'Put'), ('Delete', 'Delete'), ('Update', 'Update')], default='exit', max_length=20),
            preserve_default=False,
        ),
    ]
