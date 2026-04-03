# rag-prep-service

Сервис для подготовки файлов к загрузке в RAG. **Чанкинг не делает** — только извлечение и нормализация.

Сервис stateless: входящий binary-файл обрабатывается в памяти и сразу возвращается обратно как `.md`, без сохранения на диск.

## Возможности
- PDF, DOCX, MD, TXT, JSON, HTML, CSV, XLSX, PPTX
- Выход: markdown `.md`
- API и CLI

## Установка
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск через Docker Compose
```bash
docker compose up --build -d
```

Остановить:
```bash
docker compose down
```

Логи:
```bash
docker compose logs -f
```

## Локальный запуск без Docker
```bash
uvicorn app.main:app --reload --port 8080
```

### Пример запроса
```bash
curl -X POST -F "file=@/path/to/file.pdf" http://localhost:8080/convert -o file.md
```

## CLI
```bash
python -m app.cli docs/file.pdf docs/file.docx --out processed
```
CLI тоже сохраняет результат как `.md`.

## Формат ответа
- HTTP body: markdown text
- `Content-Type: text/markdown; charset=utf-8`
- без `Content-Disposition` и без имени файла в response

## Заметки
- Для PDF сначала используется обычное извлечение текста; если он пустой или почти пустой, включается OCR fallback.
- OCR в Docker работает через Tesseract (`rus` + `eng`).
- Таблицы приводятся к markdown.
- Сервис не хранит входящие файлы и не сохраняет результат сам — только возвращает response; CLI пишет `.md` локально, если он нужен.
