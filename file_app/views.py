from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404, FileResponse
import docker
import os

# Functions here:

def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
# Create your views here.

def index(request):
    return render(request, 'index.html')

def container_list_view(request):
    client = docker.from_env()

    try:
        containers = client.containers.list(all=True)
        container_list = []
        for container in containers:
            container_list.append({
                'id': container.id,
                'name': container.name,
                'status': container.status,
                'image': container.image.tags[0],
                'created': container.attrs['Created'],
                'ports': container.attrs['NetworkSettings']['Ports']
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'container_list.html', {'containers': container_list})



def container_detail_view(request):
    client = docker.from_env()

    try:
        container = client.containers.get(request.GET.get('id'))
        container_detail = {
            'id': container.id,
            'name': container.name,
            'status': container.status,
            'image': container.image.tags[0],
            'created': container.attrs['Created'],
            'ports': container.attrs['NetworkSettings']['Ports'],
            'environment': container.attrs['Config']['Env'],
            'volumes': container.attrs['Mounts']
        }

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'container_detail.html', {'container': container_detail})


def file_list_view(request, path=''):
    base_path = '/mnt/'
    full_path = os.path.join(base_path, path)

    if not os.path.exists(full_path):
        raise Http404('Path does not exist')
    
    files = []
    for entry in os.listdir(full_path):
        entry_path = os.path.join(full_path, entry)
        if os.path.isdir(entry_path):
            size = get_size(entry_path)
        else:
            size = os.path.getsize(entry_path)
        files.append({
            'name': entry,
            'path': os.path.join(path, entry),
            'size': size,
            'is_dir': os.path.isdir(entry_path),
        })

    return render(request, 'file_list.html', {'files': files, 'path': path})

                                              
def file_detail_view(request, path):
    base_path = '/mnt/'
    full_path = os.path.join(base_path, path)

    if not os.path.exists(full_path):
        raise Http404('Path does not exist')
    
    if os.path.isdir(full_path):
        return file_list_view(request, path)
    else:
        with open(full_path, 'r') as f:
            response = FileResponse(f)
            return response
        
    
        

def file_upload_view(request):
    return render(request, 'file_upload.html')

def file_download_view(request):
    return render(request, 'file_download.html')

def search_view(request):
    return render(request, 'search.html')

# AUTHENTICATION VIEWS

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    return render(request, 'logout.html')

def register_view(request):
    return render(request, 'register.html')

