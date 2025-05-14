from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.adminPage, name='adminPage'),
    path('lections/', views.LectionCRUD, name='lections'),
    path('lections/<int:id>/', views.LectionMaterial, name='LectionMaterial'),
    path('subject/<int:id>/', views.SubjectPage, name='SubjectPage'),
    path('subject/create_lection/<int:subject_id>/', views.create_lection, name='create_lection'),
    path('lections/edit/<int:id>/', views.edit_lection, name='edit_lection'),
    path('lections/delete/<int:id>/', views.delete_lection, name='delete_lection'),
    path('subjects/', views.AllSubjectPage, name='AllSubjectPage'),
    path('subjects/null/', views.nullSubjects, name='nullSubjects'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('null/', views.nullPage, name='nullPage'),

    path('group-crud/', views.group_crud, name='group_crud'),


    
    path('group-crud/create/', views.create_group, name='create_group'),
    path('group-crud/edit/<int:id>/', views.edit_group, name='edit_group'),
    path('group-crud/delete/<int:id>/', views.delete_group, name='delete_group'),

    path('admin/export/', views.export_groups_to_sql, name='export_groups_to_sql'),
    # path('admin/import/', views.import_groups_from_sql, name='import_groups_from_sql'),
    # path('admin/export/', views.export_students_works, name='export_students_works'),


    path('user-crud/', views.user_crud, name='user_crud'),
    path('user-crud/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('user-crud/delete/<int:id>/', views.delete_user, name='delete_user'),
    path('subject-crud/', views.subject_crud, name='subject_crud'),
    path('subject-crud/edit/<int:id>/', views.edit_subject, name='edit_subject'),
    path('subject-crud/delete/<int:id>/', views.delete_subject, name='delete_subject'),
    path('subject/<int:subject_id>/create_practical_work/', views.create_practical_work, name='create_practical_work'),
    
    

    path('practical-work/<int:idPracticalWork>/', views.PracticalWorkMaterial, name='practical_work_material'),    

    path('practical_work/delete/<int:id>/', views.delete_practical_work, name='delete_practical_work'),
    path('practical_work/edit/<int:id>/', views.edit_practical_work, name='edit_practical_work'),
    
    # Важно: используем одинаковое имя URL повсюду
    path('practical_work/<int:practical_work_id>/add/', views.AddCompleteWork, name='add_complete_work'),
    
    path('practical_work/<int:practical_work_id>/grade/<int:user_id>/', views.grade_completed_work, name='grade_completed_work'),
    path('subject/<int:subject_id>/create_test/', views.create_test, name='create_test'),
    path('test/<int:id>/', views.test_material, name='test_material'),
    path('test/edit/<int:id>/', views.edit_test, name='edit_test'),
    path('test/delete/<int:id>/', views.delete_test, name='delete_test'),
    path('test/<int:id>/start/', views.start_test, name='start_test'),
    path('test/<int:id>/submit/', views.submit_test, name='submit_test'),
    path('test/<int:id>/results/', views.test_results, name='test_results'),
    path('test/<int:id>/attempts/', views.test_attempts, name='test_attempts'),
    path('test/<int:id>/students_results/', views.test_students_results, name='test_students_results'),
    
    path('practical_work/<int:practical_work_id>/export_students_performance/', views.export_students_performance, name='export_students_performance'),

   
    path('test/<int:id>/process/', views.test_process, name='test_process'),



]