# Generated by Django 4.0.5 on 2022-08-08 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_workout', '0003_alter_part_description_alter_part_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
