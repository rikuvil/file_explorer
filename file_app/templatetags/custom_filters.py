from django import template
register = template.Library()

@register.filter
def human_size(size):
    if size is None:
        return '-'
    
    size_in_bytes = int(size)
    if size_in_bytes < 1024:
        return f'{size_in_bytes} B'
    elif size_in_bytes < 1024**2:
        return f'{size_in_bytes / 1024:.2f} KB'
    elif size_in_bytes < 1024**3:
        return f'{size_in_bytes / 1024**2:.2f} MB'
    else:
        return f'{size_in_bytes / 1024**3:.2f} GB'
# 