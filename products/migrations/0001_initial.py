# Generated by Django 5.0.1 on 2024-02-06 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField()),
                ('description', models.CharField(max_length=255)),
                ('rating', models.PositiveIntegerField()),
            ],
        ),
    ]
