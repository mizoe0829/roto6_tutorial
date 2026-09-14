FROM python:3.11-slim

# 環境変数(バイトコード生成抑制・ログのバッファリング抑制)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 依存関係だけ先にコピーしてキャッシュを効かせる
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
