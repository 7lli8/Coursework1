# Generated by Django 5.0.4 on 2024-05-13 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=120, unique=True, verbose_name='Email'),
        ),
    ]