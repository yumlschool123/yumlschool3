import datetime
from venv import logger
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import requests
from datetime import datetime
import datetime  
import logging
import json
from django.contrib import messages
from django.template.loader import get_template
import base64
import bcrypt
import re

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from django.shortcuts import render, redirect
from datetime import datetime, date
from django.utils import timezone
import csv
from django.http import HttpResponse
import re
import json
from django.contrib import messages


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse


API_BASE_URL = 'https://yumlschool.ru/api'  


from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.http import HttpResponse


from django.http import HttpResponse
from docx import Document
from docx.shared import Pt


from django.http import HttpResponse
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import json
import os
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Вспомогательная функция для выполнения API-запросов
def make_api_request(endpoint, method='get', data=None, params=None):
    # Убираем ведущий слеш, если он присутствует
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]
    
    # Здесь должно быть API_BASE_URL без добавления "api/" вначале URL,
    # так как эта часть уже содержится в endpoint
    url = f'{API_BASE_URL}/{endpoint}'
    
    print(f"API Request: {method.upper()} {url}")
    
    try:
        response = requests.request(
            method, 
            url, 
            json=data if method.lower() in ['post', 'put'] else None,
            data=data if method.lower() not in ['post', 'put'] else None,
            params=params,
            verify=False
        )
        print(f"API Response: {response.status_code}")
        
        # Возвращаем словарь с данными вместо объекта ответа
        result = {
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None
        }
        return result
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return {
            'status_code': 500,
            'data': None,
            'error': str(e)
        }
    


def export_groups_to_json(request):
    # Получаем данные из таблицы Group
    groups_response = make_api_request('Groups')
    
    if groups_response['status_code'] != 200:
        return HttpResponse("Ошибка при получении данных групп.", status=500)

    groups = groups_response['data']

    # Формируем данные в нужном формате
    formatted_groups = [{"nameGroup": group['nameGroup']} for group in groups]

    # Создаем JSON файл
    json_file_path = 'exported_groups.json'
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(formatted_groups, file, ensure_ascii=False, indent=4)

    # Отправляем файл пользователю
    response = HttpResponse(open(json_file_path, 'rb'), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(json_file_path)}"'
    
    return response



def import_groups_from_json(request):
    if request.method == 'POST':
        json_file = request.FILES.get('json_file')  # Используем get вместо прямого доступа
        if json_file:
            fs = FileSystemStorage()
            filename = fs.save(json_file.name, json_file)

            # Читаем JSON файл и загружаем данные
            file_path = fs.path(filename)  # Получаем путь к файлу
            with open(file_path, 'r', encoding='utf-8') as file:  # Используем file_path
                groups_data = json.load(file)

            # Отправляем данные на API
            api_url = f'{API_BASE_URL}/Groups'  

            for group in groups_data:
                # Убедитесь, что данные имеют правильный формат
                if 'nameGroup' in group:
                    response = requests.post(api_url, json={'nameGroup': group['nameGroup']}, verify=False)  # Игнорируем проверку сертификата
                    if response.status_code not in [201, 200]:  # Проверяем, что запрос успешен
                        messages.error(request, f'Ошибка при загрузке группы: {group["nameGroup"]}')
                        return redirect('group_crud')
                else:
                    messages.error(request, 'Некорректный формат данных в JSON файле.')
                    return redirect('group_crud')

            messages.success(request, 'Данные успешно загружены из JSON файла.')
            return redirect('group_crud')
        else:
            messages.error(request, 'Файл не загружен. Пожалуйста, выберите файл.')
            return redirect('group_crud')

    return render(request, 'AdminPanel.html')




def export_students_performance(request, practical_work_id):
    practical_work_url = f'{API_BASE_URL}/PracticalWorks/{practical_work_id}'
    response_from_api = requests.get(practical_work_url, verify=False)

    if response_from_api.status_code != 200:
        return HttpResponse("Практическая работа не найдена.", status=404)

    practical_work = response_from_api.json()

    # Получаем информацию о предмете
    subject_url = f'{API_BASE_URL}/Subjects/{practical_work["subjectId"]}'
    response_subject = requests.get(subject_url, verify=False)
    subject = response_subject.json() if response_subject.status_code == 200 else {}
    subject_name = subject.get('nameSubject', 'Неизвестно')
    group_id = subject.get('idGroup', None)

    # Получаем информацию о группе
    group_name = 'Не указано'
    if group_id:
        group_url = f'{API_BASE_URL}/Groups/{group_id}'
        response_group = requests.get(group_url, verify=False)
        group = response_group.json() if response_group.status_code == 200 else {}
        group_name = group.get('nameGroup', 'Не указано')

    completed_works_url = f'{API_BASE_URL}/PracticalWorks/{practical_work_id}/completed'
    response_completed_works = requests.get(completed_works_url, verify=False)

    if response_completed_works.status_code != 200:
        return HttpResponse("Нет сданных работ.", status=404)

    completed_works = response_completed_works.json()

    # Создаем PDF документ
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Успеваемость студентов.pdf"'
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Настройка шрифта
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))  # Убедитесь, что шрифт доступен
    p.setFont("Arial", 16)

    # Заголовок
    p.drawString(100, height - 50, 'YumlSchool')
    p.setFont("Arial", 12)
    p.drawString(100, height - 70, f'"{practical_work["namePracticalWork"]}"')
    p.drawString(100, height - 90, f'Предмет: {subject_name}')
    p.drawString(100, height - 110, f'Группа: {group_name}')

    # Список студентов и их оценки в виде таблицы
    p.setFont("Arial", 14)
    p.drawString(100, height - 140, 'Список студентов и их оценки')

    # Рисуем таблицу
    table_start_y = height - 160
    row_height = 20
    col_widths = [3 * inch, 1 * inch]  # Ширина столбцов

    # Заголовки таблицы
    p.setFont("Arial", 12)
    p.setFillColor(colors.grey)
    p.rect(100, table_start_y, sum(col_widths), row_height, stroke=1, fill=1)
    p.setFillColor(colors.black)
    p.drawString(100 + 5, table_start_y + 5, 'ФИО студента')
    p.drawString(100 + col_widths[0], table_start_y + 5, 'Оценка')

    # Рисуем строки таблицы
    p.setFillColor(colors.white)
    table_start_y -= row_height

    for work in completed_works:
        user_id = work['userId']
        user_url = f'{API_BASE_URL}/Users/{user_id}'
        response_user = requests.get(user_url, verify=False)
        user = response_user.json() if response_user.status_code == 200 else {}
        
        full_name = f"{user.get('firstName', 'Не указано')} {user.get('secondName', 'Не указано')} {user.get('middleName', 'Не указано')}"
        grade = str(work.get('grade', 'Не сдано'))

        # Рисуем строки
        p.setFillColor(colors.white)
        p.rect(100, table_start_y, sum(col_widths), row_height, stroke=1, fill=1)
        p.setFillColor(colors.black)
        p.drawString(100 + 5, table_start_y + 5, full_name)
        p.drawString(100 + col_widths[0], table_start_y + 5, grade)

        table_start_y -= row_height

    # Получаем текущую дату
    current_date = datetime.now()
    day = current_date.day
    month = current_date.strftime("%B")  # Получаем название месяца на английском
    year = current_date.year

    # Словарь для перевода названий месяцев на русский
    months_translation = {
        "January": "января",
        "February": "февраля",
        "March": "марта",
        "April": "апреля",
        "May": "мая",
        "June": "июня",
        "July": "июля",
        "August": "августа",
        "September": "сентября",
        "October": "октября",
        "November": "ноября",
        "December": "декабря"
    }

    # Переводим месяц на русский
    month_russian = months_translation.get(month, month)

    # Подпись преподавателя
    p.drawString(100, table_start_y - 20, 'Подпись преподавателя  _____________')
    p.drawString(100, table_start_y - 40, f'«{day}» {month_russian} {year} года')

    # Имя преподавателя
    teacher_url = f'{API_BASE_URL}/Users/{practical_work["userId"]}'
    response_teacher = requests.get(teacher_url, verify=False)
    teacher = response_teacher.json() if response_teacher.status_code == 200 else {}
    full_teacher_name = f"{teacher.get('firstName', 'Не указано')} {teacher.get('secondName', 'Не указано')} {teacher.get('middleName', 'Не указано')}"
    p.drawString(100, table_start_y - 60, f'Проверил преподаватель {full_teacher_name}')

    p.showPage()
    p.save()
    buffer.seek(0)
    response.write(buffer.read())
    return response













def index(request):
    return redirect('login')

def adminPage(request):
    return render(request, 'AdminPanel.html')

def LectionCRUD(request):
    return render(request, 'SubjectInfo/LectionCRUD.html')

def LectionMaterial(request, id):
    # Проверяем авторизацию
    if 'user_id' not in request.session:
        request.session['next_url'] = request.path
        return redirect('login')

    lection_url = f'{API_BASE_URL}/LectionMaterials/{id}'
    response_from_api_lection = requests.get(lection_url, verify=False)
    lection = response_from_api_lection.json() if response_from_api_lection.status_code == 200 else {}

    # Получаем информацию о преподавателе
    teacher_url = f'{API_BASE_URL}/Users/{lection["userId"]}'  
    response_from_api_teacher = requests.get(teacher_url, verify=False)
    teacher = response_from_api_teacher.json() if response_from_api_teacher.status_code == 200 else {}

    # Получаем роль пользователя из сессии
    role_id = request.session.get('role_id')
    user_id = request.session.get('user_id')

    return render(request, 'SubjectInfo/LectionMaterial.html', {
        'lection': lection,
        'teacher': teacher,
        'role_id': role_id,  # Добавляем role_id в контекст
        'user_id': user_id   # Добавляем user_id в контекст
    })




def SubjectPage(request, id):
    # Проверяем, авторизован ли пользователь
    if 'user_id' not in request.session:
        request.session['next_url'] = request.path
        return redirect('login')
    
    try:
        # Получаем информацию о предмете
        subject_url = f'{API_BASE_URL}/Subjects/{id}'
        subject_response = requests.get(subject_url, verify=False)
        
        if subject_response.status_code != 200:
            return redirect('AllSubjectPage')  
        
        subject = subject_response.json()
        
        # Получаем информацию о группе
        group_id = subject.get('idGroup')
        group_url = f'{API_BASE_URL}/Groups/{group_id}'
        group_response = requests.get(group_url, verify=False)
        group = group_response.json() if group_response.status_code == 200 else None

        # Получаем студентов из группы
        students_url = f'{API_BASE_URL}/Users'
        students_response = requests.get(students_url, verify=False)
        all_users = students_response.json() if students_response.status_code == 200 else []
        students = [user for user in all_users if user.get('idGroup') == group_id and user.get('idRole') == 3]  # Студенты (role_id = 3)

        # Получаем лекции, практические работы и тесты
        lections_url = f'{API_BASE_URL}/LectionMaterials'
        lections_response = requests.get(lections_url, verify=False)
        lections = [lection for lection in lections_response.json() if lection.get('subjectId') == id] if lections_response.status_code == 200 else []

        practical_works_url = f'{API_BASE_URL}/PracticalWorks'
        practical_works_response = requests.get(practical_works_url, verify=False)
        practical_works = [pw for pw in practical_works_response.json() if pw.get('subjectId') == id] if practical_works_response.status_code == 200 else []

        tests_url = f'{API_BASE_URL}/Tests'
        tests_response = requests.get(tests_url, verify=False)
        tests = [test for test in tests_response.json() if test.get('subjectId') == id] if tests_response.status_code == 200 else []

        # Получаем информацию о преподавателе
        teacher_id = subject.get('userId')
        teacher_url = f'{API_BASE_URL}/Users/{teacher_id}'
        teacher_response = requests.get(teacher_url, verify=False)
        teacher = teacher_response.json() if teacher_response.status_code == 200 else None

        context = {
            'subject': subject,
            'group': group,
            'students': students,  # Добавляем студентов в контекст
            'lections': lections,
            'practical_works': practical_works,
            'tests': tests,
            'teacher': teacher,  # Добавляем учителя в контекст
            'role_id': request.session.get('role_id')
        }
        
        return render(request, 'SubjectPage.html', context)

    except Exception as e:
        print(f"Error in SubjectPage: {e}")
        return redirect('AllSubjectPage')






def create_lection(request, subject_id):
    if request.method == 'POST':
        name_lection_material = request.POST.get('nameLectionMaterial')
        description_lection_material = request.POST.get('descriptionLectionMaterial')
        name_file_lection = request.POST.get('nameFileLection')
        url_file_lection = request.POST.get('urlFileLection')
        user_id = request.session.get('user_id')

        # Получаем текущую дату и время
        date_upload = date.today() 
        time_upload = datetime.now().time().strftime('%H:%M:%S')  

        # Создаем лекцию
        api_url = f'{API_BASE_URL}/LectionMaterials'
        data = {
            'nameLectionMaterial': name_lection_material,
            'descriptionLectionMaterial': description_lection_material,
            'dateUploadLectionMaterial': str(date_upload),
            'timeUploadLectionMaterial': str(time_upload),
            'nameFileLection': name_file_lection,
            'urlFileLection': url_file_lection,
            'userId': user_id,
            'subjectId': subject_id  # Связываем лекцию с предметом
        }

        try:
            response = requests.post(api_url, json=data, verify=False)
            response.raise_for_status()
            return redirect('SubjectPage', id=subject_id)  
        except requests.exceptions.RequestException as e:
            return render(request, 'SubjectInfo/LectionCRUD.html', {
                'error': 'Ошибка при добавлении лекции: ' + str(e),
            })

    return render(request, 'SubjectInfo/LectionCRUD.html')


def edit_lection(request, id):
    lection_url = f'{API_BASE_URL}/LectionMaterials/{id}'

    # Получаем текущую лекцию
    try:
        response_from_api_lection = requests.get(lection_url, verify=False)
        response_from_api_lection.raise_for_status()
        lection = response_from_api_lection.json()
    except requests.exceptions.RequestException as e:
        return render(request, 'SubjectInfo/LectionEdit.html', {
            'error': 'Ошибка при получении лекции: ' + str(e),
        })

    if request.method == 'POST':
        updated_data = {
            'IdLectionMaterial': id,
            'nameLectionMaterial': request.POST.get('nameLectionMaterial', lection['nameLectionMaterial']),
            'descriptionLectionMaterial': request.POST.get('descriptionLectionMaterial', lection['descriptionLectionMaterial']),
            'dateUploadLectionMaterial': lection['dateUploadLectionMaterial'],
            'timeUploadLectionMaterial': lection['timeUploadLectionMaterial'],
            'nameFileLection': request.POST.get('nameFileLection', lection['nameFileLection']),
            'urlFileLection': request.POST.get('urlFileLection', lection['urlFileLection']),
            'userId': lection['userId'],
            'subjectId': lection['subjectId'],
        }

        print("Отправляемые данные для обновления:", updated_data)

        try:
            response = requests.put(lection_url, json=updated_data, verify=False)
            response.raise_for_status()
            print("Ответ от API:", response.status_code, response.text)
            # Изменяем редирект на страницу лекции
            return redirect('LectionMaterial', id=id)  # Перенаправляем на страницу лекции
        except requests.exceptions.RequestException as e:
            return render(request, 'SubjectInfo/LectionEdit.html', {
                'error': 'Ошибка при обновлении лекции: ' + str(e),
                'lection': lection,
            })

    return render(request, 'SubjectInfo/LectionEdit.html', {'lection': lection})


def delete_lection(request, id):
    # Получаем информацию о лекции для получения subjectId
    lection_url = f'{API_BASE_URL}/LectionMaterials/{id}'
    response_from_api_lection = requests.get(lection_url, verify=False)
    lection = response_from_api_lection.json() if response_from_api_lection.status_code == 200 else {}

    if request.method == 'POST':
        response = requests.delete(lection_url, verify=False)
        if response.status_code == 204: 
            return redirect('SubjectPage', id=lection['subjectId'])  
    return HttpResponse(status=405)



def AllSubjectPage(request):
    # Проверяем, авторизован ли пользователь
    if 'user_id' not in request.session:
        # Сохраняем URL, на который пользователь пытался перейти
        request.session['next_url'] = request.path
        return redirect('login')
    
    try:
        # Получаем информацию о пользователе
        user_id = request.session.get('user_id')
        role_id = request.session.get('role_id')
        
        # Получаем список всех предметов
        subjects_response = make_api_request('Subjects')
        
        # Проверяем статус код в словаре, а не как атрибут объекта
        if subjects_response['status_code'] != 200:
            return redirect('nullSubjects')
        
        # Получаем данные из словаря, а не вызывая метод json()
        all_subjects = subjects_response['data']
        
        # Фильтруем предметы в зависимости от роли пользователя
        if role_id == 1:  # Администратор
            subjects = all_subjects  # Администратору доступны все предметы
        elif role_id == 2:  # Преподаватель
            # Фильтруем предметы, где userId совпадает с ID пользователя
            subjects = [subject for subject in all_subjects if subject.get('userId') == user_id]
        elif role_id == 3:  # Студент
            # Получаем информацию о группе пользователя
            user_response = make_api_request(f'Users/{user_id}')
            if user_response['status_code'] != 200:
                return redirect('nullSubjects')
            
            user = user_response['data']
            group_id = user.get('idGroup')
            
            # Фильтруем предметы, где idGroup совпадает с группой пользователя
            subjects = [subject for subject in all_subjects if subject.get('idGroup') == group_id]
        else:
            return redirect('nullSubjects')
        
        if not subjects:
            return redirect('nullSubjects')
        
        # Получаем информацию о группах
        groups_response = make_api_request('Groups')
        groups = groups_response['data'] if groups_response['status_code'] == 200 else []
        
        # Получаем информацию о пользователях (преподавателях)
        users_response = make_api_request('Users')
        users = users_response['data'] if users_response['status_code'] == 200 else []
        
        context = {
            'subjects': subjects,
            'groups': groups,
            'users': users,
        }
        
        return render(request, 'AllSubjectPage.html', context)
    
    except Exception as e:
        print(f"Error in AllSubjectPage: {e}")
        return redirect('nullSubjects')


def nullSubjects(request):
    return render(request, 'NullSubjects.html')


def login(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        
        if not login or not password:
            return render(request, 'login.html', {'error': 'Логин и пароль обязательны', 'login': login})

        try:
            # Получаем всех пользователей
            users_response = requests.get(f'{API_BASE_URL}/Users', verify=False)
            if users_response.status_code == 200:
                users = users_response.json()
                
                # Ищем пользователя по зашифрованному логину
                encoded_login = base64.b64encode(login.encode()).decode()
                user = next((u for u in users if u['login'] == encoded_login), None)
                
                if user is None:
                    # Логин не существует
                    return render(request, 'login.html', {'error': 'Такого логина не существует', 'login': login})
                
                if not bcrypt.checkpw(password.encode(), user['password'].encode()):
                    # Пароль неверный
                    return render(request, 'login.html', {'error': 'Неверный пароль', 'login': login})

                # Пароль верный
                request.session.flush()
                
                request.session['user_id'] = user.get('idUser')
                request.session['role_id'] = user.get('idRole')
                request.session['full_name'] = f"{user.get('firstName')} {user.get('secondName')}"
                request.session['last_activity'] = str(datetime.now())
                
                request.session.set_expiry(60 * 60 * 24 * 14)
                request.session.save()
                
                next_url = request.session.get('next_url')
                if next_url:
                    del request.session['next_url']
                    return redirect(next_url)
                
                # Изменяем логику перенаправления в зависимости от роли
                role_id = user.get('idRole')
                if role_id == 1:  # Администратор
                    return redirect('adminPage')
                else:  # Преподаватель или студент
                    return redirect('AllSubjectPage')
            else:
                return render(request, 'login.html', {'error': 'Ошибка при проверке учетных данных', 'login': login})
                
        except Exception as e:
            print(f"Exception during authentication: {str(e)}")
            return render(request, 'login.html', {'error': f'Ошибка при аутентификации: {str(e)}', 'login': login})
    
    return render(request, 'login.html')








def logout(request):
    request.session.flush()
    return redirect('login')


import re
import base64
import bcrypt
import requests
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        request.session.flush()

        # Получаем данные из формы
        first_name = request.POST.get('firstName')
        second_name = request.POST.get('secondName')
        middle_name = request.POST.get('middleName')
        email = request.POST.get('email')
        login = request.POST.get('login')
        password = request.POST.get('password')

        # Список для хранения ошибок
        errors = []

        # Проверка на минимальную длину логина и пароля
        if len(login) < 8:
            errors.append('Логин должен содержать минимум 8 символов.')
        if len(password) < 8:
            errors.append('Пароль должен содержать минимум 8 символов.')

        # Проверка на наличие цифры и специального символа в пароле
        if not re.search(r'\d', password):
            errors.append('Пароль должен содержать как минимум одну цифру.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Пароль должен содержать как минимум один специальный символ.')

        # Если есть ошибки, возвращаем их в шаблон
        if errors:
            return render(request, 'registration.html', {
                'error': ' '.join(errors),
                'first_name': first_name,
                'second_name': second_name,
                'middle_name': middle_name,
                'email': email,
                'login': login
            })

        # Проверяем, существует ли пользователь с таким email или логином
        try:
            users_response = requests.get(f'{API_BASE_URL}/Users', verify=False)
            if users_response.status_code == 200:
                users = users_response.json()
                
                # Проверка на существование email
                if any(user['email'].lower() == email.lower() for user in users):
                    return render(request, 'registration.html', {
                        'error': 'Пользователь с таким email уже существует',
                        'first_name': first_name,
                        'second_name': second_name,
                        'middle_name': middle_name,
                        'email': email,
                        'login': login
                    })

                # Проверка на существование логина
                if any(base64.b64decode(user['login']).decode() == login for user in users):
                    return render(request, 'registration.html', {
                        'error': 'Пользователь с таким логином уже существует',
                        'first_name': first_name,
                        'second_name': second_name,
                        'middle_name': middle_name,
                        'email': email,
                        'login': login
                    })

            # Шифруем логин в base64
            encoded_login = base64.b64encode(login.encode()).decode()
            
            # Хешируем пароль с помощью bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

            id_role = 4

            if len(users) == 0:
                id_role = 1

            new_user = {
                'firstName': first_name,
                'secondName': second_name,
                'middleName': middle_name,
                'email': email,
                'login': encoded_login,
                'password': hashed_password,
                'idRole': id_role,
                'idGroup': 6
            }

            print("Отправляемые данные:", new_user)
            response = requests.post(f'{API_BASE_URL}/Users', json=new_user, verify=False)
            print("Статус ответа:", response.status_code)
            print("Ответ:", response.text)
            
            if response.status_code in [200, 201]:
                user_data = response.json()
                request.session['user_id'] = user_data.get('idUser')
                request.session['role_id'] = 4
                request.session['full_name'] = f"{first_name} {second_name} {middle_name}"
                return redirect('nullSubjects')
            else:
                error_message = f"Ошибка при регистрации. Статус: {response.status_code}"
                return render(request, 'registration.html', {
                    'error': error_message,
                    'first_name': first_name,
                    'second_name': second_name,
                    'middle_name': middle_name,
                    'email': email,
                    'login': login
                })

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при регистрации: {str(e)}")
            return render(request, 'registration.html', {
                'error': 'Ошибка при регистрации: ' + str(e),
                'first_name': first_name,
                'second_name': second_name,
                'middle_name': middle_name,
                'email': email,
                'login': login
            })

    return render(request, 'registration.html')





def group_crud(request):
    response_from_api = requests.get(f'{API_BASE_URL}/Groups', verify=False)
    
    if response_from_api.status_code == 200:
        groups = response_from_api.json()
    else:
        groups = []

    return render(request, 'AdminPanel/GroupCRUD.html', {'groups': groups})

def create_group(request):
    if request.method == 'POST':
        name_group = request.POST.get('nameGroup')
        response = requests.post(f'{API_BASE_URL}/Groups', json={'nameGroup': name_group}, verify=False)
        return redirect('group_crud')
    return HttpResponse(status=405)

def edit_group(request, id):
    if request.method == 'POST':
        name_group = request.POST.get('nameGroup')
        response = requests.put(f'{API_BASE_URL}/Groups/{id}', json={'idGroup': id, 'nameGroup': name_group}, verify=False)
        return redirect('group_crud')
    return HttpResponse(status=405)

def delete_group(request, id):
    if request.method == 'POST':
        response = requests.delete(f'{API_BASE_URL}/Groups/{id}', verify=False)
        return redirect('group_crud')
    return HttpResponse(status=405)



def user_crud(request):
    response_from_api_users = requests.get(f'{API_BASE_URL}/Users', verify=False)
    users = response_from_api_users.json() if response_from_api_users.status_code == 200 else []

    response_from_api_roles = requests.get(f'{API_BASE_URL}/Roles', verify=False)
    roles = response_from_api_roles.json() if response_from_api_roles.status_code == 200 else []

    response_from_api_groups = requests.get(f'{API_BASE_URL}/Groups', verify=False)
    groups = response_from_api_groups.json() if response_from_api_groups.status_code == 200 else []

    selected_group_id = request.GET.get('group_id')
    if selected_group_id:
        users = [user for user in users if user.get('idGroup') == int(selected_group_id)]

    search_query = request.GET.get('search', '').strip()
    if search_query:
        users = [user for user in users if (
            search_query.lower() in user['firstName'].lower() or
            search_query.lower() in user['secondName'].lower() or
            search_query.lower() in user['middleName'].lower()
        )]

    sort_by = request.GET.get('sort_by', 'secondName')  
    if sort_by == 'secondName':
        users.sort(key=lambda x: x['secondName'])
    elif sort_by == 'firstName':
        users.sort(key=lambda x: x['firstName'])
    elif sort_by == 'middleName':
        users.sort(key=lambda x: x['middleName'])
    elif sort_by == 'group':
        users.sort(key=lambda x: x.get('idGroup', ''))

    return render(request, 'AdminPanel/UserCRUD.html', {'users': users, 'roles': roles, 'groups': groups})






from django.contrib import messages
import re

def edit_user(request, id):
    if request.method == 'POST':
        user_data = {
            'IdUser': id,
            'FirstName': request.POST.get('firstName'),
            'SecondName': request.POST.get('secondName'),
            'MiddleName': request.POST.get('middleName'),
            'Email': request.POST.get('email'),
            'IdRole': request.POST.get('idRole'),
            'IdGroup': request.POST.get('idGroup'),
        }    
        print(user_data)

        response = requests.put(f'{API_BASE_URL}/Users/{id}', json=user_data, verify=False)

        if response.status_code == 204: 
            return redirect('user_crud')
        else:
            print("Ошибка при обновлении пользователя:", response.status_code, response.text)
            return HttpResponse("Ошибка при обновлении данных пользователя.", status=response.status_code)

    return HttpResponse(status=405)


def delete_user(request, id):
    if request.method == 'POST':
        response = requests.delete(f'{API_BASE_URL}/Users/{id}', verify=False)
        return redirect('user_crud')
    return HttpResponse(status=405)

def subject_crud(request):
    if request.method == 'POST':
        new_subject = {
            'nameSubject': request.POST.get('nameSubject'),
            'idGroup': request.POST.get('idGroup'),
            'userId': request.POST.get('userId'),
        }
        response = requests.post(f'{API_BASE_URL}/Subjects', json=new_subject, verify=False)
        return redirect('subject_crud')

    response_from_api_groups = requests.get(f'{API_BASE_URL}/Groups', verify=False)
    groups = response_from_api_groups.json() if response_from_api_groups.status_code == 200 else []

    response_from_api_users = requests.get(f'{API_BASE_URL}/Users', verify=False)
    users = response_from_api_users.json() if response_from_api_users.status_code == 200 else []

    response_from_api_subjects = requests.get(f'{API_BASE_URL}/Subjects', verify=False)
    subjects = response_from_api_subjects.json() if response_from_api_subjects.status_code == 200 else []

    return render(request, 'AdminPanel/SubjectCRUD.html', {'groups': groups, 'users': users, 'subjects': subjects})

def edit_subject(request, id):
    if request.method == 'POST':
        updated_subject = {
            'idSubject': id,
            'nameSubject': request.POST.get('nameSubject'),
            'idGroup': request.POST.get('idGroup'),
            'userId': request.POST.get('userId'),
        }
        response = requests.put(f'{API_BASE_URL}/Subjects/{id}', json=updated_subject, verify=False)
        return redirect('subject_crud')

    response_from_api_subject = requests.get(f'{API_BASE_URL}/Subjects/{id}', verify=False)
    subject = response_from_api_subject.json() if response_from_api_subject.status_code == 200 else {}

    response_from_api_groups = requests.get(f'{API_BASE_URL}/Groups', verify=False)
    groups = response_from_api_groups.json() if response_from_api_groups.status_code == 200 else []

    response_from_api_users = requests.get(f'{API_BASE_URL}/Users', verify=False)
    users = response_from_api_users.json() if response_from_api_users.status_code == 200 else []

    return render(request, 'AdminPanel/SubjectEdit.html', {
        'subject': subject,
        'groups': groups,
        'users': users,
    })

def delete_subject(request, id):
    if request.method == 'POST':
        response = requests.delete(f'{API_BASE_URL}/Subjects/{id}', verify=False)
        return redirect('subject_crud')
    return HttpResponse(status=405)



def create_practical_work(request, subject_id):
    if request.method == 'POST':
        name_practical_work = request.POST.get('namePracticalWork')
        description_practical_work = request.POST.get('descriptionPracticalWork')
        name_file_practical_work = request.POST.get('nameFilePracticalWork')
        url_file_practical_work = request.POST.get('urlFilePracticalWork')
        user_id = request.session.get('user_id')

        # Получаем текущую дату и время
        date_upload = date.today()
        time_upload = datetime.now().time().strftime('%H:%M:%S')

        # Данные для API
        api_url = f'{API_BASE_URL}/PracticalWorks'
        data = {
            'namePracticalWork': name_practical_work,
            'descriptionPracticalWork': description_practical_work,
            'dateUploadPracticalWork': str(date_upload),
            'timeUploadPracticalWork': str(time_upload),
            'nameFilePracticalWork': name_file_practical_work,
            'urlFilePracticalWork': url_file_practical_work,
            'userId': user_id,
            'subjectId': subject_id
        }

        try:
            response = requests.post(api_url, json=data, verify=False)
            response.raise_for_status()
            return redirect('SubjectPage', id=subject_id)  
        except requests.exceptions.RequestException as e:
            return render(request, 'SubjectInfo/PracticalWork.html', {
                'error': 'Ошибка при добавлении практической работы: ' + str(e),
            })

    return render(request, 'SubjectInfo/CRUDPracticalWork.html')



def process_completed_works(completed_works, students=None):
    """
    Обрабатывает список выполненных работ
    """
    processed_works = []
    student_works = {}
    
    # Группируем работы по студентам и практическим работам
    for work in completed_works:
        user_id = work.get('userId')
        
        # Добавляем информацию о студенте
        if students:
            full_name = "Неизвестный студент"
            for student in students:
                if student.get('idUser') == user_id:
                    full_name = f"{student.get('firstName')} {student.get('secondName')} {student.get('middleName')}".strip()
                    break
            work['student_name'] = full_name
        
        # Проверяем, есть ли attemptCount в данных
        if 'attemptCount' in work:
            # Если уже есть - просто используем
            work['attempt_count'] = work['attemptCount']
        else:
            # Если нет - используем camelCase версию ключа
            if 'attemptCount' in work:
                work['attempt_count'] = work['attemptCount']
            else:
                # Если информации о попытках нет, устанавливаем по умолчанию 1
                work['attempt_count'] = 1
        
        # Группировка работ по студентам для отображения в админ-панели
        if user_id not in student_works:
            student_works[user_id] = {
                'works': [],
                'full_name': work.get('student_name', "Неизвестный студент")
            }
        
        student_works[user_id]['works'].append(work)
        processed_works.append(work)
    
    # Сортируем работы каждого студента по дате
    for user_id in student_works:
        student_works[user_id]['works'].sort(
            key=lambda x: (
                x.get('dateUploadCompletedWork', ''), 
                x.get('timeUploadCompletedWork', '')
            ),
            reverse=True  # Сначала новые
        )
    
    return processed_works, student_works





def PracticalWorkMaterial(request, idPracticalWork=None, id=None):
    # Use id parameter if idPracticalWork is not provided
    if idPracticalWork is None and id is not None:
        idPracticalWork = id
    
    # Проверяем и обновляем сессию
    if not ensure_session_valid(request):
        request.session['next_url'] = request.path
        return redirect('login')
    
    user_id = request.session['user_id']
    role_id = request.session.get('role_id')
    
    # Инициализируем переменные для работ и попыток
    latest_work = None
    completed_works = []
    used_attempts = []
    
    try:
        # Получаем информацию о практической работе
        practical_work_response = make_api_request(f'PracticalWorks/{idPracticalWork}')
        if practical_work_response['status_code'] != 200:
            return render(request, 'nullPage.html', {'message': 'Практическая работа не найдена'})
        
        practical_work = practical_work_response['data']
        
        # Получаем информацию о предмете
        subject_response = make_api_request(f'Subjects/{practical_work["subjectId"]}')
        if subject_response['status_code'] == 200:
            subject = subject_response['data']
        else:
            subject = None
        
        # Получаем сданные работы по этой практической работе
        completed_works_response = make_api_request('CompletedWorks')
        
        # Для учителей - мы будем показывать все работы по этому заданию
        students_completed_works = {}
        
        if completed_works_response['status_code'] == 200:
            # Фильтруем только работы по данной практической работе
            all_completed_works = completed_works_response['data']
            all_works_for_practical = [work for work in all_completed_works if str(work.get('practicalWorkId')) == str(idPracticalWork)]
            
            # Получаем информацию о студентах
            students_response = make_api_request('Users')
            students = {}
            
            if students_response['status_code'] == 200:
                students_data = students_response['data']
                
                # Фильтруем только студентов (роль 3)
                students_data = [student for student in students_data if student.get('idRole') == 3]
                
                # Создаем словарь студентов для быстрого доступа
                for student in students_data:
                    students[student['idUser']] = student
                
                # Обрабатываем работы в зависимости от роли пользователя
                if role_id == 3:  # Если студент
                    # Находим только работы этого студента
                    user_works = [work for work in all_works_for_practical if str(work.get('userId')) == str(user_id)]
                    
                    # Добавляем информацию о попытке в каждую работу
                    for work in user_works:
                        if 'attemptCount' in work:
                            attempt_count = int(work.get('attemptCount', 1))
                            work['attempt_count'] = attempt_count
                            
                            # Собираем уникальные номера попыток
                            if attempt_count not in used_attempts:
                                used_attempts.append(attempt_count)
                    
                    # Сортируем номера попыток
                    used_attempts.sort()
                    
                    # Выводим отладочную информацию
                    print(f"DEBUG: Работы пользователя: {len(user_works)}")
                    print(f"DEBUG: Использованные попытки: {used_attempts}")
                    
                    # Присваиваем работы в completed_works для шаблона
                    completed_works = user_works
                    
                    if user_works:
                        # Сортируем по attemptCount и статусу проверки
                        # Сначала на проверке (если есть), затем с высшим значением attemptCount
                        works_on_check = [work for work in user_works if work.get('grade') == "На проверке"]
                        checked_works = [work for work in user_works if work.get('grade') != "На проверке"]
                        
                        # Внутри каждой категории - сортировка по attemptCount
                        works_on_check.sort(key=lambda x: int(x.get('attemptCount', 0)), reverse=True)
                        checked_works.sort(key=lambda x: int(x.get('attemptCount', 0)), reverse=True)
                        
                        # Если есть работы на проверке, берем первую из них (последнюю по времени)
                        if works_on_check:
                            latest_work = works_on_check[0]
                            print(f"DEBUG: Отображаем последнюю работу НА ПРОВЕРКЕ: ID={latest_work.get('idCompletedWork')}, "
                                f"Попытка={latest_work.get('attemptCount')}, Оценка={latest_work.get('grade')}")
                        elif checked_works:  # Иначе берем проверенную с высшим attemptCount
                            latest_work = checked_works[0]
                            print(f"DEBUG: Отображаем последнюю ПРОВЕРЕННУЮ работу: ID={latest_work.get('idCompletedWork')}, "
                                f"Попытка={latest_work.get('attemptCount')}, Оценка={latest_work.get('grade')}")
                
                elif role_id == 2 or role_id == 1:  # Преподаватель или администратор
                    # Группируем работы по студентам для удобного отображения в панели преподавателя
                    for work in all_works_for_practical:
                        student_id = work.get('userId')
                        
                        if student_id in students:
                            student = students[student_id]
                            student_name = f"{student.get('firstName', '')} {student.get('secondName', '')} {student.get('middleName', '')}"
                            work['student_name'] = student_name
                            
                            # Проверяем, проверена ли работа
                            is_checked = work.get('grade') and work.get('grade') != "На проверке"
                            work['is_checked'] = is_checked
                            
                            # Добавляем в группировку по студентам
                            if student_id not in students_completed_works:
                                students_completed_works[student_id] = {
                                    'full_name': student_name,
                                    'works': []
                                }
                            students_completed_works[student_id]['works'].append(work)
                    
                    # Сортируем работы каждого студента (для преподавателя)
                    for student_id in students_completed_works:
                        students_completed_works[student_id]['works'].sort(
                            key=lambda x: (
                                x.get('dateUploadCompletedWork', ''), 
                                x.get('timeUploadCompletedWork', '')
                            ),
                            reverse=True  # Сначала новые
                        )
        
        # Статистика для преподавателя
        passed_count = 0
        not_passed_count = 0
        
        if role_id == 2 or role_id == 1:
            # Считаем только для преподавателя/админа, так как студенту это не нужно
            for student_id, student_info in students_completed_works.items():
                for work in student_info['works']:
                    if work.get('grade') in ['3', '4', '5']:
                        passed_count += 1
                    else:
                        not_passed_count += 1
        
        # Подготовка контекста с учетом роли пользователя
        context = {
            'practical_work': practical_work,
            'subject': subject,
            'role_id': role_id,
            'user_role_id': role_id, 
            'user_id': user_id,
            'is_teacher': role_id == 2,
            'is_student': role_id == 3,  # Явно устанавливаем флаг для студента
            'is_admin': role_id == 1,
            'students_completed_works': students_completed_works,
            'passed_count': passed_count if 'passed_count' in locals() else 0,
            'not_passed_count': not_passed_count if 'not_passed_count' in locals() else 0,
            'latest_work': latest_work,
            'completed_works': completed_works,
            'used_attempts': used_attempts,  # Добавляем список использованных попыток
            'total_attempts': 3,  # Общее количество доступных попыток
            'remaining_attempts': 3 - len(used_attempts)  # Оставшиеся попытки
        }
        
        # Добавляем отладочную информацию в контекст
        context['debug_attempts'] = {
            'count': len(used_attempts),
            'values': used_attempts,
            'is_student_flag': role_id == 3
        }
        
        return render(request, 'SubjectInfo/PracticalWorkMaterial.html', context)
        
    except Exception as e:
        print(f"Ошибка при получении данных практической работы: {e}")
        return redirect('AllSubjectPage')  # Было return render('nullPage.html', ...)






def delete_practical_work(request, id):
    if request.method == 'POST':
        try:
            # Получаем информацию о практической работе перед удалением
            practical_work_url = f'{API_BASE_URL}/PracticalWorks/{id}'
            response_get = requests.get(practical_work_url, verify=False)
            
            if response_get.status_code == 200:
                practical_work = response_get.json()
                subject_id = practical_work.get('subjectId')
                
                # 1. Сначала получаем все выполненные работы для данной практической работы
                completed_works_url = f'{API_BASE_URL}/CompletedWorks'
                completed_works_response = requests.get(completed_works_url, verify=False)
                
                if completed_works_response.status_code == 200:
                    completed_works = completed_works_response.json()
                    # Фильтруем работы, относящиеся к удаляемой практической работе
                    related_works = [work for work in completed_works 
                                   if work.get('practicalWorkId') == id]
                    
                    # 2. Удаляем каждую выполненную работу
                    for work in related_works:
                        delete_completed_url = f'{API_BASE_URL}/CompletedWorks/{work["idCompletedWork"]}'
                        delete_completed_response = requests.delete(delete_completed_url, verify=False)
                        print(f"Удаление выполненной работы {work['idCompletedWork']}: {delete_completed_response.status_code}")
                
                # 3. После удаления всех связанных работ удаляем саму практическую работу
                response_delete = requests.delete(practical_work_url, verify=False)
                
                if response_delete.status_code == 204:  # Успешное удаление
                    messages.success(request, 'Практическая работа и все связанные с ней попытки успешно удалены')
                    return redirect('SubjectPage', id=subject_id)
                else:
                    messages.error(request, 'Ошибка при удалении практической работы')
            else:
                messages.error(request, 'Практическая работа не найдена')
            
            # В случае ошибки возвращаемся на страницу предмета
            return redirect('SubjectPage', id=request.POST.get('subjectId'))
            
        except Exception as e:
            print(f"Ошибка при удалении: {str(e)}")
            messages.error(request, f'Произошла ошибка: {str(e)}')
            return redirect('SubjectPage', id=request.POST.get('subjectId'))
    
    # Если метод не POST
    return HttpResponse("Метод не разрешен", status=405)



def edit_practical_work(request, id):
    practical_work_url = f'{API_BASE_URL}/PracticalWorks/{id}'

    try:
        response_from_api = requests.get(practical_work_url, verify=False)
        response_from_api.raise_for_status()
        practical_work = response_from_api.json()
    except requests.exceptions.RequestException as e:
        return render(request, 'SubjectInfo/PracticalWorkEdit.html', {
            'error': 'Ошибка при получении практической работы: ' + str(e),
        })

    if request.method == 'POST':
        updated_data = {
            'idPracticalWork': id,
            'namePracticalWork': request.POST.get('namePracticalWork', practical_work['namePracticalWork']),
            'descriptionPracticalWork': request.POST.get('descriptionPracticalWork', practical_work['descriptionPracticalWork']),
            'dateUploadPracticalWork': practical_work['dateUploadPracticalWork'],
            'timeUploadPracticalWork': practical_work['timeUploadPracticalWork'],
            'nameFilePracticalWork': request.POST.get('nameFilePracticalWork', practical_work['nameFilePracticalWork']),
            'urlFilePracticalWork': request.POST.get('urlFilePracticalWork', practical_work['urlFilePracticalWork']),
            'userId': practical_work['userId'],
            'subjectId': practical_work['subjectId'],
        }

        try:
            response = requests.put(practical_work_url, json=updated_data, verify=False)
            response.raise_for_status()
            return redirect('SubjectPage', id=practical_work['subjectId'])  
        except requests.exceptions.RequestException as e:
            return render(request, 'SubjectInfo/PracticalWorkEdit.html', {
                'error': 'Ошибка при обновлении практической работы: ' + str(e),
                'practical_work': practical_work,
            })

    return render(request, 'SubjectInfo/PracticalWorkEdit.html', {'practical_work': practical_work})

def AddCompleteWork(request, practical_work_id):
    """
    Функция для добавления выполненной работы
    """
    # Получение данных о практической работе
    try:
        # Получаем данные о практической работе
        practical_work_response = make_api_request(f"PracticalWorks/{practical_work_id}")
        
        if practical_work_response['status_code'] != 200:
            # Логирование ошибки
            print(f"Ошибка API: {practical_work_response['status_code']}")
            return HttpResponse("Ошибка при получении данных о практической работе")
            
        practical_work = practical_work_response['data']
        
        # Проверяем, авторизован ли пользователь
        if 'user_id' not in request.session:
            return redirect('login')
            
        user_id = request.session['user_id']
        
        # ИСПРАВЛЕНИЕ: Получаем все работы для подсчета попыток
        print(f"Получение списка всех выполненных работ для определения номера попытки")
        completed_works_response = make_api_request("CompletedWorks")
        
        # По умолчанию - первая попытка
        attempt_count = 1
        existing_works = []
        
        if completed_works_response['status_code'] == 200 and completed_works_response['data']:
            # Фильтруем работы для конкретного пользователя и практической работы
            all_works = completed_works_response['data']
            
            # ИСПРАВЛЕНО: Более точная фильтрация работ студента
            user_works = []
            for work in all_works:
                work_user_id = work.get('userId')
                work_practical_id = work.get('practicalWorkId')
                
                # Преобразуем идентификаторы к одному типу для сравнения
                if str(work_user_id) == str(user_id) and str(work_practical_id) == str(practical_work_id):
                    user_works.append(work)
                    print(f"Найдена работа: ID={work.get('idCompletedWork')}, попытка={work.get('attemptCount')}")
            
            print(f"Найдено {len(user_works)} существующих работ пользователя {user_id} для практической работы {practical_work_id}")
            
            if user_works:
                existing_works = user_works
                # ИСПРАВЛЕНО: Используем самый большой номер попытки из существующих работ
                max_attempt = 0
                for work in user_works:
                    work_attempt = work.get('attemptCount')
                    if work_attempt and int(work_attempt) > max_attempt:
                        max_attempt = int(work_attempt)
                
                # Следующая попытка будет на 1 больше максимальной существующей
                attempt_count = max_attempt + 1
                print(f"Максимальная существующая попытка: {max_attempt}")
                print(f"Номер текущей попытки: {attempt_count}")
        else:
            print(f"Не удалось получить список работ. Статус: {completed_works_response['status_code']}")
        
        # Ограничиваем максимальное количество попыток
        max_attempts_reached = attempt_count > 3
        if max_attempts_reached:
            attempt_count = 3  # Отображаем максимум 3
        
        if request.method == 'POST':
            if max_attempts_reached:
                # Если превышено количество попыток, показываем сообщение об ошибке
                return render(request, 'SubjectInfo/AddCompleteWork.html', {
                    'practical_work': practical_work,
                    'attempt_count': 3,  # Показываем 3, так как больше быть не может
                    'max_attempts_reached': True,
                    'subject_id': practical_work.get('subjectId')
                })
            
            file_name = request.POST.get('nameFileCompletedWork')
            url_link = request.POST.get('urlFileCompletedWork')
            
            if not file_name or not url_link:
                return render(request, 'SubjectInfo/AddCompleteWork.html', {
                    'practical_work': practical_work,
                    'attempt_count': attempt_count,
                    'max_attempts_reached': max_attempts_reached,
                    'subject_id': practical_work.get('subjectId'),
                    'error': 'Необходимо указать название файла и ссылку'
                })
            
            # Отправляем работу с корректным attempt_count
            result = send_completed_work_direct(user_id, practical_work_id, file_name, url_link)
            
            if result:
                # Исправляем перенаправление, используя параметр 'id' вместо 'idPracticalWork'
                return redirect('PracticalWorkMaterial', id=practical_work_id)
            else:
                return render(request, 'SubjectInfo/AddCompleteWork.html', {
                    'practical_work': practical_work,
                    'attempt_count': attempt_count,
                    'max_attempts_reached': max_attempts_reached,
                    'subject_id': practical_work.get('subjectId'),
                    'error': 'Ошибка при отправке работы'
                })
        else:
            # GET запрос - показываем форму
            return render(request, 'SubjectInfo/AddCompleteWork.html', {
                'practical_work': practical_work,
                'attempt_count': attempt_count,
                'max_attempts_reached': max_attempts_reached,
                'subject_id': practical_work.get('subjectId')
            })
            
    except Exception as e:
        print(f"Ошибка в AddCompleteWork: {e}")
        return redirect('AllSubjectPage')  # Было return redirect('nullPage')

def send_completed_work_direct(user_id, practical_work_id, file_name, url_link):
    print("\n--- Отправка данных о выполненной работе ---")
    
    # Получаем все работы и фильтруем
    completed_works_response = make_api_request("CompletedWorks")
    
    # По умолчанию - первая попытка
    attempt_count = 1
    
    if completed_works_response['status_code'] == 200 and completed_works_response['data']:
        all_works = completed_works_response['data']
        
        # ИСПРАВЛЕНО: Более точная фильтрация и подсчет попыток
        user_works = []
        for work in all_works:
            work_user_id = work.get('userId')
            work_practical_id = work.get('practicalWorkId')
            
            # Преобразуем идентификаторы к одному типу для сравнения
            if str(work_user_id) == str(user_id) and str(work_practical_id) == str(practical_work_id):
                user_works.append(work)
                print(f"Найдена существующая работа: ID={work.get('idCompletedWork')}, попытка={work.get('attemptCount')}")
        
        print(f"Найдено {len(user_works)} работ пользователя {user_id}")
        
        if user_works:
            # Находим максимальный номер попытки
            max_attempt = 0
            for work in user_works:
                work_attempt = work.get('attemptCount')
                if work_attempt and int(work_attempt) > max_attempt:
                    max_attempt = int(work_attempt)
            
            # Следующая попытка будет на 1 больше максимальной существующей
            attempt_count = max_attempt + 1
            print(f"Максимальная существующая попытка: {max_attempt}")
            print(f"Номер новой попытки: {attempt_count}")
    
    # Проверяем, не превышено ли максимальное число попыток
    if attempt_count > 3:
        print(f"Превышено максимальное количество попыток: {attempt_count}")
        return False
    
    print(f"Установлен номер попытки: {attempt_count}")
    
    # Создаем текущую дату и время
    import datetime
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # Создаем данные для отправки
    data = {
        "NameFileCompletedWork": file_name,
        "UrlFileCompletedWork": url_link,
        "Grade": "На проверке",
        "StatusId": 2,
        "UserId": user_id,
        "PracticalWorkId": practical_work_id,
        "AttemptCount": attempt_count,
        "DateUploadCompletedWork": date_str,
        "TimeUploadCompletedWork": time_str
    }
    
    # URL для отправки данных
    url = f'{API_BASE_URL}/CompletedWorks'
    
    try:
        # Отправляем данные на сервер
        response = requests.post(url, json=data, verify=False)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code in [200, 201, 204]:
            print("Работа успешно добавлена!")
            return True
        else:
            print(f"Ошибка при добавлении работы: {response.text}")
            
            # Если первая попытка не удалась, пробуем другие варианты URL
            urls_to_try = [
                f'{API_BASE_URL}/completedworks',  # нижний регистр
                f'{API_BASE_URL}/completedWorks',  # смешанный регистр
                f'{API_BASE_URL}/CompletedWorks/',  # с закрывающим слешем
            ]
            
            for alt_url in urls_to_try:
                print(f"Пробуем альтернативный URL: {alt_url}")
                try:
                    alt_response = requests.post(alt_url, json=data, verify=False)
                    print(f"Статус ответа: {alt_response.status_code}")
                    
                    if alt_response.status_code in [200, 201, 204]:
                        print(f"Работа успешно добавлена с URL: {alt_url}")
                        return True
                except Exception as e:
                    print(f"Ошибка при использовании URL {alt_url}: {str(e)}")
            
            return False
    except Exception as e:
        print(f"Исключение при отправке данных: {str(e)}")
        return False

def grade_completed_work(request, practical_work_id, user_id):
    try:
        # Получение работ остается без изменений
        completed_works_response = make_api_request(f"CompletedWorks")
        
        if completed_works_response['status_code'] != 200 or not completed_works_response['data']:
            print(f"Не удалось получить список всех выполненных работ")
            return HttpResponse("Ошибка при получении данных о выполненных работах")
        
        completed_works = completed_works_response['data']
        user_works = [work for work in completed_works 
                      if work['userId'] == int(user_id) and work['practicalWorkId'] == int(practical_work_id)]
        
        if not user_works:
            print(f"Работа пользователя с ID {user_id} для практической работы {practical_work_id} не найдена")
            return HttpResponse("Выполненная работа не найдена")
        
        # Берем последнюю работу
        completed_work = max(user_works, key=lambda w: w.get('attemptCount', 0))
        print(f"Найдена работа пользователя: {completed_work}")
        
        # Получим список допустимых статусов
        status_response = make_api_request(f"Status")
        valid_statuses = []
        if status_response['status_code'] == 200 and status_response['data']:
            valid_statuses = status_response['data']
            print(f"Доступные статусы: {valid_statuses}")
            
            # Выведем статусы для отладки
            for status in valid_statuses:
                print(f"Статус: {status['idStatus']} - {status['nameStatus']}")
        
        if request.method == 'POST':
            grade = request.POST.get('grade')
            print(f"Полученная оценка: {grade}")
            
            # ИСПРАВЛЕННАЯ ЛОГИКА определения статуса на основе оценки
            # Вначале установим переменные для четкого понимания
            STATUS_PASSED = 1    # ID статуса "Задание сдано"
            STATUS_FAILED = 2    # ID статуса "Задание не сдано"
            
            status_id = None
            if grade:
                try:
                    # Преобразуем оценку в число если возможно, или оставляем как строку
                    grade_value = int(grade) if grade.isdigit() else grade
                    print(f"Преобразованная оценка: {grade_value}, тип: {type(grade_value)}")
                    
                    # Явно проверяем равенство и устанавливаем соответствующий статус
                    if grade_value == 2:
                        status_id = STATUS_FAILED  # Оценка 2 -> "Задание не сдано"
                        print(f"Оценка 2 -> устанавливаем статус {STATUS_FAILED} (Задание не сдано)")
                    elif grade_value in [3, 4, 5]:
                        status_id = STATUS_PASSED  # Оценки 3,4,5 -> "Задание сдано"
                        print(f"Оценка {grade_value} -> устанавливаем статус {STATUS_PASSED} (Задание сдано)")
                    else:
                        # Если оценка не 2,3,4,5 - берем статус из формы или оставляем текущий
                        status_id = request.POST.get('statusId', completed_work['statusId'])
                        print(f"Оценка {grade_value} не распознана -> используем статус из формы: {status_id}")
                except Exception as e:
                    print(f"Ошибка при определении статуса по оценке: {str(e)}")
                    status_id = request.POST.get('statusId', completed_work['statusId'])
            else:
                # Если оценка не указана, берем статус из формы
                status_id = request.POST.get('statusId', completed_work['statusId'])
                print(f"Оценка не указана -> используем статус из формы: {status_id}")
            
            print(f"Итоговые данные: grade={grade}, statusId={status_id}")
            
            # Создаем копию оригинального объекта, чтобы сохранить все поля
            updated_work = completed_work.copy()
            
            # Обновляем только необходимые поля
            updated_work['grade'] = grade
            if status_id:
                updated_work['statusId'] = int(status_id)
            
            # В случае, если в базе идентификаторы называются по-другому
            if 'statusId' not in updated_work and 'StatusId' in updated_work:
                updated_work['StatusId'] = int(status_id) if status_id else updated_work['StatusId']
            
            print(f"Отправляем объект для обновления: {updated_work}")
            
            # Используем правильный URL для обновления данных
            update_url = f"{API_BASE_URL}/CompletedWorks/{completed_work['idCompletedWork']}"
            print(f"Обновляем оценку по URL: {update_url}")
            
            try:
                # Явно указываем заголовок Content-Type
                headers = {'Content-Type': 'application/json'}
                response = requests.put(update_url, json=updated_work, headers=headers, verify=False)
                print(f"Статус обновления: {response.status_code}")
                
                if response.status_code in [200, 201, 204]:
                    # Исправленное перенаправление - используем 'id' вместо 'idPracticalWork'
                    return redirect('PracticalWorkMaterial', id=practical_work_id)
                else:
                    print(f"Ответ сервера: {response.text}")
                    return HttpResponse(f"Ошибка при обновлении оценки: {response.status_code}, {response.text}")
            except Exception as e:
                print(f"Исключение при обновлении: {str(e)}")
                return HttpResponse(f"Ошибка при обновлении оценки: {str(e)}")
                
        # Код для GET-запроса остается без изменений
        practical_work_response = make_api_request(f"PracticalWorks/{practical_work_id}")
        if practical_work_response['status_code'] != 200:
            return HttpResponse("Ошибка при получении данных о практической работе")
        
        practical_work = practical_work_response['data']
        
        context = {
            'completed_work': completed_work,
            'practical_work': practical_work,
            'user_id': user_id,
            'statuses': valid_statuses
        }
        
        return render(request, 'SubjectInfo/GradeCompletedWork.html', context)
        
    except Exception as e:
        print(f"Исключение в функции grade_completed_work: {str(e)}")
        return HttpResponse(f"Произошла ошибка: {str(e)}")


def create_test(request, subject_id):
    if request.method == 'POST':
        try:
            # Создаем тест
            test_data = {
                'nameTest': request.POST.get('nameTest'),
                'descriptionTest': request.POST.get('descriptionTest'),
                'timeLimit': int(request.POST.get('timeLimit')),
                'subjectId': subject_id
            }
            
            test_url = f'{API_BASE_URL}/Tests'
            response = requests.post(test_url, json=test_data, verify=False)
            
            if response.status_code not in [200, 201]:
                messages.error(request, 'Ошибка при создании теста')
                return redirect('create_test', subject_id=subject_id)
            
            test = response.json()
            test_id = test.get('idTest')
            
            # Создаем критерии оценивания
            criteria_url = f'{API_BASE_URL}/GradingCriterions'
            
            # Создаем критерии для каждой оценки - используем только один способ создания критериев
            criteria_data = [
                {
                    'idTest': test_id,
                    'grade': 5,
                    'minPoints': int(float(request.POST.get('grade5Min'))),  # Преобразуем в целое число
                    'maxPoints': int(float(request.POST.get('grade5Max')))   # Преобразуем в целое число
                },
                {
                    'idTest': test_id,
                    'grade': 4,
                    'minPoints': int(float(request.POST.get('grade4Min'))),
                    'maxPoints': int(float(request.POST.get('grade4Max')))
                },
                {
                    'idTest': test_id,
                    'grade': 3,
                    'minPoints': int(float(request.POST.get('grade3Min'))),
                    'maxPoints': int(float(request.POST.get('grade3Max')))
                }
            ]

            # Отправляем каждый критерий
            for criterion in criteria_data:
                response = requests.post(criteria_url, json=criterion, verify=False)
                print(f"Создание критерия для оценки {criterion['grade']}:")
                print(f"Отправленные данные: {criterion}")
                print(f"Статус ответа: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
                
                if response.status_code not in [200, 201]:
                    messages.warning(request, f'Ошибка при создании критерия для оценки {criterion["grade"]}')

            # Остальной код остается без изменений...

            # Получаем вопросы из формы
            questions_json = request.POST.get('questions')
            if questions_json:
                try:
                    questions = json.loads(questions_json)
                    # Создаем вопросы
                    questions_url = f'{API_BASE_URL}/QuestionsTests'
                    for question in questions:
                        question_data = {
                            'questionText': question['text'],
                            'questionType': question['type'],
                            'points': question['points'],
                            'correctAnswer': question['correctAnswer'],
                            'answerVariants': '; '.join(question['answers']) if question['answers'] else '',
                            'idTest': test_id
                        }
                        response = requests.post(questions_url, json=question_data, verify=False)
                        if response.status_code not in [200, 201]:
                            print(f"Ошибка при создании вопроса: {response.status_code}")
                            print(f"Ответ сервера: {response.text}")
                except json.JSONDecodeError as e:
                    print(f"Ошибка при разборе JSON вопросов: {e}")
            
            messages.success(request, 'Тест успешно создан')
            return redirect('test_material', id=test_id)
            
        except Exception as e:
            print(f"Ошибка при создании теста: {str(e)}")
            messages.error(request, f'Ошибка при создании теста: {str(e)}')
            return redirect('create_test', subject_id=subject_id)
    
    # GET запрос - показываем форму создания теста
    return render(request, 'SubjectInfo/CreateTest.html', {
        'subject_id': subject_id
    })

def get_test_questions(test_id):
    """Вспомогательная функция для получения вопросов теста"""
    questions_response = make_api_request('QuestionsTests')
    if questions_response['status_code'] == 200 and questions_response['data']:
        # Фильтруем вопросы для конкретного теста по idTest
        questions = [q for q in questions_response['data'] if q.get('idTest') == int(test_id)]
        print(f"Получено {len(questions)} вопросов для теста {test_id}")
        return questions
    return []


def test_material(request, id):
    # Получаем данные о тесте
    logger.info(f"Получение данных теста с ID: {id}")
    response = make_api_request(f'Tests/{id}')
    
    # Проверяем статус код в словаре
    status_code = response['status_code']
    test_data = response['data'] if status_code == 200 else None
    
    if status_code == 200 and test_data:
        test = test_data
        
        # Получаем имя предмета
        subject_name = ""
        subject_id = test.get('subjectId')
        if subject_id:
            subject_response = make_api_request(f'Subjects/{subject_id}')
            subject_status_code = subject_response['status_code']
            subject_data = subject_response['data'] if subject_status_code == 200 else None
                
            if subject_status_code == 200 and subject_data:
                subject = subject_data
                subject_name = subject.get('nameSubject', '')
        
        # Определяем роль пользователя
        role_id = request.session.get('role_id')
        is_teacher = role_id in [1, 2]  # Администратор или преподаватель
        is_student = role_id == 3       # Студент
        
        # Инициализируем переменные
        questions = []
        grading_criteria = []
        
        # Получаем вопросы теста ТОЛЬКО для преподавателей
        if is_teacher:
            print(f"Получение вопросов для преподавателя, тест ID: {id}")
            questions = get_test_questions(id)
        
        # Получаем критерии оценивания для конкретного теста
        print(f"Получение критериев оценивания для теста ID: {id}")
        criteria_response = make_api_request('GradingCriterions')
        if criteria_response['status_code'] == 200 and criteria_response['data']:
            # Фильтруем критерии только для текущего теста
            all_criteria = criteria_response['data']
            grading_criteria = [
                criterion for criterion in all_criteria 
                if criterion.get('idTest') == int(id)  # Убедитесь, что типы совпадают
            ]
            print(f"Получено {len(grading_criteria)} критериев оценивания для теста {id}")
            print(f"Критерии: {grading_criteria}")  # Добавляем для отладки
        else:
            print(f"Ошибка при получении критериев оценивания: {criteria_response['status_code']}")
            print(f"Ответ сервера: {criteria_response.get('data')}")  # Добавляем для отладки
        
        # Сортируем критерии по оценке (от высшей к низшей)
        if grading_criteria:
            grading_criteria.sort(key=lambda x: float(x.get('grade', 0)), reverse=True)
        
        context = {
            'test': test,
            'questions': questions,
            'grading_criteria': grading_criteria,
            'teacher_view': is_teacher,
            'student_view': is_student,
            'subject_name': subject_name,
            'subject_id': subject_id,
            'show_debug': True,  # Включаем отладочную информацию
            'debug_info': {
                'criteria_response': criteria_response,
                'test_id': id,
                'found_criteria': grading_criteria
            }
        }
        
        # Если пользователь - студент, добавляем информацию о попытках
        if is_student:
            user_id = request.session.get('user_id')
            if user_id:
                # Получаем все попытки
                attempts_url = f'{API_BASE_URL}/TestAttempts'
                try:
                    response = requests.get(attempts_url, verify=False)
                    all_attempts = response.json() if response.status_code == 200 else []
                    
                    # Фильтруем попытки для конкретного теста и пользователя
                    attempts = [
                        attempt for attempt in all_attempts 
                        if str(attempt.get('testId')) == str(id) 
                        and str(attempt.get('userId')) == str(user_id)
                    ]
                    
                    print(f"DEBUG: Найдено {len(attempts)} попыток для теста {id} и пользователя {user_id}")
                    for attempt in attempts:
                        print(f"DEBUG: Попытка: {attempt}")
                    
                    # Инициализируем переменные
                    attempts_count = len(attempts)
                    max_attempts = 3
                    remaining_attempts = max(0, max_attempts - attempts_count)
                    latest_attempt = None
                    can_retake = True
                    
                    # Получаем последнюю попытку, если есть
                    if attempts:
                        # Сортируем по времени окончания
                        attempts.sort(
                            key=lambda x: x.get('endTime', '0') or '0', 
                            reverse=True
                        )
                        latest_attempt = attempts[0]
                        print(f"DEBUG: Последняя попытка: {latest_attempt}")
                        
                        # Проверка на успешное прохождение
                        try:
                            grade = latest_attempt.get('grade')
                            if grade:
                                grade = float(grade)
                                if grade >= 3:
                                    can_retake = False
                                    print(f"DEBUG: Тест уже сдан с оценкой {grade}")
                                else:
                                    can_retake = remaining_attempts > 0
                                    print(f"DEBUG: Тест не сдан, оценка {grade}, осталось попыток: {remaining_attempts}")
                            else:
                                print("DEBUG: Оценка отсутствует")
                        except (ValueError, TypeError) as e:
                            print(f"DEBUG: Ошибка при обработке оценки: {e}")
                            can_retake = remaining_attempts > 0
                    
                    context.update({
                        'attempts': attempts,
                        'attempts_count': attempts_count,
                        'max_attempts': max_attempts,
                        'remaining_attempts': remaining_attempts,
                        'latest_attempt': latest_attempt,
                        'can_retake': can_retake
                    })
                    
                except Exception as e:
                    print(f"Ошибка при получении попыток теста: {e}")
                    context.update({
                        'attempts': [],
                        'attempts_count': 0,
                        'max_attempts': 3,
                        'remaining_attempts': 3,
                        'latest_attempt': None,
                        'can_retake': True
                    })
    
        return render(request, 'SubjectInfo/TestMaterial.html', context)


def start_test(request, id):
    """Функция для начала прохождения теста."""
    # Получаем информацию о тесте
    test_url = f'{API_BASE_URL}/Tests/{id}'
    try:
        response = requests.get(test_url, verify=False)
        test = response.json() if response.status_code == 200 else {}
        
        if not test:
            messages.error(request, 'Не удалось загрузить информацию о тесте.')
            return redirect('test_material', id=id)
    except:
        messages.error(request, 'Не удалось загрузить информацию о тесте.')
        return redirect('test_material', id=id)

    # Получаем вопросы теста
    questions_url = f'{API_BASE_URL}/QuestionsTests'
    try:
        # Получаем все вопросы
        response_questions = requests.get(questions_url, verify=False)
        all_questions = response_questions.json() if response_questions.status_code == 200 else []
        
        # Фильтруем вопросы только для текущего теста
        questions = [
            question for question in all_questions 
            if str(question.get('idTest')) == str(id)
        ]
        
        print(f"DEBUG: Найдено {len(questions)} вопросов для теста {id}")
        
        if not questions:
            messages.error(request, 'Для этого теста не найдены вопросы.')
            return redirect('test_material', id=id)
    except Exception as e:
        print(f"Ошибка при получении вопросов: {e}")
        messages.error(request, 'Не удалось загрузить вопросы теста.')
        return redirect('test_material', id=id)

    # Создаем запись о начале тестирования
    user_id = request.session.get('user_id')
    
    # Текущая дата и время
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Текущая дата и время в ISO формате
    start_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    
    # Записываем начало попытки
    attempt_data = {
        'dateTestAttempt': current_date,
        'timeTestAttempt': current_time,
        'score': 0,
        'testId': id,
        'userId': user_id,
        'startTime': start_time,  # Добавляем время начала
        'endTime': None,  # Время окончания пока null
        'status': 'InProgress'  # Добавляем статус
    }
    
    # Создаем новую попытку через API
    attempt_id = None
    try:
        attempt_url = f'{API_BASE_URL}/TestAttempts'
        response = requests.post(attempt_url, json=attempt_data, verify=False)
        if response.status_code in [200, 201]:
            attempt = response.json()
            attempt_id = attempt.get('idTestAttempt')
    except Exception as e:
        print(f"Ошибка при создании попытки: {e}")

    # Выводим вопросы для тестирования
    return render(request, 'SubjectInfo/TestProcess.html', {
        'test': test,
        'questions': questions,
        'time_limit': test.get('timeLimit', 60),
        'attempt_id': attempt_id,
        'start_time': start_time  # Передаем время начала в шаблон
    })


def submit_test(request, id):
    print("\n=== НАЧАЛО ПРОВЕРКИ ТЕСТА ===")
    
    try:
        # Получаем user_id из сессии в начале функции
        user_id = request.session.get('user_id')
        if not user_id:
            raise Exception("Пользователь не авторизован")

        # Инициализируем переменные для подсчета баллов
        total_score = 0
        max_score = 0
        
        # Получаем все вопросы теста
        questions_response = make_api_request(f"QuestionsTests")
        if questions_response['status_code'] != 200:
            raise Exception("Не удалось получить вопросы теста")
            
        questions = [q for q in questions_response['data'] 
                    if str(q.get('idTest')) == str(id)]
        
        # Проверяем каждый вопрос
        for question in questions:
            question_id = question.get('idQuestion')
            question_type = question.get('questionType')
            max_score += question.get('points', 0)
            
            print(f"\nПроверка вопроса {question_id} (тип {question_type}):")
            print(f"Текст вопроса: {question.get('questionText')}")
            
            # Проверяем ответ в зависимости от типа вопроса
            if question_type == 1:  # Один правильный ответ
                total_score += check_single_choice(request, question_id, question)
            elif question_type == 2:  # Несколько правильных ответов
                total_score += check_multiple_choice(request, question_id, question)
            elif question_type == 3:  # Сопоставление
                total_score += check_matching(request, question_id, question)
            elif question_type == 4:  # Ввод ответа
                total_score += check_text_input(request, question_id, question)
            elif question_type == 5:  # Установление порядка
                total_score += check_ordering(request, question_id, question)
                
        print(f"\nИтоговый результат: {total_score} из {max_score} баллов")
        
        # Сохраняем результаты
        current_datetime = datetime.now()
        end_time = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        
        # Рассчитываем оценку
        grade = calculate_grade(total_score, max_score, id)
        
        # Получаем ID попытки из формы
        attempt_id = request.POST.get('attempt_id')
        
        # Подготавливаем данные для сохранения
        attempt_data = {
            'testId': int(id),
            'userId': int(user_id),
            'score': total_score,
            'maxScore': max_score,
            'grade': grade,
            'startTime': request.POST.get('start_time'),
            'endTime': end_time,
            'status': 'Completed'
        }
        
        # Если есть ID попытки, добавляем его
        if attempt_id and attempt_id.lower() != 'none':
            attempt_data['idTestAttempt'] = int(attempt_id)
            # Обновляем существующую попытку
            response = requests.put(
                f'{API_BASE_URL}/TestAttempts/{attempt_id}',
                json=attempt_data,
                verify=False
            )
        else:
            # Создаем новую попытку
            response = requests.post(
                f'{API_BASE_URL}/TestAttempts',
                json=attempt_data,
                verify=False
            )
        
        if response.status_code in [200, 201, 204]:
            messages.success(
                request, 
                f'Тест успешно завершен! Ваш результат: {total_score} из {max_score} баллов. Оценка: {grade}'
            )
            return redirect('test_results', id=id)
        else:
            print(f"Ошибка сохранения результатов: {response.status_code}")
            print(f"Ответ сервера: {response.text}")
            raise Exception(f"Ошибка сохранения результатов: {response.status_code}")
            
    except Exception as e:
        print(f"Ошибка при отправке результатов теста: {e}")
        messages.error(request, f'Произошла ошибка при отправке результатов теста: {str(e)}')
        return redirect('test_material', id=id)

def calculate_grade(score, max_score, test_id):
    """Функция для расчета оценки на основе критериев оценивания"""
    try:
        # Получаем критерии оценивания для конкретного теста
        criteria_response = make_api_request('GradingCriterions')
        if criteria_response['status_code'] != 200:
            return calculate_default_grade(score, max_score)
            
        # Фильтруем критерии только для текущего теста
        all_criteria = criteria_response['data']
        criteria = [
            criterion for criterion in all_criteria 
            if str(criterion.get('idTest')) == str(test_id)
        ]
        
        if not criteria:
            return calculate_default_grade(score, max_score)
        
        print(f"\nПодсчет оценки для теста {test_id}:")
        print(f"Набрано баллов: {score}")
        print(f"Максимум баллов: {max_score}")
        print("Критерии оценивания:")
        for criterion in criteria:
            print(f"Оценка {criterion['grade']}: {criterion['minPoints']}-{criterion['maxPoints']} баллов")
        
        # Сортируем критерии по оценке (от высшей к низшей)
        sorted_criteria = sorted(criteria, key=lambda x: float(x['grade']), reverse=True)
        
        # Проходим по критериям и находим подходящую оценку
        for criterion in sorted_criteria:
            min_points = float(criterion['minPoints'])
            max_points = float(criterion['maxPoints'])
            
            if min_points <= score <= max_points:
                print(f"Итоговая оценка: {criterion['grade']} (набрано {score} баллов)")
                return criterion['grade']
        
        # Если набрано меньше минимума - ставим 2
        print(f"Набрано баллов меньше минимума, оценка: 2")
        return 2
        
    except Exception as e:
        print(f"Ошибка при расчете оценки: {e}")
        return calculate_default_grade(score, max_score)

def calculate_default_grade(score, max_score):
    """Стандартная шкала оценок, если критерии недоступны"""
    if max_score == 0:
        return 2
        
    percentage = (score / max_score) * 100
    
    if percentage >= 85:
        return 5
    elif percentage >= 70:
        return 4
    elif percentage >= 50:
        return 3
    else:
        return 2

def test_results(request, id):
    """Функция для отображения результатов теста."""
    try:
        # Получаем информацию о тесте
        test_url = f'{API_BASE_URL}/Tests/{id}'
        response = requests.get(test_url, verify=False)
        test = response.json() if response.status_code == 200 else {}

        user_id = request.session.get('user_id')
        
        # Получаем попытки прохождения теста для текущего пользователя
        try:
            attempts_url = f'{API_BASE_URL}/TestAttempts'
            response_attempts = requests.get(attempts_url, verify=False)
            
            if response_attempts.status_code == 200:
                all_attempts = response_attempts.json()
                
                # Фильтруем попытки только для текущего пользователя и теста
                attempts = [
                    attempt for attempt in all_attempts 
                    if str(attempt.get('testId')) == str(id) 
                    and str(attempt.get('userId')) == str(user_id)
                ]
                
                print(f"DEBUG: Найдено {len(attempts)} попыток для теста {id} и пользователя {user_id}")
                
                # Сортируем попытки по времени окончания (от новых к старым)
                attempts.sort(
                    key=lambda x: x.get('endTime', '0'),
                    reverse=True
                )
                
                # Берем последнюю попытку (первую в отсортированном списке)
                latest_attempt = attempts[0] if attempts else None
                
                attempts_count = len(attempts)
                max_attempts = 3
                remaining_attempts = max(0, max_attempts - attempts_count)
                
                # Определяем, может ли пользователь пересдать тест
                can_retake = True
                if latest_attempt:
                    try:
                        grade = float(latest_attempt.get('grade', 0))
                        if grade >= 3:
                            can_retake = False
                        else:
                            can_retake = remaining_attempts > 0
                    except (ValueError, TypeError):
                        can_retake = remaining_attempts > 0
                
            else:
                attempts = []
                latest_attempt = None
                attempts_count = 0
                remaining_attempts = 3
                can_retake = True
                
        except Exception as e:
            print(f"Ошибка при получении попыток: {e}")
            attempts = []
            latest_attempt = None
            attempts_count = 0
            remaining_attempts = 3
            can_retake = True
        
        # Получаем критерии оценивания только для текущего теста
        try:
            criteria_url = f'{API_BASE_URL}/GradingCriterions'
            response_criteria = requests.get(criteria_url, verify=False)
            
            if response_criteria.status_code == 200:
                all_criteria = response_criteria.json()
                # Фильтруем критерии только для текущего теста
                grading_criteria = [
                    criterion for criterion in all_criteria 
                    if str(criterion.get('idTest')) == str(id)
                ]
                # Сортируем по оценке (от высшей к низшей)
                grading_criteria.sort(key=lambda x: float(x.get('grade', 0)), reverse=True)
                
                print(f"DEBUG: Найдено {len(grading_criteria)} критериев для теста {id}")
            else:
                grading_criteria = []
                print(f"DEBUG: Ошибка при получении критериев: {response_criteria.status_code}")
        except Exception as e:
            print(f"DEBUG: Ошибка при обработке критериев: {e}")
            grading_criteria = []
        
        return render(request, 'SubjectInfo/TestResults.html', {
            'test': test,
            'attempts': attempts,
            'latest_attempt': latest_attempt,
            'can_retake': can_retake,
            'remaining_attempts': remaining_attempts,
            'grading_criteria': grading_criteria,  # Отфильтрованные критерии
            'attempts_count': attempts_count,
            'max_attempts': max_attempts
        })
        
    except Exception as e:
        print(f"Ошибка при получении результатов теста: {e}")
        messages.error(request, 'Произошла ошибка при получении результатов теста')
        return redirect('test_material', id=id)

def test_attempts(request, id):
    """
    Функция для отображения всех попыток прохождения теста для преподавателя.
    """
    # Получаем информацию о тесте
    test_url = f'{API_BASE_URL}/Tests/{id}'
    try:
        response = requests.get(test_url, verify=False)
        test = response.json() if response.status_code == 200 else {}
    except:
        messages.error(request, 'Не удалось загрузить информацию о тесте.')
        return redirect('SubjectPage', id=1)
    
    # Получаем все попытки прохождения теста
    attempts_url = f'{API_BASE_URL}/TestAttempts/test/{id}'
    try:
        response_attempts = requests.get(attempts_url, verify=False)
        attempts = response_attempts.json() if response_attempts.status_code == 200 else []
    except:
        attempts = []
    
    # Группируем попытки по пользователям
    user_attempts = {}
    for attempt in attempts:
        user_id = attempt['userId']
        if user_id not in user_attempts:
            # Получаем информацию о пользователе
            user_url = f'{API_BASE_URL}/Users/{user_id}'
            try:
                response_user = requests.get(user_url, verify=False)
                user = response_user.json() if response_user.status_code == 200 else {}
                full_name = f"{user.get('firstName', 'Не указано')} {user.get('secondName', 'Не указано')} {user.get('middleName', 'Не указано')}"
            except:
                full_name = 'Неизвестный пользователь'
            
            user_attempts[user_id] = {
                'full_name': full_name,
                'attempts': []
            }
        
        user_attempts[user_id]['attempts'].append(attempt)
    
    # Для каждого пользователя сортируем попытки по дате и времени
    for user_id in user_attempts:
        user_attempts[user_id]['attempts'].sort(key=lambda x: (x['dateTestAttempt'], x['timeTestAttempt']), reverse=True)
    
    return render(request, 'SubjectInfo/TestAttempts.html', {
        'test': test,
        'user_attempts': user_attempts
    })


def test_students_results(request, id):
    """
    Функция для отображения результатов теста всех студентов для преподавателя.
    """
    # Получаем информацию о тесте
    test_url = f'{API_BASE_URL}/Tests/{id}'
    try:
        response = requests.get(test_url, verify=False)
        test = response.json() if response.status_code == 200 else {}
        subject_id = test.get('subjectId')
    except:
        messages.error(request, 'Не удалось загрузить информацию о тесте.')
        return redirect('SubjectPage', id=1)
    
    # Получаем информацию о предмете
    subject_url = f'{API_BASE_URL}/Subjects/{subject_id}'
    try:
        response_subject = requests.get(subject_url, verify=False)
        subject = response_subject.json() if response_subject.status_code == 200 else {}
        group_id = subject.get('idGroup')
    except:
        group_id = None
    
    # Получаем студентов группы
    students = []
    if group_id:
        students_url = f'{API_BASE_URL}/Users'
        try:
            response_students = requests.get(students_url, verify=False)
            all_users = response_students.json() if response_students.status_code == 200 else []
            # Фильтруем только студентов (role_id = 3) из нужной группы
            students = [user for user in all_users if user.get('idRole') == 3 and user.get('idGroup') == group_id]
        except:
            students = []
    
    # Получаем все попытки прохождения теста
    attempts_url = f'{API_BASE_URL}/TestAttempts'
    try:
        response_attempts = requests.get(attempts_url, verify=False)
        all_attempts = response_attempts.json() if response_attempts.status_code == 200 else []
        
        print(f"Получено попыток: {len(all_attempts)}")
        print(f"ID теста для фильтрации: {id}")
        
        # Фильтруем попытки только для текущего теста
        test_attempts = [
            attempt for attempt in all_attempts 
            if str(attempt.get('testId')) == str(id)
        ]
        
        print(f"Отфильтровано попыток для теста {id}: {len(test_attempts)}")
    except Exception as e:
        print(f"Ошибка при получении попыток: {e}")
        test_attempts = []
    
    # Для каждого студента находим его попытки
    for student in students:
        student_id = student['idUser']
        # Фильтруем попытки только для текущего студента и текущего теста
        student_attempts = [
            attempt for attempt in test_attempts 
            if str(attempt.get('userId')) == str(student_id)
        ]
        
        if student_attempts:
            # Сортируем попытки по дате и времени (от новых к старым)
            student_attempts.sort(
                key=lambda x: (x.get('endTime', '') or ''),
                reverse=True
            )
            
            # Обрабатываем каждую попытку
            for attempt in student_attempts:
                if 'endTime' in attempt:
                    try:
                        # Разбираем строку ISO datetime
                        end_time = attempt['endTime'].split('T')
                        attempt['dateTestAttempt'] = end_time[0]  # Дата
                        attempt['timeTestAttempt'] = end_time[1].split('.')[0]  # Время
                    except (IndexError, AttributeError):
                        attempt['dateTestAttempt'] = 'Нет данных'
                        attempt['timeTestAttempt'] = 'Нет данных'
                else:
                    attempt['dateTestAttempt'] = 'Нет данных'
                    attempt['timeTestAttempt'] = 'Нет данных'
            
            # Находим лучшую попытку (с максимальным баллом)
            best_attempt = max(student_attempts, key=lambda x: float(x.get('score', 0)))
            student['best_attempt'] = best_attempt
            student['all_attempts'] = student_attempts
            student['attempts_count'] = len(student_attempts)
            student['has_passed'] = float(best_attempt.get('grade', 0)) >= 3
        else:
            student['best_attempt'] = None
            student['all_attempts'] = []
            student['attempts_count'] = 0
            student['has_passed'] = False
    
    # Статистика
    total_students = len(students)
    passed_students = sum(1 for student in students if student['has_passed'])
    not_passed_students = total_students - passed_students
    
    context = {
        'test': test,
        'students': students,
        'total_students': total_students,
        'passed_students': passed_students,
        'not_passed_students': not_passed_students,
        'subject': subject
    }
    
    return render(request, 'SubjectInfo/TestStudentsResults.html', context)


def edit_test(request, id):
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            test_data = {
                'idTest': id,
                'nameTest': request.POST.get('nameTest'),
                'descriptionTest': request.POST.get('descriptionTest'),
                'timeLimit': int(request.POST.get('timeLimit')),
                'subjectId': int(request.POST.get('subjectId'))
            }
            
            # Обновляем тест
            test_url = f'{API_BASE_URL}/Tests/{id}'
            response = requests.put(test_url, json=test_data, verify=False)
            
            if response.status_code not in [200, 204]:
                messages.error(request, 'Ошибка при обновлении теста')
                return redirect('edit_test', id=id)

            # Обновляем критерии оценивания
            criteria_url = f'{API_BASE_URL}/GradingCriterions'
            
            # Получаем существующие критерии
            existing_criteria_response = make_api_request('GradingCriterions')
            if existing_criteria_response['status_code'] == 200:
                existing_criteria = [
                    c for c in existing_criteria_response['data'] 
                    if c.get('idTest') == int(id)
                ]
                
                # Удаляем существующие критерии
                for criterion in existing_criteria:
                    # Используем правильное имя поля idCriteria
                    delete_url = f'{API_BASE_URL}/GradingCriterions/{criterion["idCriteria"]}'
                    requests.delete(delete_url, verify=False)

            # Создаем новые критерии без поля idCriteria
            new_criteria = [
                {
                    'idTest': id,
                    'grade': 5,
                    'minPoints': int(request.POST.get('grade5Min')),
                    'maxPoints': int(request.POST.get('grade5Max'))
                },
                {
                    'idTest': id,
                    'grade': 4,
                    'minPoints': int(request.POST.get('grade4Min')),
                    'maxPoints': int(request.POST.get('grade4Max'))
                },
                {
                    'idTest': id,
                    'grade': 3,
                    'minPoints': int(request.POST.get('grade3Min')),
                    'maxPoints': int(request.POST.get('grade3Max'))
                }
            ]

            # Отправляем новые критерии
            for criterion in new_criteria:
                response = requests.post(criteria_url, json=criterion, verify=False)
                if response.status_code not in [200, 201]:
                    print(f"Ошибка при создании критерия: {response.status_code}")
                    print(f"Отправленные данные: {criterion}")
                    print(f"Ответ сервера: {response.text}")
                    messages.warning(request, f'Ошибка при обновлении критерия для оценки {criterion["grade"]}')

            # Остальной код для обработки вопросов остается без изменений...
            
            messages.success(request, 'Тест успешно обновлен')
            return redirect('test_material', id=id)
            
        except Exception as e:
            print(f"Ошибка при сохранении теста: {str(e)}")
            messages.error(request, f'Ошибка при сохранении теста: {str(e)}')
            return redirect('edit_test', id=id)
    
    # GET запрос
    try:
        # Получаем данные о тесте
        test_response = make_api_request(f'Tests/{id}')
        if test_response['status_code'] != 200:
            messages.error(request, 'Тест не найден')
            return redirect('index')
        
        test = test_response['data']
        
        # Получаем вопросы теста используя общую функцию
        questions = get_test_questions(id)
        
        # Получаем критерии оценивания
        criteria_response = make_api_request('GradingCriterions')
        if criteria_response['status_code'] == 200:
            # Фильтруем критерии только для текущего теста
            grading_criteria = [
                c for c in criteria_response['data'] 
                if c.get('idTest') == int(id)
            ]
            # Сортируем по оценке (от высшей к низшей)
            grading_criteria.sort(key=lambda x: float(x.get('grade', 0)), reverse=True)
        else:
            grading_criteria = []
        
        context = {
            'test': test,
            'questions': questions,
            'grading_criteria': grading_criteria
        }
        
        return render(request, 'SubjectInfo/EditTest.html', context)

    except Exception as e:
        print(f"Ошибка при загрузке теста: {str(e)}")
        messages.error(request, f'Ошибка при загрузке теста: {str(e)}')
        return redirect('index')

def delete_test(request, id):
    """
    Функция для удаления теста.
    """
    if request.method == 'POST':
        try:
            # Получаем информацию о тесте для получения subject_id
            test_url = f'{API_BASE_URL}/Tests/{id}'
            response = requests.get(test_url, verify=False)
            
            if response.status_code != 200:
                messages.error(request, 'Тест не найден')
                return redirect('AllSubjectPage')
                
            test = response.json()
            subject_id = test.get('subjectId')

            # Сначала удаляем все попытки прохождения теста
            attempts_url = f'{API_BASE_URL}/TestAttempts'
            attempts_response = requests.get(attempts_url, verify=False)
            if attempts_response.status_code == 200:
                attempts = attempts_response.json()
                # Фильтруем попытки для данного теста
                test_attempts = [a for a in attempts if str(a.get('testId')) == str(id)]
                
                # Удаляем каждую попытку
                for attempt in test_attempts:
                    attempt_id = attempt.get('idTestAttempt')
                    delete_attempt_url = f'{API_BASE_URL}/TestAttempts/{attempt_id}'
                    requests.delete(delete_attempt_url, verify=False)

            # Удаляем все вопросы теста
            questions_url = f'{API_BASE_URL}/QuestionsTests'
            questions_response = requests.get(questions_url, verify=False)
            if questions_response.status_code == 200:
                questions = questions_response.json()
                # Фильтруем вопросы для данного теста
                test_questions = [q for q in questions if str(q.get('idTest')) == str(id)]
                
                # Удаляем каждый вопрос
                for question in test_questions:
                    question_id = question.get('idQuestion')
                    delete_question_url = f'{API_BASE_URL}/QuestionsTests/{question_id}'
                    requests.delete(delete_question_url, verify=False)

            # Удаляем критерии оценивания
            criteria_url = f'{API_BASE_URL}/GradingCriterions'
            criteria_response = requests.get(criteria_url, params={'testId': id}, verify=False)
            if criteria_response.status_code == 200:
                criteria = criteria_response.json()
                # Фильтруем критерии для данного теста
                test_criteria = [c for c in criteria if str(c.get('testId')) == str(id)]
                
                # Удаляем каждый критерий
                for criterion in test_criteria:
                    criterion_id = criterion.get('idGradingCriterion')
                    delete_criterion_url = f'{API_BASE_URL}/GradingCriterions/{criterion_id}'
                    requests.delete(delete_criterion_url, verify=False)

            # Наконец, удаляем сам тест
            response = requests.delete(test_url, verify=False)
            if response.status_code == 204:
                messages.success(request, 'Тест успешно удален')
                return redirect('SubjectPage', id=subject_id)
            else:
                messages.error(request, 'Ошибка при удалении теста')
                return redirect('test_material', id=id)
                
        except Exception as e:
            messages.error(request, f'Ошибка при удалении теста: {str(e)}')
            return redirect('AllSubjectPage')
            
    return HttpResponse(status=405)  # Method Not Allowed

def check_api_access(request):
    """
    Функция для проверки соединения с API
    """
    try:
        # Проверяем доступ к основным эндпоинтам
        users_response = make_api_request('Users')
        subjects_response = make_api_request('Subjects')
        groups_response = make_api_request('Groups')
        
        status = {
            'users': {
                'status': users_response.status_code,
                'message': 'OK' if users_response.status_code == 200 else 'Failed'
            },
            'subjects': {
                'status': subjects_response.status_code,
                'message': 'OK' if subjects_response.status_code == 200 else 'Failed'
            },
            'groups': {
                'status': groups_response.status_code,
                'message': 'OK' if groups_response.status_code == 200 else 'Failed'
            }
        }
        
        return JsonResponse(status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def ensure_session_valid(request):
    """
    Функция для проверки валидности сессии и продления времени жизни
    """
    if 'user_id' not in request.session:
        return False
    
    # Обновляем время последней активности
    request.session['last_activity'] = str(datetime.now())
    # Устанавливаем флаг модификации сессии
    request.session.modified = True
    # Принудительно сохраняем сессию
    request.session.save()
    
    return True

def test_submit(request, test_id):
    """
    Функция для отправки результатов теста.
    """
    import json
    
    # Подробное логирование полученных данных
    print("\n=============== ДАННЫЕ ФОРМЫ ===============")
    for key, value in request.POST.items():
        print(f"POST: {key} = {value}")
    print("============================================\n")
    
    # Анализируем данные сопоставления и упорядочивания
    matching_questions = {}
    order_questions = {}
    
    for key in request.POST.keys():
        # Поиск данных сопоставления
        if '_matching_' in key:
            parts = key.split('_matching_')
            question_id = parts[0].replace('question_', '')
            if question_id not in matching_questions:
                matching_questions[question_id] = []
            matching_questions[question_id].append(request.POST[key])
        
        # Поиск данных упорядочивания
        elif '_order_' in key:
            parts = key.split('_order_')
            question_id = parts[0].replace('question_', '')
            if question_id not in order_questions:
                order_questions[question_id] = []
            order_questions[question_id].append(request.POST[key])
    
    print("Найденные данные сопоставления:")
    for question_id, values in matching_questions.items():
        print(f"Вопрос {question_id}: {values}")
    
    print("Найденные данные упорядочивания:")
    for question_id, values in order_questions.items():
        print(f"Вопрос {question_id}: {values}")
    
def check_single_choice(request, question_id, question):
    """Проверка вопроса с одним правильным ответом"""
    print("\nОтладка вопроса с одним ответом:")
    print(f"Весь вопрос: {question}")  # Добавляем вывод всего вопроса
    
    user_answer = request.POST.get(f'question_{question_id}')
    correct_answer = question.get('correctAnswer')
    answer_variants = question.get('answerVariants', '').split(';')
    
    print(f"ID вопроса: {question_id}")
    print(f"Варианты ответов: {answer_variants}")
    print(f"Полученный ответ: {user_answer}")
    print(f"Правильный ответ: {correct_answer}")
    
    if not user_answer or not correct_answer:
        print("Ошибка: Отсутствует ответ пользователя или правильный ответ")
        return 0
    
    # Нормализуем ответы перед сравнением
    user_answer = user_answer.strip().lower()
    correct_answer = correct_answer.strip().lower()
    
    is_correct = user_answer == correct_answer
    points = question.get('points', 0) if is_correct else 0
    
    print(f"Результат проверки: {'Верно' if is_correct else 'Неверно'}")
    print(f"Начислено баллов: {points}")
    
    return points
    
def check_multiple_choice(request, question_id, question):
    """Проверка вопроса с множественным выбором"""
    print(f"\nПроверка вопроса с множественным выбором (ID: {question_id}):")
    print(f"Текст вопроса: {question.get('questionText')}")
    
    # Получаем все возможные варианты ответов
    answer_variants = question.get('answerVariants', '').split(';')
    answer_variants = [v.strip() for v in answer_variants if v.strip()]
    
    # Получаем правильные ответы и нормализуем их
    correct_answers = question.get('correctAnswer', '').split(';')
    correct_answers = [ans.strip() for ans in correct_answers if ans.strip()]
    
    # Получаем ответы пользователя
    user_answers = []
    for i in range(len(answer_variants)):
        answer_key = f'question_{question_id}_option_{i+1}'
        if answer_key in request.POST:
            answer = request.POST[answer_key].strip()
            if answer:
                user_answers.append(answer)
    
    print(f"Варианты ответов: {answer_variants}")
    print(f"Правильные ответы (до нормализации): {correct_answers}")
    print(f"Ответы пользователя (до нормализации): {user_answers}")
    
    # Функция для нормализации строки
    def normalize_string(s):
        # Приводим к нижнему регистру
        s = s.lower()
        # Убираем начальные и конечные пробелы
        s = s.strip()
        # Заменяем множественные пробелы на один
        s = ' '.join(s.split())
        return s
    
    # Нормализуем оба набора ответов
    normalized_correct = {normalize_string(ans) for ans in correct_answers}
    normalized_user = {normalize_string(ans) for ans in user_answers}
    
    print(f"Нормализованные правильные ответы: {normalized_correct}")
    print(f"Нормализованные ответы пользователя: {normalized_user}")
    
    # Сравниваем множества
    is_correct = normalized_correct == normalized_user
    points = question.get('points', 0) if is_correct else 0
    
    print(f"Результат проверки: {'Верно' if is_correct else 'Неверно'}")
    print(f"Начислено баллов: {points}")
    
    return points
    
def check_text_input(request, question_id, question):
    """Проверка вопроса с вводом ответа"""
    user_answer = request.POST.get(f'question_{question_id}', '').strip()
    correct_answer = question.get('correctAnswer', '').strip()
    
    print(f"Вопрос {question_id}:")
    print(f"- Введенный ответ: '{user_answer}'")
    print(f"- Правильный ответ: '{correct_answer}'")
    
    # Нормализация ответов для сравнения
    user_normalized = user_answer.lower().replace(' ', '')
    correct_normalized = correct_answer.lower().replace(' ', '')
    
    return question.get('points', 0) if user_normalized == correct_normalized else 0
    
def check_matching(request, question_id, question):
    """Проверка вопроса на сопоставление"""
    print(f"\nПроверка вопроса на сопоставление (ID: {question_id}):")
    print(f"Текст вопроса: {question.get('questionText')}")
    
    # Получаем правильные пары из correctAnswer
    correct_pairs = {}
    if question.get('correctAnswer'):
        pairs = question.get('correctAnswer').split(';')
        for pair in pairs:
            if ' - ' in pair:
                left, right = pair.split(' - ', 1)
                correct_pairs[left.strip().lower()] = right.strip().lower()
    
    print(f"Правильные пары: {correct_pairs}")
    
    # Получаем ответы пользователя
    user_pairs = {}
    i = 0
    while True:
        left_key = f'question_{question_id}_left_{i}'
        match_key = f'question_{question_id}_match_{i}'
        
        if left_key not in request.POST:
            break
            
        left = request.POST.get(left_key, '').strip().lower()
        match = request.POST.get(match_key, '').strip()
        
        if left and match:
            if ':' in match:  # Если формат "left:right"
                _, right = match.split(':', 1)
                user_pairs[left] = right.strip().lower()
            else:
                user_pairs[left] = match.lower()
                
        i += 1
    
    print(f"Пары пользователя: {user_pairs}")
    
    # Проверяем все соединения
    is_correct = True
    for left, right in user_pairs.items():
        if left not in correct_pairs or correct_pairs[left] != right:
            is_correct = False
            break
    
    # Проверяем, что количество пар совпадает
    if len(user_pairs) != len(correct_pairs):
        is_correct = False
    
    points = question.get('points', 0) if is_correct else 0
    
    print(f"Результат проверки: {'Верно' if is_correct else 'Неверно'}")
    print(f"Начислено баллов: {points}")
    
    return points
    
def check_ordering(request, question_id, question):
    """Проверка вопроса на установление порядка"""
    print(f"\nПроверка вопроса на установление порядка (ID: {question_id}):")
    print(f"Весь вопрос: {question}")  # Добавляем вывод всего вопроса
    print(f"Текст вопроса: {question.get('questionText')}")
    
    # Получаем правильный порядок
    correct_order = []
    if question.get('correctAnswer'):
        correct_order = [item.strip() for item in question.get('correctAnswer').split(';') if item.strip()]
    
    print(f"Правильный порядок: {correct_order}")
    
    # Получаем все POST параметры для отладки
    print("Все POST параметры для этого вопроса:")
    for key, value in request.POST.items():
        if f'question_{question_id}' in key:
            print(f"{key}: {value}")
    
    # Получаем ответ пользователя
    user_order = []
    i = 0
    while True:
        key = f'question_{question_id}_order_{i}'
        if key not in request.POST:
            break
        value = request.POST.get(key).strip()
        if value:
            user_order.append(value)
        i += 1
    
    print(f"Порядок пользователя: {user_order}")
    
    # Проверяем совпадение порядка
    is_correct = user_order == correct_order
    points = question.get('points', 0) if is_correct else 0
    
    print(f"Результат проверки: {'Верно' if is_correct else 'Неверно'}")
    print(f"Начислено баллов: {points}")
    
    return points
    