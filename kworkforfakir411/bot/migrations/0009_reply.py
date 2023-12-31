# Generated by Django 4.2.4 on 2023-08-25 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_remove_message_id_message_message_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=250, verbose_name='Текст сообщения')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Картинка')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.message', verbose_name='Сообщение')),
            ],
        ),
    ]
