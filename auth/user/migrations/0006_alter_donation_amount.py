# Generated by Django 4.2.6 on 2023-11-05 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_childrenorphanage_visit_review_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
