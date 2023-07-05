# Generated by Django 4.2.1 on 2023-07-04 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_review_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='email',
            field=models.EmailField(default=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='name',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviews',
            field=models.TextField(default=True, max_length=400),
        ),
    ]
