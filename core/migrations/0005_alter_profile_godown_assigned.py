# Generated by Django 4.1.3 on 2022-11-28 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_indocumentitem_rename_document_indocument_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='godown_assigned',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.godown'),
        ),
    ]