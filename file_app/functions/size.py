import os
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

def calculate_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_size(path):
    cache_key = f'path_size_{path}'
    size = cache.get(cache_key)
    if size is None:
        if os.path.isdir(path):
            size = calculate_directory_size(path)
        else:
            size = os.path.getsize(path)
        cache.set(cache_key, size, timeout=60)
    return size

def invalidate_cache(path):
    cache_key = f'path_size_{path}'
    cache.delete(cache_key)