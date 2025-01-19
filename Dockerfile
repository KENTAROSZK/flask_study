# 使用するベースイメージを指定
FROM ubuntu:20.04

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

# 作業ディレクトリを設定
WORKDIR /app

# ライブラリをインストール
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ポートの公開
EXPOSE 8000

