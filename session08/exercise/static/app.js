/**
 * TODO App JavaScript - 実習用スターター
 * 第8回: セキュリティの基礎 & 総仕上げ
 *
 * 第7回の正解をベースに、XSS脆弱性やバリデーション不足を残しています。
 * TODO コメントの指示に従って安全なコードに修正してください。
 */

const API_URL = "/todos";

// ============================================================
// TODO操作（CRUD）
// ============================================================

/**
 * TODO一覧を取得して表示する
 */
async function loadTodos() {
  // TODO(実習5): try-catch でエラーハンドリングを追加してください
  //   ヒント:
  //   try {
  //     const response = await fetch(API_URL);
  //     if (!response.ok) {
  //       const error = await response.json();
  //       showError(error.detail || "TODOの取得に失敗しました");
  //       return;
  //     }
  //     const todos = await response.json();
  //     renderTodos(todos);
  //   } catch (error) {
  //     showError("通信エラーが発生しました");
  //   }

  const response = await fetch(API_URL);
  const todos = await response.json();
  renderTodos(todos);
}

/**
 * 新しいTODOを追加する
 */
async function addTodo() {
  const input = document.getElementById("todo-input");
  const title = input.value.trim();

  // TODO(実習4): クライアント側バリデーションを追加してください
  //   1. title === "" なら showError("TODOのタイトルを入力してください") で return
  //   2. title.length > 100 なら showError("タイトルは100文字以内で入力してください") で return

  // TODO(実習5): try-catch でエラーハンドリングを追加してください
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: title }),
  });

  input.value = "";
  await loadTodos();
}

/**
 * TODOの完了状態を切り替える
 */
async function toggleTodo(id, currentDone) {
  // TODO(実習5): try-catch でエラーハンドリングを追加してください
  await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ done: !currentDone }),
  });

  await loadTodos();
}

/**
 * TODOを削除する
 */
async function deleteTodo(id) {
  // TODO(実習5): try-catch でエラーハンドリングを追加してください
  await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
  });

  await loadTodos();
}

// ============================================================
// 描画
// ============================================================

/**
 * TODOリストを描画する
 *
 * 注意: この関数にはXSS脆弱性があります！
 *       第7回と同じく <label class="todo-label"> で checkbox + span を包む構造です。
 */
function renderTodos(todos) {
  const list = document.getElementById("todo-list");
  list.innerHTML = "";

  todos.forEach((todo) => {
    const li = document.createElement("li");
    li.className = "todo-item" + (todo.done ? " done" : "");

    // TODO(実習2): XSS脆弱性を修正してください
    //   innerHTML を使うと、ユーザー入力がHTMLとして解釈されてしまいます。
    //   createElement + textContent に書き換えてください。
    //
    //   修正後（第7回と同じ構造）:
    //     const label = document.createElement("label");
    //     label.className = "todo-label";
    //
    //     const checkbox = document.createElement("input");
    //     checkbox.type = "checkbox";
    //     checkbox.className = "todo-checkbox";
    //     checkbox.checked = todo.done;
    //     checkbox.addEventListener("change", () => toggleTodo(todo.id, todo.done));
    //
    //     const titleSpan = document.createElement("span");
    //     titleSpan.className = "todo-title";
    //     titleSpan.textContent = todo.title;
    //
    //     label.appendChild(checkbox);
    //     label.appendChild(titleSpan);
    //
    //     const deleteBtn = document.createElement("button");
    //     deleteBtn.className = "delete-button";
    //     deleteBtn.textContent = "削除";
    //     deleteBtn.addEventListener("click", () => deleteTodo(todo.id));
    //
    //     li.appendChild(label);
    //     li.appendChild(deleteBtn);

    // 危険！ innerHTML を使用（XSS脆弱性あり）
    //li.innerHTML = `
      //<label class="todo-label">
        //<input type="checkbox" class="todo-checkbox"
          //${todo.done ? "checked" : ""}
          //onchange="toggleTodo(${todo.id}, ${todo.done})">
        //<span class="todo-title">${todo.title}</span>
      //</label>
      //<button class="delete-button" onclick="deleteTodo(${todo.id})">削除</button>
    //`;

    list.appendChild(li);
  });
}

// ============================================================
// メッセージ表示
// ============================================================

// TODO(実習5): showError 関数を実装してください
//   ヒント:
   function showError(message) {
     const errorDiv = document.getElementById("error-message");
     errorDiv.textContent = message;
     errorDiv.style.display = "block";
     setTimeout(() => {
       errorDiv.style.display = "none";
     }, 5000);
   }

// ============================================================
// イベントリスナー
// ============================================================

document.getElementById("todo-form").addEventListener("submit", function (e) {
  e.preventDefault();
  addTodo();
});

// ページ読み込み時にTODO一覧を取得
loadTodos();
