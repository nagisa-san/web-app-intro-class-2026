// ============================================================
// TODOアプリ JavaScript - 実習用スターター
// 第4回: JavaScript基礎 — TODOアプリに動きをつける
//
// TODO コメントを参考に、各関数を実装してください。
// ============================================================
 
// ------------------------------------------------------------
// TODOデータを管理する配列
// 各要素は { title: "文字列", done: true/false } の形式
// ------------------------------------------------------------
let todos = [];
 
// ------------------------------------------------------------
// DOM要素の取得
// ------------------------------------------------------------
const todoForm = document.getElementById("todo-form");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");
 
// ============================================================
// addTodo: 新しいTODOを配列に追加する
//
// 処理:
//   1. titleが空文字なら何もしない（return）
//   2. { title: title, done: false } を todos に push
//   3. render() を呼んで画面を再描画
// ============================================================
function addTodo(title) {
  // ヒント:
  //   if (title === "") return;
  //   todos.push({ title: title, done: false });
  //   render();
  if (title === "") return;
  todos.push({ title: title, done: false });
  render();
}
 
// ============================================================
// toggleTodo: TODOの完了状態を切り替える
//
// 処理:
//   1. todos[index].done の値を反転（ !todos[index].done ）
//   2. render() を呼んで画面を再描画
// ============================================================
function toggleTodo(index) {
  // ヒント:
  //   todos[index].done = !todos[index].done;
  //   render();
  todos[index].done = !todos[index].done;
  render();
}
 
// ============================================================
// deleteTodo: TODOを削除する
//
// 処理:
//   1. todos.splice(index, 1) で配列から削除
//   2. render() を呼んで画面を再描画
// ============================================================
function deleteTodo(index) {
  // ヒント:
  //   todos.splice(index, 1);
  //   render();
  todos.splice(index, 1);
  render()
}
 
// ============================================================
// render: TODOリストを画面に描画する
//
// 処理:
//   1. todoList.innerHTML = "" でリストを空にする
//   2. todosが空なら「TODOがありません」メッセージを表示
//   3. todos.forEach で各TODOの要素を作成:
//      - li要素を作成、class="todo-item" を設定
//      - done なら class に "done" を追加
//      - label要素（class="todo-label"）を作成
//      - checkbox（class="todo-checkbox"）を作成
//      - span（class="todo-title"）に textContent でタイトルを設定
//      - 削除ボタン（class="delete-button"）を作成
//      - 各要素を組み立てて todoList に追加
//   4. todoList に li を appendChild
// ============================================================
function render() {
  // ステップ1: リストを空にする
  // ステップ2: todosが空の場合の処理
  // ステップ3: todosの各要素を描画
  // ヒント:
  //   todos.forEach((todo, index) => {
  //     const li = document.createElement("li");
  //     li.className = "todo-item" + (todo.done ? " done" : "");
  //
  //     const label = document.createElement("label");
  //     label.className = "todo-label";
  //
  //     const checkbox = document.createElement("input");
  //     checkbox.type = "checkbox";
  //     checkbox.className = "todo-checkbox";
  //     checkbox.checked = todo.done;
  //     checkbox.addEventListener("change", () => toggleTodo(index));
  //
  //     const span = document.createElement("span");
  //     span.className = "todo-title";
  //     span.textContent = todo.title;
  //
  //     const deleteBtn = document.createElement("button");
  //     deleteBtn.className = "delete-button";
  //     deleteBtn.textContent = "削除";
  //     deleteBtn.addEventListener("click", () => deleteTodo(index));
  //
  //     label.appendChild(checkbox);
  //     label.appendChild(span);
  //     li.appendChild(label);
  //     li.appendChild(deleteBtn);
  //     todoList.appendChild(li);
  //   });
  todos.forEach((todo, index) => {
       const li = document.createElement("li");
       li.className = "todo-item" + (todo.done ? " done" : "");
 
       const label = document.createElement("label");
       label.className = "todo-label";
 
       const checkbox = document.createElement("input");
       checkbox.type = "checkbox";
       checkbox.className = "todo-checkbox";
       checkbox.checked = todo.done;
      checkbox.addEventListener("change", () => toggleTodo(index));
 
       const span = document.createElement("span");
       span.className = "todo-title";
       span.textContent = todo.title;
 
       const deleteBtn = document.createElement("button");
       deleteBtn.className = "delete-button";
       deleteBtn.textContent = "削除";
       deleteBtn.addEventListener("click", () => deleteTodo(index));
 
       label.appendChild(checkbox);
       label.appendChild(span);
       li.appendChild(label);
      li.appendChild(deleteBtn);
      todoList.appendChild(li);
    });
}
 
// ============================================================
// フォーム送信イベント（実装済み）
// ============================================================
todoForm.addEventListener("submit", (event) => {
  event.preventDefault();
  addTodo(todoInput.value.trim());
  todoInput.value = "";
  todoInput.focus();
});
 
// ============================================================
// 初期表示
// ============================================================
render();