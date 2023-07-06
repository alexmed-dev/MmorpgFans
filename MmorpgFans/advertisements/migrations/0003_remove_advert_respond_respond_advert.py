# Generated by Django 4.2.2 on 2023-06-20 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0002_advert_datetimecreate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advert',
            name='respond',
        ),
        migrations.AddField(
            model_name='respond',
            name='advert',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='advertisements.advert'),
            preserve_default=False,
        ),
    ]