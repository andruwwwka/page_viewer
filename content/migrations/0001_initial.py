# Generated by Django 3.0.3 on 2020-02-19 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('order', models.IntegerField(default=0)),
                ('counter', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AudioContent',
            fields=[
                ('basecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.BaseContent')),
                ('bitrate', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('content.basecontent',),
        ),
        migrations.CreateModel(
            name='TextContent',
            fields=[
                ('basecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.BaseContent')),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('content.basecontent',),
        ),
        migrations.CreateModel(
            name='VideoContent',
            fields=[
                ('basecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.BaseContent')),
                ('video_file', models.URLField()),
                ('subs', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.basecontent',),
        ),
        migrations.AddField(
            model_name='basecontent',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='content.Page'),
        ),
    ]
