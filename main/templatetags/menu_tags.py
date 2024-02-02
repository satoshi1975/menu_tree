from django import template
from ..models import MenuItem
from django.utils.safestring import mark_safe
register = template.Library()

'''тег для генерации древовидного меню'''
@register.simple_tag
def draw_menu(name, current_url=None):
    current_url = current_url.rsplit('/', 1)[-1]
    menu_items = MenuItem.objects.filter(parent=None, menu_name=name)

    # Функция определения активного пути
    def find_active_path(menu_item, current_url, path=[]):
        if current_url == menu_item.named_url:
            return path + [menu_item]
        for child in menu_item.children.all():
            found_path = find_active_path(child, current_url, path + [menu_item])
            if found_path:
                return found_path
        return []

    # Собираем активный путь для текущего URL
    active_path = []
    for item in menu_items:
        active_path = find_active_path(item, current_url)
        if active_path:
            break

    def generate_menu_tree(menu_items, active_path, current_level=0):
        menu_html = ""
        for item in menu_items:
            is_active = item in active_path
            is_direct_child = active_path[current_level] == item if current_level < len(active_path) else False
            if item.url:
                menu_html += f"<li><a href='{item.url}' class={'active' if is_active else ''}>{item.name}</a>"
            else:
                menu_html += f"<li><a href='{{%url {item.named_url}%}}' class={'active' if is_active else ''}>{item.name}</a>"

            # Показываем подменю только если элемент активен или является прямым родителем активного элемента
            if is_active or (is_direct_child and len(active_path) > current_level + 1):
                submenu_items = item.children.all()
                if submenu_items:
                    menu_html += "<ul>"
                    menu_html += generate_menu_tree(submenu_items, active_path, current_level + 1)
                    menu_html += "</ul>"
            menu_html += "</li>"

        return menu_html

    return mark_safe(generate_menu_tree(menu_items, active_path))







