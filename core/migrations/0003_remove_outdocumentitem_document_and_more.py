# Generated by Django 4.1.3 on 2022-11-28 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_document_type_alter_documentitem_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outdocumentitem',
            name='document',
        ),
        migrations.AddField(
            model_name='outdocumentitem',
            name='outdocument',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.outdocument'),
            preserve_default=False,
        ),
    ]