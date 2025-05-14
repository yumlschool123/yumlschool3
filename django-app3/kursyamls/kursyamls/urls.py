from django.contrib import admin
from django.urls import path

from yamlschool.views import *
from django.urls import path

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('admin/', adminPage, name='adminPage'), 
    path('admin/export/groups/', export_groups_to_json, name='export_groups_to_json'),
    path('admin/import/groups/', import_groups_from_json, name='import_groups_from_json'),


    path('subjects/', AllSubjectPage, name='AllSubjectPage'),

    path('register/', register, name='register'),
    path('nullSubjects/', nullSubjects, name='nullSubjects'), 

    
    path('admin/groups/', group_crud, name='group_crud'),
    path('admin/groups/create/', create_group, name='create_group'),
    path('admin/groups/edit/<int:id>/', edit_group, name='edit_group'),
    path('admin/groups/delete/<int:id>/', delete_group, name='delete_group'),

    path('admin/users/', user_crud, name='user_crud'),
    path('admin/users/edit/<int:id>/', edit_user, name='edit_user'),
    path('admin/users/delete/<int:id>/', delete_user, name='delete_user'),


    path('admin/subjects/', subject_crud, name='subject_crud'),
    path('admin/subjects/edit/<int:id>/', edit_subject, name='edit_subject'),
    path('admin/subjects/delete/<int:id>/', delete_subject, name='delete_subject'),



    path('lection/<int:id>/', LectionMaterial, name='LectionMaterial'),  
    path('edit_lection/<int:id>/', edit_lection, name='edit_lection'),
    path('delete_lection/<int:id>/', delete_lection, name='delete_lection'),

    
    path('subject/<int:id>/', SubjectPage, name='SubjectPage'), 
    path('subject/<int:subject_id>/lection/create/', create_lection, name='create_lection'), 

    path('subject/<int:subject_id>/practical_work/create/', create_practical_work, name='create_practical_work'),  
   
    path('practical_work/<int:id>/', PracticalWorkMaterial, name='PracticalWorkMaterial'),
    path('practical_work/edit/<int:id>/', edit_practical_work, name='edit_practical_work'),
    path('practical_work/delete/<int:id>/', delete_practical_work, name='delete_practical_work'),

    path('practical_work/<int:practical_work_id>/add/', AddCompleteWork, name='AddCompleteWork'),

    path('practical_work/<int:practical_work_id>/grade/<int:user_id>/', grade_completed_work, name='grade_completed_work'),

    path('practical-work/<int:practical_work_id>/export-performance/', export_students_performance, name='export_students_performance'),

    path('subject/<int:subject_id>/test/create/', create_test, name='create_test'),
    path('test/<int:id>/', test_material, name='test_material'),
    path('test/edit/<int:id>/', edit_test, name='edit_test'),
    path('test/delete/<int:id>/', delete_test, name='delete_test'),
    path('test/<int:id>/start/', start_test, name='start_test'),
    path('test/<int:id>/submit/', submit_test, name='submit_test'),
    path('test/<int:id>/results/', test_results, name='test_results'),
    path('test/<int:id>/attempts/', test_attempts, name='test_attempts'),
    path('test/<int:id>/students-results/', test_students_results, name='test_students_results'),

]
