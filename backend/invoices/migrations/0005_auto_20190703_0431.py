# Generated by Django 2.1.2 on 2019-07-03 04:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20190703_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceedhistory',
            name='ed_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoiceedhistory',
            name='ed_newdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceedhistory',
            name='ed_olddate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
