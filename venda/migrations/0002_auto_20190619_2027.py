# Generated by Django 2.2.2 on 2019-06-19 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendaitem',
            name='preco',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Preço'),
        ),
    ]
