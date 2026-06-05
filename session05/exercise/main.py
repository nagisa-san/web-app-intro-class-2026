"""
第5回 実習: Python & FastAPI入門

このファイルを編集して、以下のエンドポイントを完成させてください:
  1. GET /            - Hello World（実装済み）
  2. GET /hello/{name} - 名前付き挨拶
  3. GET /todos       - TODOリスト取得

起動方法:
  python main.py
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI()


# -----------------------------------------------
# エンドポイント1: ルート（実装済み）
# -----------------------------------------------
@app.get("/")
def root():
    return {"message": "TODO API is running", "docs": "/docs"}


# -----------------------------------------------
# エンドポイント2: 名前付き挨拶
# -----------------------------------------------
# ヒント:
@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"こんにちは、{name}さん！"}


# -----------------------------------------------
# エンドポイント3: TODOリスト取得
# -----------------------------------------------
# ヒント: まずTODOデータを作成
todos = [
    {"id": 1, "title": "買い物に行く", "done": False},
    {"id": 2, "title": "レポートを書く", "done": True},
    {"id": 3, "title": "部屋を掃除する", "done": False},
]
#
# ヒント: エンドポイントを作成
@app.get("/todos")
def get_todos():
    return todos

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
