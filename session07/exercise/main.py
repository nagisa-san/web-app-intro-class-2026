"""
第7回 実習: フロントエンドとバックエンドの結合

第6回の正解をベースに、静的ファイル配信とCORS設定（発展）を追加します。
TODO コメントの部分を実装してください。

起動方法:
  python init_db.py
  python main.py
"""

import sqlite3

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Pydantic モデル ---


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    done: bool


# --- FastAPI アプリケーション ---

app = FastAPI(title="TODO API")


# --- TODO: CORS設定を追加してください（実習6・発展）---
# 同一オリジン配信なら無くても動く。フロントを別オリジンに分けたとき必要になる設定。
# ヒント:
#   app.add_middleware(
#       CORSMiddleware,
#       allow_origins=["*"],
#       allow_credentials=True,
#       allow_methods=["*"],
#       allow_headers=["*"],
#   )


# --- データベース接続について ---
# 各APIの中で sqlite3.connect(DATABASE) して接続し、最後に conn.close() で閉じる。
# （ヘルパー関数や row_factory は使わず、毎回つなぐシンプルなスタイルに統一）

DATABASE = "todo.db"


# --- APIエンドポイント（第6回の正解） ---


@app.get("/todos")
def get_todos():
    """TODO一覧を取得する"""
    conn = sqlite3.connect(DATABASE)  # 接続する
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, done FROM todos ORDER BY id")
    rows = cursor.fetchall()  # 取得した全行をリストで受け取る

    conn.close()  # 接続を閉じる
    # 1行は (id, title, done) の順のタプル。番号で取り出して辞書のリストにする
    return [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]


@app.post("/todos")
def create_todo(todo: TodoCreate):
    """新しいTODOを追加する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO todos (title, done) VALUES (?, 0)",
        (todo.title,),
    )
    conn.commit()
    todo_id = cursor.lastrowid  # たった今追加した行の id

    conn.close()
    return {"id": todo_id, "title": todo.title, "done": False}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    """TODOの完了状態を更新する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # まず対象のTODOが存在するか確認する
    cursor.execute("SELECT title FROM todos WHERE id = ?", (todo_id,))
    existing = cursor.fetchone()  # 無ければ None
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="TODO not found")

    cursor.execute(
        "UPDATE todos SET done = ? WHERE id = ?",
        (int(todo.done), todo_id),
    )
    conn.commit()

    conn.close()
    # existing は (title,) のタプルなので先頭を取り出す
    return {"id": todo_id, "title": existing[0], "done": todo.done}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """TODOを削除する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 削除する前に対象が存在するか確認する
    cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="TODO not found")

    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()

    conn.close()
    return {"message": "TODO deleted", "id": todo_id}


# --- TODO: 静的ファイル配信を追加してください（実習2）---
# TODO(実習2): 静的ファイルを配信してください
#   ヒント:
#   app.mount("/", StaticFiles(directory="static", html=True), name="static")
#
# 注意: app.mount() はすべてのパスを受け取るので、ファイルの最後に書いてください


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
