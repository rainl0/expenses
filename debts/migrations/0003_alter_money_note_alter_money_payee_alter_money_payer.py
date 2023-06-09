# Generated by Django 4.2 on 2023-04-20 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0002_alter_money_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='money',
            name='note',
            field=models.CharField(max_length=240),
        ),
        migrations.AlterField(
            model_name='money',
            name='payee',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='money',
            name='payer',
            field=models.CharField(max_length=100),
        ),
    ]
