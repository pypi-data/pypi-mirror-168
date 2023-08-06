import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("obapi", "0007_rename_text_html_textcontentitem_text_html_tmp_and_more"),
        ("obpages", "0005_alter_usersequence_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="CuratedContentItem",
            fields=[
                (
                    "content_item",
                    models.OneToOneField(
                        help_text="Which content item to curate",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="obapi.contentitem",
                    ),
                ),
            ],
        ),
    ]
