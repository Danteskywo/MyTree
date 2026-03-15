from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

User = get_user_model()

class Gender(models.TextChoices):
    MALE = 'M','Мужской'
    FEMALE = 'W','Женский'
    NOT_SPECIFIED = 'NS', 'Не указано'


class Person (models.Model):
    first_name = models.CharField('Имя',max_length=20)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    last_name = models.CharField('Фамилия', max_length=100)
    maiden_name = models.CharField('Девичья фамилия', max_length=100, blank=True, 
                                   help_text='Если женщина меняла фамилию')
    gender = models.CharField('Пол', max_length=2, choices=Gender.choices, 
                              default=Gender.NOT_SPECIFIED)
    birth_name = models.CharField('Имя при рождении', max_length=100, blank=True,
                                  help_text='Если имя менялось')
    birth_last_name = models.CharField('Фамилия при рождении', max_length=100, blank=True,
                                  help_text='Если фамилия менялось')
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    birth_date_approximate = models.BooleanField('Примерная дата рождения', default=False)
    birth_date_text = models.CharField('Текст даты рождения', max_length=100, blank=True,
                                       help_text='Например: "около 1820 г." или "весна 1943"')
    death_date = models.DateField('Дата смерти', null=True, blank=True)
    death_date_approximate = models.BooleanField('Примерная дата смерти', default=False)
    death_date_text = models.CharField('Текст даты смерти', max_length=100, blank=True)
    birth_place = models.CharField('Место рождения', max_length=255, blank=True)
    death_place = models.CharField('Место смерти', max_length=255, blank=True)
    current_residence = models.CharField('Текущее место жительства', max_length=255, blank=True)
    is_alive = models.BooleanField('Жив', default=True)
    is_private = models.BooleanField('Приватный профиль', default=False,
                                     help_text='Скрыть данные от гостей')
    bio = models.TextField('Биография', blank=True)
    occupation = models.CharField('Профессия/Занятие', max_length=255, blank=True)
    notes = models.TextField('Заметки', blank=True)
    # Метаданные
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='created_persons', verbose_name='Создал')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural ='Люди'
        indexes = [
            models.Index(fields=['last_name','first_name']),
            models.Index(fields=['birth_date']),
        ]
    def __str__(self):
        return self.full_name
    
    @property
    def  full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return ' '.join(filter(None,parts))
    @property
    def display_birth_date(self):
        if self.birth_date_text:
            return self.birth_date_text
        elif self.birth_date:
            return self.birth_date.strftime('%d.%m.%Y')
        return 'Неизвестно'
   
    
    def get_age(self, on_date=None):
        if not self.birth_date:
            return None
        if on_date is None:
            on_date = date.today()
        
        age = on_date.year - self.birth_date.year

        if on_date.month < self.birth_date.month or (on_date.month == self.birth_date.month and
                                                     on_date.day < self.birth_date.day):
            age -= 1
        return age

class RelationshipType(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    name_reverse = models.CharField('Обработаное задание', max_length=50,
                                    help_text='Например: "Родитель" -> "ребенок"')
    is_family = models.BooleanField('Семейная связь', default=True)
    description = models.TextField('Описание', blank=True)

    is_biological = models.BooleanField('Биологическая связь', default=False)
    is_adoptive = models.BooleanField('Приемная связь', default=False)
    is_guardian = models.BooleanField('Опека', default=False)

    class Meta:
        verbose_name = 'Тип отношений'
        verbose_name_plural = 'Типы отношений'

    def __str__(self):
        return self.name
    
class Relationship(models.Model):
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE,
                                    related_name='relationship_from',
                                    verbose_name='От кого')
    to_person = models.ForeignKey(Person, on_delete=models.CASCADE,
                                  related_name='relationship_to',
                                  verbose_name='К кому')
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.PROTECT,
                                          verbose_name='Тип отношений')
    date_start = models.DateField('Дата начала отношений', null=True, blank=True)
    date_end = models.DateField('Дата окончания', null=True, blank=True)
    is_current = models.BooleanField('Текущие отношения', default=True)
    notes = models.TextField('Заметки о связи', blank=True)

    # Для обратных связей (например, если связь двунаправленная)

    is_bidirectional = models.BooleanField('Двунаправленная', default=False,
                                           help_text='Напримерб супруги - связь в обе стороны')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
        unique_together = ['from_person','to_person','relationship_type']
        indexes = [
            models.Index(fields=['from_person','relationship_type']),
        ]
    def __str__(self):
        return f"{self.from_person} - {self.relationship_type} - {self.to_person}"
    
    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        if self.is_bidirectional:
            reverse_rel, created = Relationship.objects.get_or_create(
                from_person=self.to_person,
                to_person=self.from_person,
                relationship_type=self.relationship_type,
                defaults={'is_bidirectional': True, 'is_current': self.is_current}
            )







    
    













