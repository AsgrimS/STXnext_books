# Generated by Django 3.0.9 on 2020-08-05 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.TextField(null=True),
        ),
    ]
