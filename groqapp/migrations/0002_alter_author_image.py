# Generated by Django 4.2.11 on 2024-03-12 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groqapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='authors'),
        ),
    ]
