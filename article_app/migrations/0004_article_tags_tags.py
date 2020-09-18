# Generated by Django 3.1.1 on 2020-09-18 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article_app', '0003_auto_20200918_0916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags_title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Article_Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article_app.article')),
                ('tags_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article_app.tags')),
            ],
            options={
                'db_table': 'Article_Tags_mapping',
            },
        ),
    ]
