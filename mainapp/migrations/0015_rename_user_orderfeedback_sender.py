# Generated by Django 4.2 on 2023-04-13 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_order_freelancer_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderfeedback',
            old_name='user',
            new_name='sender',
        ),
    ]
