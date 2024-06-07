from celery import shared_task
import os
from ..file_app.models import File

@shared_task
def scan_dir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file, created = File.objects.get_or_create(path=file_path, name=file, size=os.path.getsize(file_path), is_dir=False)
        
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            dir, created = File.objects.get_or_create(path=dir_path, name=dir, size=0, is_dir=True)
        
    return 'Scan complete'