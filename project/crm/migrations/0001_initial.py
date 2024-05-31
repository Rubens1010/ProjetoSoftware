# Generated by Django 5.0.6 on 2024-05-30 23:46

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_income', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('monthly_expense', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
