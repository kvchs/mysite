# Generated by Django 2.0.4 on 2018-04-19 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180419_2009'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booktoauthor',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='booktoauthor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='booktoauthor',
            name='book',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='blog.Author'),
        ),
        migrations.DeleteModel(
            name='BookToAuthor',
        ),
    ]
