# Generated by Django 3.2.8 on 2021-11-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0002_preguntaprueba'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntaprueba',
            name='alternativa_a',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='preguntaprueba',
            name='alternativa_b',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='preguntaprueba',
            name='alternativa_c',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='preguntaprueba',
            name='alternativa_d',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='preguntaprueba',
            name='solucion_math',
            field=models.TextField(max_length=200),
        ),
    ]
