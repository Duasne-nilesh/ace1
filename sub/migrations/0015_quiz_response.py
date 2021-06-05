# Generated by Django 3.1.3 on 2021-06-05 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub', '0014_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='quiz_response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('semester', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('q_id', models.CharField(max_length=900)),
                ('sub_answer', models.CharField(max_length=800)),
                ('corr_answer', models.CharField(max_length=800)),
                ('marks', models.CharField(max_length=800)),
                ('category', models.CharField(max_length=400)),
            ],
        ),
    ]
