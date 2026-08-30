#!/usr/bin/env python3
"""
Берёт самую старую статью из content/queue/, проставляет ей сегодняшнюю дату
и переносит в content/published/. Используется еженедельным GitHub Actions.
Если очередь пуста — ничего не делает (и печатает предупреждение в лог workflow).
"""
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "content", "queue")
PUB_DIR = os.path.join(ROOT, "content", "published")

DATE_LINE_RE = re.compile(r"^date:\s*.*$", re.MULTILINE)


def main():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    os.makedirs(PUB_DIR, exist_ok=True)
    queued = sorted(f for f in os.listdir(QUEUE_DIR) if f.endswith(".md"))
    if not queued:
        print("Очередь статей пуста — публиковать нечего. "
              "Добавьте новые .md файлы в content/queue/.")
        return
    next_file = queued[0]
    src = os.path.join(QUEUE_DIR, next_file)
    dst = os.path.join(PUB_DIR, next_file)
    with open(src, encoding="utf-8") as f:
        text = f.read()
    today = date.today().isoformat()
    if DATE_LINE_RE.search(text):
        text = DATE_LINE_RE.sub(f"date: {today}", text, count=1)
    else:
        text = text.replace("---\n", f"---\ndate: {today}\n", 1)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    os.remove(src)
    print(f"Опубликована статья: {next_file} (дата: {today}). "
          f"Осталось в очереди: {len(queued) - 1}.")


if __name__ == "__main__":
    main()
