# Generated by Django 4.0.2 on 2022-03-22 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('topic', models.CharField(max_length=120)),
                ('number_of_questions', models.IntegerField()),
                ('time', models.IntegerField(help_text='Время теста в минутах')),
                ('reqired_score_to_pass', models.IntegerField(help_text='Необходимый балл для прохождения в %')),
                ('difficulty', models.CharField(choices=[('Простой', 'Простой'), ('Средний', 'Средний'), ('Сложный', 'Сложный')], max_length=7)),
            ],
        ),
    ]