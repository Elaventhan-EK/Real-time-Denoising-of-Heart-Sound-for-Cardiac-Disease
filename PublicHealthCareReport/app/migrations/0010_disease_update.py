# Generated by Django 2.2.4 on 2021-04-05 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210401_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease_Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('area', models.CharField(max_length=200)),
                ('count', models.IntegerField(null=True, verbose_name='No of Affected Count')),
                ('cured_count', models.IntegerField(null=True, verbose_name='Cured Count')),
                ('current_count', models.IntegerField(null=True, verbose_name='No of Currently Affected Count')),
                ('disease_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Disease_Category')),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Doctor_Register')),
            ],
        ),
    ]
