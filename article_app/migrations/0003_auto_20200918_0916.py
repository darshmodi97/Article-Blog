# Generated by Django 3.1.1 on 2020-09-18 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0002_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article_app.users'),
        ),
    ]
