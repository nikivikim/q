from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Indicator(models.Model):
    name = models.CharField('Название кода', max_length=100)
    code = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'

class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('Период')
    company_name = models.CharField('Название компании', max_length=100)
    activity_type = models.ForeignKey('ActivityType', verbose_name='Вид деятельности', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        unique_together = ('user', 'date')

class IndicatorValue(models.Model):
    balance = models.ForeignKey(Balance, related_name='indicator_values', on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    value = models.FloatField('Значение')
    value2 = models.FloatField('Значение1')
    value3 = models.FloatField('Значение2')
    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'

class ActivityType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид деятельности'
        verbose_name_plural = 'Виды деятельности'

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    report_data = models.TextField()
    chart = models.TextField()

    def __str__(self):
        return f"Report for {self.balance.company_name} on {self.created_at}"