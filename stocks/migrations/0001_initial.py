# Generated by Django 5.0.6 on 2024-05-15 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50, verbose_name='Название компании')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена акции')),
                ('is_growing', models.BooleanField(verbose_name='Растет ли акция в цене?')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Когда последний раз обновлялось значение акции?')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фото логотипа компании')),
            ],
        ),
    ]
