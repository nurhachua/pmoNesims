# Generated by Django 2.0.3 on 2018-03-31 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmoApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan_evaluation',
            name='id',
        ),
        migrations.AddField(
            model_name='plan_evaluation',
            name='Plan_Evaluation_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='statusreport',
            name='statusDescription',
            field=models.CharField(max_length=100000, null=True),
        ),
    ]
