from django import template
import random
import re

register = template.Library()

@register.filter
def split(value, delimiter):
    """Разделяет строку по указанному разделителю."""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def index(lst, i):
    """
    Returns the item at index i in the list.
    Example: {{ list|index:i }}
    """
    try:
        return lst[i]
    except:
        return ''

@register.filter
def split_pairs(items, part):
    """
    Разделяет строки вида "левая часть -> правая часть" на части.
    Для part='left' возвращает список левых частей.
    Для part='right' возвращает список правых частей.
    """
    result = []
    if not items:
        return result
    
    # Проверка, является ли items списком строк или одной строкой
    if isinstance(items, str):
        items = [items]
    
    for item in items:
        if '->' in item:
            left, right = item.split('->', 1)
            if part == 'left':
                result.append(left.strip())
            elif part == 'right':
                result.append(right.strip())
        else:
            # Если разделитель не найден, возвращаем исходную строку для обеих частей
            if part in ['left', 'right']:
                result.append(item.strip())
    
    return result

@register.filter
def randomize(items):
    """Случайно перемешивает элементы списка"""
    if items:
        result = list(items)  # Создаем копию списка
        random.shuffle(result)
        return result
    return []

@register.filter
def get_item(value, index):
    """Получает элемент списка по индексу."""
    try:
        return value[index]
    except (IndexError, TypeError):
        return None

@register.filter
def filter_by_grade(criteria, grade):
    """Находит критерий с указанной оценкой"""
    for criterion in criteria:
        if criterion.get('grade') == grade:
            return criterion
    return None

@register.filter
def filter_by_key(value, key):
    """Фильтрует список словарей по наличию ключа."""
    if not value:
        return []
    
    return [item for item in value if key in item]

@register.filter
def filter_by_value(value, val):
    """Фильтрует список словарей по значению в первом ключе."""
    if not value:
        return []
    
    result = []
    for item in value:
        if item and list(item.values())[0] == val:
            result.append(item)
    
    return result 