# Generated by Django 4.1.5 on 2023-03-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='online_time',
        ),
        migrations.AlterField(
            model_name='account',
            name='register',
            field=models.TextField(blank=True, default='22:08:54, 23.03.2023', help_text='Дата и время регистрации'),
        ),
    ]
