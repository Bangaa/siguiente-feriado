# Generated by Django 2.0.4 on 2018-04-24 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True, unique=True)),
                ('festividad', models.CharField(blank=True, max_length=50)),
                ('es_irrenunciable', models.BooleanField(default=False)),
                ('tipo', models.CharField(choices=[('C', 'Civil'), ('R', 'Religioso')], default='C', max_length=1)),
            ],
        ),
    ]
