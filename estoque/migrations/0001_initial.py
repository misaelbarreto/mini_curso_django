# Generated by Django 2.2.2 on 2019-06-19 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoProduto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
            ],
            options={
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço')),
                ('quantidade_em_estoque', models.IntegerField(default=0, editable=False, verbose_name='Quantidade Em Estoque')),
                ('tipo_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.TipoProduto')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('tipo_movimentacao', models.CharField(choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída'), ('VENDA', 'Venda')], max_length=10, verbose_name='Tipo de Movimentação')),
                ('observacao', models.CharField(blank=True, max_length=255, null=True, verbose_name='Observação')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.Produto')),
            ],
            options={
                'ordering': ['produto', 'quantidade', 'tipo_movimentacao'],
            },
        ),
    ]
