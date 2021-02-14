from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(max_length=50, verbose_name='E-mail')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователей'

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='Имя')
    messages = models.TextField(blank=True, verbose_name='Сообщение')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.messages
