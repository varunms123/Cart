# Generated by Django 4.2.1 on 2023-07-04 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_review_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='product_name',
        ),
    ]
