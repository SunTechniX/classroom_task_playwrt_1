"""Статический анализ синтаксиса и импортов (без выполнения кода!)"""
import ast
import re
from pathlib import Path
import pytest

PROJECT_ROOT = Path("you_playwright")

def parse_python_file(filepath):
    """Парсинг файла через AST без выполнения"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return ast.parse(content, filename=str(filepath)), content
    except SyntaxError as e:
        pytest.fail(f"❌ Синтаксическая ошибка в {filepath.name}: {e.msg} (строка {e.lineno})")
    except FileNotFoundError:
        pytest.fail(f"❌ Файл {filepath.name} не найден")
    except Exception as e:
        pytest.fail(f"❌ Ошибка чтения {filepath.name}: {e}")

def has_sync_playwright_import(tree):
    """Проверка импорта sync_playwright"""
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "playwright.sync_api":
            if any(alias.name == "sync_playwright" for alias in node.names):
                return True
    return False

def has_browser_launch(code, browser_name):
    """Проверка запуска конкретного браузера через регулярные выражения"""
    # Ищем шаблоны: p.chromium.launch(), browser = p.chromium.launch()
    pattern = rf'p\.{browser_name}\.launch\('
    return bool(re.search(pattern, code))

def has_print_title(code):
    """Проверка вывода заголовка через print(...) и page.title()"""
    # Ищем: print(page.title()) или title = page.title(); print(title)
    return bool(re.search(r'print\s*\([^)]*title\(\)', code, re.IGNORECASE))

def has_headless_mode(code):
    """Проверка запуска в headless-режиме"""
    # Ищем: headless=True в launch()
    return bool(re.search(r'headless\s*=\s*True', code))

def has_required_outputs(code):
    """Проверка наличия вывода 3 параметров в info_headless.py"""
    has_ua = bool(re.search(r'(print|User-Agent).*[Uu]ser.?Agent', code, re.IGNORECASE)) or \
             bool(re.search(r'navigator\.userAgent', code))
    has_viewport = bool(re.search(r'(viewport|size|width.*height|height.*width)', code, re.IGNORECASE))
    has_url = bool(re.search(r'(URL|url|page\.url)', code, re.IGNORECASE))
    return has_ua, has_viewport, has_url

# === Тесты для Задания 1 ===

@pytest.mark.syntax
def test_chromium_syntax():
    tree, code = parse_python_file(PROJECT_ROOT / "run_chromium.py")
    assert has_sync_playwright_import(tree), "❌ Отсутствует импорт sync_playwright из playwright.sync_api"
    assert has_browser_launch(code, "chromium"), "❌ Не найден запуск браузера: p.chromium.launch()"
    assert has_print_title(code), "❌ Не обнаружен вывод заголовка страницы через print()"

@pytest.mark.syntax
def test_firefox_syntax():
    tree, code = parse_python_file(PROJECT_ROOT / "run_firefox.py")
    assert has_sync_playwright_import(tree), "❌ Отсутствует импорт sync_playwright из playwright.sync_api"
    assert has_browser_launch(code, "firefox"), "❌ Не найден запуск браузера: p.firefox.launch()"

@pytest.mark.syntax
def test_webkit_syntax():
    tree, code = parse_python_file(PROJECT_ROOT / "run_webkit.py")
    assert has_sync_playwright_import(tree), "❌ Отсутствует импорт sync_playwright из playwright.sync_api"
    assert has_browser_launch(code, "webkit"), "❌ Не найден запуск браузера: p.webkit.launch()"

# === Тесты для Задания 2 ===

@pytest.mark.syntax
def test_headless_syntax():
    tree, code = parse_python_file(PROJECT_ROOT / "info_headless.py")
    assert has_sync_playwright_import(tree), "❌ Отсутствует импорт sync_playwright из playwright.sync_api"
    assert has_headless_mode(code), "❌ Не обнаружен запуск в headless-режиме (должно быть headless=True в launch())"

@pytest.mark.syntax
def test_headless_outputs():
    _, code = parse_python_file(PROJECT_ROOT / "info_headless.py")
    has_ua, has_viewport, has_url = has_required_outputs(code)
    
    assert has_ua, "❌ Не обнаружен вывод User-Agent (используйте page.evaluate('navigator.userAgent') или вывод содержимого)"
    assert has_viewport, "❌ Не обнаружен вывод размера viewport (ширина/высота)"
    assert has_url, "❌ Не обнаружен вывод текущего URL страницы"