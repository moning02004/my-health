# Generated by Django 4.0.5 on 2022-06-12 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userrole_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]