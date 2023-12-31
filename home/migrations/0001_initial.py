# Generated by Django 4.2.5 on 2023-10-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecordedVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(default='recording', max_length=20)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audio/')),
                ('file_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
