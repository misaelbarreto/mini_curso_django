# Generated by Django 2.2.2 on 2019-06-19 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_auto_20190619_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoque',
            name='tipo_movimentacao',
            field=models.CharField(choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída'), ('VENDA_EFETUADA', 'Venda Efetuada'), ('VENDA_CANCELADA', 'Venda Cancelada')], max_length=10, verbose_name='Tipo de Movimentação'),
        ),
    ]
