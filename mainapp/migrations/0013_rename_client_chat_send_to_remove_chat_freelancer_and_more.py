# Generated by Django 4.2 on 2023-04-13 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_alter_chat_options_rename_send_to_chat_client_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='client',
            new_name='send_to',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='freelancer',
        ),
        migrations.AddField(
            model_name='chat',
            name='sender',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
