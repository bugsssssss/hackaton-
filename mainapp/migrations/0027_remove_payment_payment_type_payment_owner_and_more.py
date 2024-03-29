# Generated by Django 4.2 on 2023-04-14 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0026_remove_customuser_wallet_wallet_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_type',
        ),
        migrations.AddField(
            model_name='payment',
            name='owner',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(choices=[('usd', 'USD'), ('eur', 'EUR'), ('rub', 'RUB'), ('uzs', 'UZS')], default='uzs', max_length=3),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.order'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('fixed', 'Фиксированная'), ('hourly', 'Почасовая')], default='pending', max_length=10),
        ),
    ]
