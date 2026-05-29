"""
第6回 実習: FastAPI + SQLite による TODO REST API

第5回の正解をベースに、SQLiteデータベースとCRUD操作を追加します。
GET /todos は実装済みです。POST / PUT / DELETE を実装してください。

起動方法:
  1. python init_db.py  (初回のみ)
  2. python main.py
  3. ブラウザで http://localhost:8000/docs を開く
"""

import sqlite3

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- アプリケーション設定 ---

app = FastAPI(
    title="TODO API",
    description="第6回: FastAPI + SQLite による TODO REST API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "todo.db"


# --- Pydantic モデル（リクエストの型定義） ---


class TodoCreate(BaseModel):
    """TODO新規作成用"""

    title: str


class TodoUpdate(BaseModel):
    """TODO更新用"""

    done: bool


# --- データベース接続について ---
# このアプリでは、各APIの中で sqlite3.connect(DATABASE) して接続し、
# 処理が終わったら conn.close() で閉じる「毎回つなぐ」スタイルに統一する。
# （ヘルパー関数や row_factory は使わず、初学者にも追いやすいシンプルな形にしている）


# --- API エンドポイント ---


@app.get("/")
def root():
    return {"message": "TODO API is running", "docs": "/docs"}


# GET /todos - TODO一覧取得（実装済み）
@app.get("/todos")
def get_todos():
    """全てのTODOをリストで返す"""
    conn = sqlite3.connect(DATABASE)  # DBに接続する
    cursor = conn.cursor()  # SQLを実行する係（カーソル）

    cursor.execute("SELECT id, title, done FROM todos ORDER BY id")
    rows = cursor.fetchall()  # 取得した全行をリストで受け取る

    conn.close()  # 接続を閉じる
    # 1行は (id, title, done) の順のタプル。番号で取り出して辞書のリストに作り変える
    return [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]


# POST /todos - TODO新規作成
@app.post("/todos")
def create_todo(todo: TodoCreate):
    """タイトルを受け取り、新しいTODOを追加する"""
    # ヒント:
    #   1. conn = sqlite3.connect(DATABASE) で接続し、cursor = conn.cursor()
    #   2. cursor.execute(
    #          "INSERT INTO todos (title, done) VALUES (?, 0)", (todo.title,)
    #      )
    #   3. conn.commit() で確定
    #   4. new_id = cursor.lastrowid で新しいIDを取得
    #   5. conn.close() で閉じる
    #   6. {"id": new_id, "title": todo.title, "done": False} を返す
    pass


# PUT /todos/{todo_id} - TODO更新
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    """指定IDのTODOの完了状態を更新する"""
    # ヒント:
    #   1. conn = sqlite3.connect(DATABASE) で接続し、cursor = conn.cursor()
    #   2. SELECT で対象が存在するか確認
    #      cursor.execute("SELECT title FROM todos WHERE id = ?", (todo_id,))
    #      existing = cursor.fetchone()  # 無ければ None が返る
    #   3. 存在しなければ conn.close() してから
    #      raise HTTPException(status_code=404, detail="TODO not found")
    #   4. cursor.execute("UPDATE todos SET done = ? WHERE id = ?", (int(todo.done), todo_id))
    #   5. conn.commit(), conn.close()
    #   6. {"id": todo_id, "title": existing[0], "done": todo.done} を返す
    #      （existing は (title,) のタプルなので先頭を取り出す）
    pass


# DELETE /todos/{todo_id} - TODO削除
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """指定IDのTODOを削除する"""
    # ヒント:
    #   1. conn = sqlite3.connect(DATABASE) で接続し、cursor = conn.cursor()
    #   2. SELECT で対象が存在するか確認
    #      cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
    #      existing = cursor.fetchone()
    #   3. 存在しなければ conn.close() してから
    #      raise HTTPException(status_code=404, detail="TODO not found")
    #   4. cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    #   5. conn.commit(), conn.close()
    #   6. {"message": "TODO deleted", "id": todo_id} を返す
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
