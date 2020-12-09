# Generated by Django 3.0.10 on 2020-12-09 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0007_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="cancel_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="subscription",
            name="trial_end",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="amount_off",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
