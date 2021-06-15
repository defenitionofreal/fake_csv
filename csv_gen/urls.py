from django.urls import path, include
from . import views

urlpatterns = [
    path('data-schemas/', views.dashboard, name='Data Schemas'),
    path('data-sets/<int:pk>', views.DataSetView.as_view(), name='Data Sets'),
    path('new-schema/', views.SchemaCreateView.as_view(),
         name='New Schema'),  # create schema
    path('edit-schema/<int:pk>/', views.SchemaUpdateView.as_view(),
         name='Update Schema'),  # update schema
    path('delete/schema/<int:pk>/', views.del_schema,
         name='delete_schema'),  # delete schema
]
