# Generated by Django 4.2.2 on 2023-06-20 09:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Respond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('accept', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('text', models.TextField()),
                ('category', models.CharField(choices=[('TN', 'Танки'), ('HL', 'Хилы'), ('DD', 'ДД'), ('TR', 'Торговцы'), ('GM', 'Гилдмастеры'), ('QG', 'Квестгиверы'), ('FR', 'Кузнецы'), ('SK', 'Кожевники'), ('PT', 'Зельевары'), ('SM', 'Мастера заклинаний')], default='TR', max_length=2)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('respond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.respond')),
            ],
        ),
    ]
