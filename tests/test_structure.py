"""Проверка структуры проекта"""
import pytest
from pathlib import Path

PROJECT_ROOT = Path("you_playwright")
REQUIRED_FILES = [
    "run_chromium.py",
    "run_firefox.py",
    "run_webkit.py",
    "info_headless.py",
    "README.md"
]

@pytest.mark.structure
def test_project_folder_exists():
    """Папка you_playwright существует"""
    assert PROJECT_ROOT.exists(), "❌ Папка you_playwright не найдена"
    assert PROJECT_ROOT.is_dir(), "❌ you_playwright не является папкой"

@pytest.mark.parametrize("filename", REQUIRED_FILES)
def test_required_file_exists(filename):
    """Все обязательные файлы присутствуют"""
    filepath = PROJECT_ROOT / filename
    assert filepath.exists(), f"❌ Файл {filename} отсутствует в папке you_playwright/"
    assert filepath.is_file(), f"❌ {filename} не является файлом"

def test_readme_not_empty():
    """README.md содержит описание (минимум 30 символов)"""
    readme = PROJECT_ROOT / "README.md"
    content = readme.read_text(encoding="utf-8").strip()
    assert len(content) >= 30, "❌ README.md слишком короткий (< 30 символов)"