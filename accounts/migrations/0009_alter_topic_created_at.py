# Generated by Django 5.2.1 on 2025-05-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_category_topic_userprofile_selected_topics"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
