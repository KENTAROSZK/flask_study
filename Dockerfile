# 使用するベースイメージを指定
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とクリーンアップ（必要な場合）
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# ライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ポートの公開
EXPOSE 8000