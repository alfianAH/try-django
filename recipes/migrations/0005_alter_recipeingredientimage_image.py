# Generated by Django 3.2.8 on 2022-02-08 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipeingredientimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredientimage',
            name='image',
            field=models.ImageField(upload_to='recipes/'),
        ),
    ]
