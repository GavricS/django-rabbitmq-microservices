# Generated by Django 4.2.3 on 2023-07-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.PositiveBigIntegerField(unique=True)),
                ('total', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=255)),
            ],
        ),
    ]
