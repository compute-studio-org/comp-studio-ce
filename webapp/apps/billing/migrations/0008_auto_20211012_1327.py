# Generated by Django 3.2.8 on 2021-10-12 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0007_auto_20201211_0808"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer", name="metadata", field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="event", name="data", field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="event", name="metadata", field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="plan", name="metadata", field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="product", name="metadata", field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="subscription", name="metadata", field=models.JSONField(),
        ),
    ]
