# Generated by Django 4.2 on 2023-04-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_customuser_service_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='published'),
        ),
    ]