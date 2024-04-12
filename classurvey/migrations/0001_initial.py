# Generated by Django 4.1.8 on 2024-04-11 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_key', models.CharField(max_length=10)),
                ('class_name', models.CharField(max_length=50)),
                ('top_level', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=255, null=True)),
                ('examples', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestSound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sound_id', models.CharField(max_length=50)),
                ('sound_class', models.CharField(max_length=50)),
                ('sound_group', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TopLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_level_name', models.CharField(max_length=10)),
                ('top_level_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('user_name', models.CharField(default='', max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
            ],
        ),
        migrations.CreateModel(
            name='SoundAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('chosen_class', models.CharField(default='', max_length=15)),
                ('confidence', models.IntegerField(choices=[(1, 'Very Unconfident'), (2, 'Unconfident'), (3, 'Neutral'), (4, 'Confident'), (5, 'Very Confident')], default='')),
                ('comment', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('test_sound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classurvey.testsound')),
            ],
        ),
    ]
