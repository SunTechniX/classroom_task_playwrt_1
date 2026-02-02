#!/usr/bin/env python3
"""Генератор отчёта с точными формулировками"""
import json
import os
import sys
from pathlib import Path

def load_linter_results():
    try:
        with open("linters_result.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    # Проверка структуры проекта (без README.md)
    project = Path("you_playwright")
    has_project = project.exists() and project.is_dir()
    
    files = {
        "run_chromium.py": False,
        "run_firefox.py": False,
        "run_webkit.py": False,
        "info_headless.py": False,
    }
    
    if has_project:
        for fname in files:
            files[fname] = (project / fname).exists()
    
    all_files_exist = all(files.values())
    
    # Загрузка результатов линтеров
    linters = load_linter_results()
    
    # === ФОРМИРОВАНИЕ ОТЧЁТА ===
    report = []
    report.append("# 📊 Автопроверка домашнего задания: Playwright")
    report.append("")
    
    # Секция 1: Структура проекта
    report.append("## 📁 Структура проекта")
    report.append("")
    if has_project:
        report.append("✅ Папка `you_playwright` существует")
        report.append("")
        report.append("| Файл | Статус |")
        report.append("|------|--------|")
        for fname, exists in files.items():
            status = "✅" if exists else "❌"
            report.append(f"| `{fname}` | {status} |")
        report.append("")
    else:
        report.append("❌ **Папка `you_playwright` отсутствует**")
        report.append("")
        report.append("Требуемая структура:")
        report.append("```")
        report.append("you_playwright/")
        report.append("├── run_chromium.py")
        report.append("├── run_firefox.py")
        report.append("├── run_webkit.py")
        report.append("└── info_headless.py")
        report.append("```")
        report.append("")
    
    # Секция 2: Линтеры
    if all_files_exist and linters:
        report.append("## 🔍 Ошибки линтеров")
        report.append("")
        
        # flake8
        report.append("### flake8 (PEP 8)")
        report.append(f"- Баллы: **{linters['flake8_score']}** / 10")
        report.append(f"- Ошибок: {linters['flake8_errors']}")
        if linters['flake8_errors'] > 0:
            report.append("- Список:")
            for i, detail in enumerate(linters['flake8_details'][:25], 1):
                report.append(f"  {i}. `{detail}`")
            if len(linters['flake8_details']) > 25:
                report.append(f"  ... и ещё {len(linters['flake8_details']) - 25}")
        else:
            report.append("- ✅ Ошибок нет")
        report.append("")
        
        # pylint
        report.append("### pylint")
        report.append(f"- Баллы: **{linters['pylint_score']}** / 10")
        report.append(f"- Критических ошибок: {linters['pylint_errors']}")
        if linters['pylint_errors'] > 0:
            report.append("- Список:")
            for i, detail in enumerate(linters['pylint_details'][:25], 1):
                report.append(f"  {i}. `{detail}`")
            if len(linters['pylint_details']) > 25:
                report.append(f"  ... и ещё {len(linters['pylint_details']) - 25}")
        else:
            report.append("- ✅ Ошибок нет")
        report.append("")
    
    # Итог
    report.append("## 🏆 Итог")
    report.append("")
    if not has_project:
        report.append("❌ **РАБОТА НЕ ПРИНЯТА** — отсутствует папка `you_playwright`")
    elif not all_files_exist:
        report.append("⚠️ **ДОРАБОТКА** — не все файлы присутствуют (см. таблицу выше)")
    else:
        report.append("✅ **Структура проекта корректна**")
        if linters and linters['total'] >= 8:
            report.append("✅ **Стиль кода соответствует требованиям**")
        else:
            report.append("⚠️ **Требуется исправить замечания линтеров** (см. раздел выше)")
    
    report.append("")
    report.append("> 💡 `README.md` не проверяется — задание фокусируется на коде.")
    
    # Сохранение
    summary_text = "\n".join(report)
    github_summary = os.getenv("GITHUB_STEP_SUMMARY")
    
    if github_summary and Path(github_summary).exists():
        with open(github_summary, "w", encoding="utf-8") as f:
            f.write(summary_text)
        print("✅ Отчёт сформирован")
    else:
        with open("SUMMARY.md", "w", encoding="utf-8") as f:
            f.write(summary_text)
        print(summary_text)
    
    # Код выхода
    sys.exit(0 if (has_project and all_files_exist) else 1)

if __name__ == "__main__":
    main()