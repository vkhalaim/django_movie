# Generated by Django 3.1 on 2020-08-25 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='fees_in_world',
            field=models.PositiveIntegerField(default=0, help_text='in dollars', verbose_name='Fees in the World'),
        ),
    ]
