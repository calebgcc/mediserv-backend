# Generated by Django 4.1.6 on 2023-02-05 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.experiment')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=300)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.experiment')),
                ('experiment_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.experimentgroup')),
            ],
        ),
    ]
