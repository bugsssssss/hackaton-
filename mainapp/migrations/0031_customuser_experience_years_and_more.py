# Generated by Django 4.2 on 2023-04-14 05:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0030_alter_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='experience_years',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='experience',
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('completed', 'Успешно'), ('pending', 'Ожидание'), ('canceled', 'Отменено')], default='pending', max_length=10),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(max_length=100)),
                ('from_year', models.IntegerField()),
                ('to_year', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='experience',
            field=models.ManyToManyField(blank=True, null=True, to='mainapp.experience'),
        ),
    ]
