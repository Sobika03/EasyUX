from django.urls import path
from .views import sample, tabulator_view,list_backup_files,dump_data_to_json,download_dumped_data,delete_backup_file

urlpatterns = [
    path('sample/', sample, name='sample'),
    path('tabulator/', tabulator_view, name='tabulator_view'),
    path('backup/', list_backup_files, name='backup-page'),
    path('dump-data/', dump_data_to_json, name='dump_data_view'),
    path('download-dump/<str:filename>/', download_dumped_data, name='download-dump'),
    path('delete-dump/<str:filename>/', delete_backup_file, name='delete-dump'),
]


