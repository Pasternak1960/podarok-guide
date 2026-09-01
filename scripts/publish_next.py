#!/usr/bin/env python3
"""
Берёт самые старые статьи из content/queue/ (сколько указано в config.json,
поле publish_per_run), проставляет им сегодняшнюю дату и переносит в
content/published/. Используется GitHub Actions по расписанию.
Если очередь пуста — ничего не делает (и печатает предупреждение в лог workflow).
"""
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "content", "queue")
PUB_DIR = os.path.join(ROOT, "content", "published")
CONFIG_PATH = os.path.join(ROOT, "config.json")

DATE_LINE_RE = re.compile(r"^date:\s*.*$", re.MULTILINE)

def load_publish_per_run():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg = json.load(f)
        n = int(cfg.get("publish_per_run", 1))
        return max(1, n)
    except Exception:
        return 1

def publish_one(fname, today):
    src = os.path.join(QUEUE_DIR, fname)
    dst = os.path.join(PUB_DIR, fname)
    with open(src, encoding="utf-8") as f:
        text = f.read()
    if DATE_LINE_RE.search(text):
        text = DATE_LINE_RE.sub(f"date: {today}", text, count=1)
    else:
        text = text.replace("---\n", f"---\ndate: {today}\n", 1)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    os.remove(src)

def main():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    os.makedirs(PUB_DIR, exist_ok=True)
    queued = sorted(f for f in os.listdir(QUEUE_DIR) if f.endswith(".md"))
    if not queued:
        print("Очередь статей пуста — публиковать нечего. "
              "Добавьте новые .md файлы в content/queue/.")
        return
    per_run = load_publish_per_run()
    today = date.today().isoformat()
    batch = queued[:per_run]
    for fname in batch:
        publish_one(fname, today)
        print(f"Опубликована статья: {fname} (дата: {today}).")
    print(f"Опубликовано за этот запуск: {len(batch)}. "
          f"Осталось в очереди: {len(queued) - len(batch)}.")

if __name__ == "__main__":
    main()
