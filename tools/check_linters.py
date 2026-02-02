#!/usr/bin/env python3
"""Проверка линтеров с подсчётом баллов"""
import subprocess
import json
import sys
from pathlib import Path

SCRIPTS = [
    "you_playwright/run_chromium.py",
    "you_playwright/run_firefox.py",
    "you_playwright/run_webkit.py",
    "you_playwright/info_headless.py"
]

def run_flake8():
    """Запуск flake8 и подсчёт баллов"""
    result = subprocess.run(
        ["flake8", "--exit-zero"] + SCRIPTS,
        capture_output=True,
        text=True,
        timeout=30
    )
    errors = [line for line in result.stdout.strip().splitlines() if line]
    error_count = len(errors)
    score = max(0, 10 - error_count // 2)  # 1 балл за каждые 2 ошибки
    return score, error_count, errors[:3]

def run_pylint():
    """Запуск pylint и подсчёт критических ошибок"""
    result = subprocess.run(
        ["pylint", "--exit-zero", "--output-format=text", "--score=no",
         "--disable=all", "--enable=E,F"] + SCRIPTS,
        capture_output=True,
        text=True,
        timeout=30
    )
    errors = [line for line in result.stdout.strip().splitlines() 
              if line.startswith("E:") or line.startswith("F:")]
    error_count = len(errors)
    score = max(0, 10 - error_count)
    return score, error_count, errors[:3]

def main():
    try:
        flake8_score, flake8_errors, flake8_details = run_flake8()
    except Exception as e:
        flake8_score, flake8_errors = 0, f"ошибка: {e}"
        flake8_details = []
    
    try:
        pylint_score, pylint_errors, pylint_details = run_pylint()
    except Exception as e:
        pylint_score, pylint_errors = 0, f"ошибка: {e}"
        pylint_details = []
    
    total = flake8_score + pylint_score
    
    # Сохраняем результат для генератора отчёта
    with open("linters_result.json", "w", encoding="utf-8") as f:
        json.dump({
            "flake8_score": flake8_score,
            "flake8_errors": flake8_errors,
            "flake8_details": flake8_details,
            "pylint_score": pylint_score,
            "pylint_errors": pylint_errors,
            "pylint_details": pylint_details,
            "total": total
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ flake8: {flake8_score}/10 баллов (ошибок: {flake8_errors})")
    print(f"✅ pylint: {pylint_score}/10 баллов (критических ошибок: {pylint_errors})")
    print(f"📊 Итого линтеры: {total}/20 баллов")
    return 0 if total >= 12 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"⚠️ Ошибка при запуске линтеров: {e}")
        with open("linters_result.json", "w") as f:
            json.dump({"total": 0, "flake8_score": 0, "pylint_score": 0}, f)
        sys.exit(1)