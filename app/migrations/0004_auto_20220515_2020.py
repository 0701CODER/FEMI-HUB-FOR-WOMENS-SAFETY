# Generated by Django 2.2.4 on 2022-05-15 14:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post_post_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 15, 14, 50, 49, 49590, tzinfo=utc), verbose_name='Posted Date'),
        ),
        migrations.AlterField(
            model_name='post_feedback',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 15, 14, 50, 49, 50590, tzinfo=utc), verbose_name='Posted Date'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=30)),
                ('date', models.DateField(default=datetime.datetime(2022, 5, 15, 14, 50, 49, 53591, tzinfo=utc), verbose_name='Posted Date')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Post')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Register_Detail')),
            ],
        ),
    ]
