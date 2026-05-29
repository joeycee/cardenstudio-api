from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolioproject",
            name="meta_description",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name="portfolioproject",
            name="seo_title",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
