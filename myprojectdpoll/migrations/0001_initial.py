# Generated by Django 4.1.13 on 2025-02-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('id_type', models.CharField(max_length=50)),
                ('id_number', models.CharField(max_length=50, unique=True)),
                ('id_doc', models.FileField(upload_to='id_docs/')),
                ('photo', models.FileField(upload_to='photos/')),
            ],
        ),
    ]
