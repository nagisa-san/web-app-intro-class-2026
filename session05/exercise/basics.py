"""
第5回 実習3: Pythonスクリプトの作成

スライドの手順に従って、このファイルを編集してください。
  1. TODOリスト（辞書のリスト）を定義する
  2. show_todos 関数を実装する
  3. show_todos(todos) を呼び出す

実行方法:
  python basics.py

期待される出力例:
  [ ] 1: 課題を出す
  [x] 2: 買い物する
  [ ] 3: 自分のTODO
"""
#ヒント: TODOリストを作成する
todos = [
 {"id": 1, "title": "課題を出す", "done": False},
 {"id": 2, "title": "買い物する", "done": True},
   {"id": 3, "title": "自分のTODO", "done": False},
   ]


# ヒント: TODOを1件ずつ表示する関数を作成する
def show_todos(todo_list):
  for todo in todo_list:
   status = "[x]" if todo["done"] else "[ ]"
   print(f'{status} {todo["id"]}: {todo["title"]}')


# ヒント: 関数を呼び出して動作を確認する
show_todos(todos)
