# Generated by Django 2.1.7 on 2019-04-28 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='키워드')),
                ('number', models.PositiveSmallIntegerField(default=0, verbose_name='번호')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='상품이름')),
                ('address', models.CharField(default='-', max_length=256, verbose_name='상품주소')),
                ('num', models.CharField(default='-', max_length=30, verbose_name='상품번호')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_searched', models.DateTimeField(auto_now_add=True)),
                ('rank', models.CharField(max_length=5, verbose_name='랭킹')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank', to='main.Keyword')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Product')),
            ],
        ),
        migrations.AddField(
            model_name='keyword',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='main.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together={('product', 'number')},
        ),
    ]
