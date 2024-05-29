# Generated by Django 5.0.6 on 2024-05-24 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursery_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plant',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Flowering Plants'), (2, 'Indoor Plants'), (3, 'Hanging Plants'), (4, 'Low Maintenance Plants')], verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='pdetails',
            field=models.CharField(max_length=100, verbose_name='Plant Details'),
        ),
    ]
