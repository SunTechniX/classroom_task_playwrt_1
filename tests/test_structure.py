"""Проверка структуры проекта — только кодовые файлы"""
import pytest
from pathlib import Path

PROJECT_ROOT = Path("you_playwright")
REQUIRED_FILES = [
    "run_chromium.py",
    "run_firefox.py",
    "run_webkit.py",
    "info_headless.py",
]

@pytest.mark.structure
def test_project_folder_exists():
    """Папка you_playwright существует"""
    assert PROJECT_ROOT.exists(), "❌ Папка you_playwright отсутствует"
    assert PROJECT_ROOT.is_dir(), "❌ you_playwright не является папкой"

@pytest.mark.parametrize("filename", REQUIRED_FILES)
def test_required_file_exists(filename):
    """Все обязательные файлы присутствуют"""
    filepath = PROJECT_ROOT / filename
    assert filepath.exists(), f"❌ Файл {filename} отсутствует"
    assert filepath.is_file(), f"❌ {filename} не является файлом"