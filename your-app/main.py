"""
TODOアプリ バックエンド - 完成版
第8回: セキュリティの基礎 & 総仕上げ
"""

import sqlite3  # Python標準のデータベース（SQLite）を使うためのライブラリ
import uvicorn  # FastAPIアプリを動かすためのWebサーバー

from fastapi import FastAPI, HTTPException  # Webアプリ本体とエラー応答用
from fastapi.middleware.cors import CORSMiddleware  # ブラウザからのアクセスを許可する設定
from fastapi.staticfiles import StaticFiles  # HTML/CSS/JSなどのファイルを配信する機能
from pydantic import BaseModel, Field  # 受け取るデータの形をチェックする道具

# --- FastAPIアプリ ---
# このappが、Webアプリ全体の本体になる
app = FastAPI(title="TODO App")

# CORS設定: 別のアドレスで動くフロント（ブラウザの画面）からの通信を許可する
# allow_origins=["*"] は「どこからのアクセスでもOK」という意味（学習用の設定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- データベース設定 ---
# データを保存するファイルの名前。アプリと同じフォルダに todo.db が作られる
DATABASE = "shop.db"


def init_db():
    """データベースとテーブルを初期化する"""
    conn = sqlite3.connect(DATABASE)  
    cursor = conn.cursor()  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,                   
        visited INTEGER DEFAULT 0             
        )
    """)
    conn.commit()  # 変更を確定して保存する
    conn.close()  # 接続を閉じる


# --- Pydanticモデル ---
# APIが受け取るデータの「形」を決めるクラス。
# 形に合わないデータが送られてきたら、FastAPIが自動でエラーを返してくれる。


class ShopCreate(BaseModel):
    # 新しいお店を作るときに受け取るデータ
    # title は1文字以上100文字以下の文字列でなければならない
    name: str = Field(min_length=1, max_length=100)


class ShopUpdate(BaseModel):
    # TODOを更新するときに受け取るデータ
    # done は True / False（完了したかどうか）
    visited: bool


# --- APIエンドポイント ---
# @app.get / @app.post などの飾り（デコレータ）で、
# 「どのURLに、どの種類のリクエストが来たら、この関数を動かすか」を決める。


@app.get("/shops")  # GET /todos にアクセスされたら実行
def get_shops():
    """お店一覧を取得する"""
    conn = sqlite3.connect(DATABASE)  # 接続する
    cursor = conn.cursor()

    # todos テーブルの全データを id 順に取り出す
    cursor.execute("SELECT id, name, visited FROM shops ORDER BY id")
    shops = cursor.fetchall()  # 取り出した全行をリストで受け取る

    conn.close()  # 接続を閉じる
    # 1行は (id, title, done) の順のタプルなので、番号で取り出す。
    # 取り出したデータを、ブラウザに返しやすい辞書のリストに作り変える。
    return [
        {"id": shop[0], "name": shop[1], "visited": bool(shop[2])}
        for shop in shops
    ]


@app.post("/shops", status_code=201)  # POST /todos で新規作成（201=作成成功）
def create_shop(shop: ShopCreate):
    """新しいTODOを作成する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 新しいTODOを1件追加する（done は 0=未完了で登録）
    # ? を使うことで、危険な文字列が混ざってもSQLが壊れない（SQLインジェクション対策）
    cursor.execute(
        "INSERT INTO shops (name, visited) VALUES (?, 0)",
        (shop.name,),
    )
    conn.commit()  # 追加を確定する
    shop_id = cursor.lastrowid  # たった今追加した行の id を取得する

    conn.close()
    return {"id": shop_id, "name": shop.name, "visited": False}


# PUT /todos/5 のように、URLの {todo_id} の部分が引数 todo_id に入る
@app.put("/shops/{shop_id}")
def update_shop(shop_id: int, shop: ShopUpdate):
    """TODOの完了状態を更新する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # まず、その id のTODOが本当にあるか確認する
    cursor.execute("SELECT name FROM shops WHERE id = ?", (shop_id,))
    existing = cursor.fetchone()  # 1件だけ取り出す。無ければ None が返る
    if existing is None:
        conn.close()  # 見つからないときも接続は閉じてから終わる
        # 404エラー（見つからない）を返して処理を中断する
        raise HTTPException(status_code=404, detail="SHOP not found")

    # done（完了状態）を更新する。True/False は int() で 1/0 に変換して保存
    cursor.execute(
        "UPDATE shops SET visited = ? WHERE id = ?",
        (int(shop.visited), shop_id),
    )
    conn.commit()  # 更新を確定する

    conn.close()
    # existing は (title,) のタプルなので、先頭を取り出す
    return {"id": shop_id, "name": existing[0], "visited": shop.visited}


@app.delete("/shops/{shop_id}")  # DELETE /todos/5 で id=5 のTODOを削除
def delete_shop(shop_id: int):
    """SHOPを削除する"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 削除する前に、その id のTODOが存在するか確認する
    cursor.execute("SELECT id FROM shops WHERE id = ?", (shop_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="SHOP not found")

    cursor.execute("DELETE FROM shops WHERE id = ?", (shop_id,))  # 削除する
    conn.commit()  # 削除を確定する

    conn.close()
    return {"message": "SHOP deleted", "id": shop_id}


# --- 静的ファイル配信 ---
# static フォルダの中身（index.html など）をそのままブラウザに表示できるようにする
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# --- アプリ起動時にDBを初期化 ---
# プログラムが読み込まれたタイミングで、テーブルが無ければ作っておく
init_db()

# このファイルを直接 `python main.py` で実行したときだけ、サーバーを起動する
if __name__ == "__main__":
    # host="0.0.0.0" で外部からのアクセスも受け付ける。ポート8000で待ち受ける
    uvicorn.run(app, host="0.0.0.0", port=8000)
