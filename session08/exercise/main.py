"""
TODOアプリ バックエンド - 実習用スターター
第8回: セキュリティの基礎 & 総仕上げ

第7回の正解をベースに、セキュリティ上の問題を意図的に残しています。
TODO コメントの指示に従って安全なコードに修正してください。
"""

import sqlite3

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# --- FastAPIアプリ ---
app = FastAPI(title="TODO App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- データベース設定 ---
DATABASE = "todo.db"


def init_db():
    """データベースとテーブルを初期化する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# データベースには、各APIの中で sqlite3.connect(DATABASE) して接続し、
# 最後に conn.close() で閉じる。（第7回までと同じ「毎回つなぐ」スタイル）


# --- Pydanticモデル ---


# TODO(実習5): TodoCreate にバリデーションを追加してください
#   ヒント: from pydantic import Field を追加して
#           title: str = Field(min_length=1, max_length=100) に書き換える
class TodoCreate(BaseModel):
    title: str  # ← ここにバリデーションを追加


class TodoUpdate(BaseModel):
    done: bool


# --- APIエンドポイント ---


@app.get("/todos")
def get_todos():
    """TODO一覧を取得する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, done FROM todos ORDER BY id")
    todos = cursor.fetchall()

    conn.close()
    # 1行は (id, title, done) の順のタプル。番号で取り出して辞書のリストにする
    return [
        {"id": todo[0], "title": todo[1], "done": bool(todo[2])}
        for todo in todos
    ]


@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    """新しいTODOを作成する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # TODO(実習4): パラメータバインディングに修正してください
    #   修正前（危険）: f-string でユーザー入力を直接SQL文に埋め込んでいる
    #   修正後（安全）:
    #     cursor.execute(
    #         "INSERT INTO todos (title, done) VALUES (?, 0)",
    #         (todo.title,)
    #     )
    cursor.execute(f"INSERT INTO todos (title, done) VALUES ('{todo.title}', 0)")
    conn.commit()
    todo_id = cursor.lastrowid

    conn.close()
    return {"id": todo_id, "title": todo.title, "done": False}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    """TODOの完了状態を更新する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 第7回の正解と同じく、レスポンスで title を返すため既存レコードを先に取得する
    cursor.execute("SELECT title FROM todos WHERE id = ?", (todo_id,))
    existing = cursor.fetchone()

    # TODO(実習6): 存在しないTODOの場合に404を返してください
    #   ヒント:
    #     if existing is None:
    #         conn.close()
    #         raise HTTPException(status_code=404, detail="TODO not found")

    # TODO(実習4): パラメータバインディングに修正してください
    #   修正後:
    #     cursor.execute(
    #         "UPDATE todos SET done = ? WHERE id = ?",
    #         (int(todo.done), todo_id)
    #     )
    cursor.execute(f"UPDATE todos SET done = {int(todo.done)} WHERE id = {todo_id}")
    conn.commit()

    conn.close()
    # existing は (title,) のタプルなので先頭を取り出す
    return {"id": todo_id, "title": existing[0], "done": todo.done}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """TODOを削除する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # TODO(実習6): 存在しないTODOの場合に404を返してください
    #   ヒント:
    #     cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
    #     existing = cursor.fetchone()
    #     if existing is None:
    #         conn.close()
    #         raise HTTPException(status_code=404, detail="TODO not found")

    # TODO(実習4): パラメータバインディングに修正してください
    #   修正後:
    #     cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    cursor.execute(f"DELETE FROM todos WHERE id = {todo_id}")
    conn.commit()

    conn.close()
    return {"message": "TODO deleted", "id": todo_id}


# --- 静的ファイル配信 ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# --- アプリ起動時にDBを初期化 ---
init_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
