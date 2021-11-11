# Generated by Django 3.2 on 2021-05-23 05:28

from django.db import migrations, models
import django.db.models.deletion
import insects.models


class Migration(migrations.Migration):

    dependencies = [
        ('insects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, upload_to=insects.models.save_to)),
                ('placeholder', models.CharField(default=None, max_length=100)),
                ('subset', models.CharField(default=None, max_length=20)),
                ('insect', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='insects.insect')),
            ],
        ),
    ]
