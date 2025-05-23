# Generated by Django 5.1.6 on 2025-05-01 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myprojectdpoll', '0023_candidate_votes_alter_voter_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='count',
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='myprojectdpoll.userprofile'),
        ),
        migrations.AlterField(
            model_name='voter',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$ZFDMuiJ3mhenvxOp90bMau$08n70nFCJDqw8nonCRb6gfxlMobjCxd2PUDGtv9PX6Q=', max_length=128),
        ),
    ]
