# Generated by Django 4.2.4 on 2023-08-17 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tender',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
