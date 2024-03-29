# Generated by Django 4.2 on 2023-04-13 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_alter_message_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='send_to',
            new_name='client',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='sender',
        ),
        migrations.AddField(
            model_name='chat',
            name='freelancer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='freelancer', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
