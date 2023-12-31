# Generated by Django 4.2.4 on 2023-08-24 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_product_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ManyToManyField(blank=True, default=None, to='bot.user'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=350, verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user')),
            ],
        ),
    ]
