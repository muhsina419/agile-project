# Generated by Django 5.1.6 on 2025-04-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myprojectdpoll', '0019_alter_voter_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$HTktM3F25li15sR2tWF85u$3XCF3IQwrW42bqrbPawCuZOHCek3GhdhfuEnc0eVO8M=', max_length=128),
        ),
    ]
