from django import forms
from django.core.exceptions import ValidationError
from .models import Relationship, RelationshipType, Gender, Person
from datetime import datea

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['create_by', 'create_at', 'updated_at']
        widgets = {
            'first_name':forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': 'Введите Имя'
            }),
            'middle_name': forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Введите отчество'
            }),
            'last_nmae' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Введите фамилию'
            }),
            'maiden_name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Девичья фамилия (если меняла)'
            }),
            'birth_name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Имя при рождении'
            }),
            'birth_last_name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Фамилия при рождении'
            }),
            'birth_date' : forms.DateInput(attrs={
                'type' : 'date',
                'class' : 'form-control'
            }),
            'death_date' : forms.DateInput(attrs={
                'type' : 'date',
                'class' : 'from-control'
            }),
            'birth_date_text' : forms.DateInput(attrs={
                'type' : 'date',
                'placeholder' : 'Например : Зима 1945г'
            }),
            'death_date_text' : forms.DateInput(attrs={
                'type' : 'date',
                'placeholder' : 'Например : Около 1945 - 1950 г'
            }),
            'birth_place' : forms.TextInput(attrs = {
                'calss' : 'form-control',
                "placeholder" : "Где родился: Страна, город, район"
            }),
            'death_place' : forms.TextInput(attrs = {
                'calss' : 'form-control',
                "placeholder" : "Последнее место нахождения: Страна, город, район"
            }),
            'current_residence' : forms.TextInput(attrs = {
                'calss' : 'form-control',
                "placeholder" : "Где живет сейчас?"
            }),
             'death_place' : forms.TextInput(attrs = {
                'calss' : 'form-control',
                "placeholder" : "Последнее место нахождения: Страна, город, район"
            }),
            # Професия
            'occupation' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Проффесия или основное занятие'
            }),
            'bio' : forms.TextInput(attrs={
                'class' : 'form-control',
                'rows' : 5, # Высота в 5 строк
                'placeholder' : 'Биография человека'
            }),
            'notes' : forms.Textarea(attrs={
                'class' : 'form-contorl',
                'rows' : 3,
                'placeholder' : 'Дополнительные заметки'
            }),
            #Булевые поля (флажки)
            'birth_date_approximate': forms.CheckboxInput(attrs={
                'class': 'form-check-input'  # Специальный класс Bootstrap для чекбоксов
            }),
            'death_date_approximate': forms.CheckboxInput(attrs={
                'class': 'form-check-input' 
            }),
            'is_alive': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id' : 'id_is_alive' 
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input' 
            }),
            # Поля выбора Select
            'gender' : forms.Select(atts={
                'class' : 'form-select'
            }),
        }