/**
 * TODO App JavaScript - 完成版
 * 第8回: セキュリティの基礎 & 総仕上げ
 *
 * 【このファイルの役割】
 *  ブラウザの画面（HTML）と、バックエンド（main.py）の橋渡しをする。
 *
 * 【全体の流れ】
 *  1. ページが開かれる → loadTodos() でサーバーからTODO一覧を取得
 *  2. renderTodos() が、取得したデータを画面のリストとして描画する
 *  3. ユーザーが「追加・チェック・削除」を操作する
 *     → 対応する関数がサーバーに変更を送る（fetch）
 *     → 最後にもう一度 loadTodos() して、最新の状態を画面に反映する
 *
 * ※ fetch はサーバーと通信する命令。通信は時間がかかるので、
 *   async / await を使って「結果が返ってくるまで待つ」書き方をしている。
 */

// サーバー側のAPIのアドレス（main.py の @app.get("/todos") などに対応）
const API_URL = "/todos";

// ============================================================
// TODO操作（CRUD）
// ============================================================

/**
 * TODO一覧を取得して表示する
 */
async function loadTodos() {
  // try ... catch: 通信中にエラーが起きても、アプリが止まらないようにする
  try {
    // サーバーに「一覧をください」とお願いし、返事(response)を待つ
    const response = await fetch(API_URL);

    // response.ok が false = サーバーがエラーを返したとき
    if (!response.ok) {
      const error = await response.json(); // エラー内容を取り出す
      showError(error.detail || "TODOの取得に失敗しました");
      return; // ここで処理を終える
    }

    // 返ってきたデータ(JSON)をJavaScriptの配列に変換する
    const todos = await response.json();
    renderTodos(todos); // 画面に描画する
  } catch (error) {
    // そもそもサーバーにつながらなかったときなど
    showError("通信エラーが発生しました");
  }
}

/**
 * 新しいTODOを追加する
 */
async function addTodo() {
  // 入力欄の要素を取得し、入力された文字を読み取る（trimで前後の空白を除去）
  const input = document.getElementById("todo-input");
  const title = input.value.trim();

  // 送信前のチェック（バリデーション）: 空のときは送らずに注意を表示
  if (title === "") {
    showError("TODOのタイトルを入力してください");
    return;
  }

  // 長すぎるときも送らない（サーバー側でも100文字までチェックしている）
  if (title.length > 100) {
    showError("タイトルは100文字以内で入力してください");
    return;
  }

  try {
    // サーバーに「このTODOを追加して」と送る
    const response = await fetch(API_URL, {
      method: "POST", // POST = 新しいデータを作る
      headers: { "Content-Type": "application/json" }, // 中身はJSON形式だと伝える
      body: JSON.stringify({ title: title }), // データをJSON文字列にして送る
    });

    if (!response.ok) {
      const error = await response.json();
      showError(error.detail || "TODOの追加に失敗しました");
      return;
    }

    input.value = ""; // 入力欄を空に戻す
    await loadTodos(); // 一覧を取り直して、追加結果を画面に反映する
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}

/**
 * TODOの完了状態を切り替える
 * id: 対象のTODOの番号 / currentDone: いまの完了状態(true/false)
 */
async function toggleTodo(id, currentDone) {
  try {
    // `${API_URL}/${id}` で /todos/5 のようなアドレスを作る（id=5のTODOが対象）
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT", // PUT = 既存のデータを更新する
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ done: !currentDone }), // !で完了/未完了を反転させる
    });

    if (!response.ok) {
      const error = await response.json();
      showError(error.detail || "TODOの更新に失敗しました");
      return;
    }

    await loadTodos(); // 一覧を取り直して、更新結果を画面に反映する
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}

/**
 * TODOを削除する
 * id: 削除したいTODOの番号
 */
async function deleteTodo(id) {
  try {
    // /todos/5 のようなアドレスに対して削除を依頼する
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE", // DELETE = データを削除する
    });

    if (!response.ok) {
      const error = await response.json();
      showError(error.detail || "TODOの削除に失敗しました");
      return;
    }

    await loadTodos(); // 一覧を取り直して、削除結果を画面に反映する
  } catch (error) {
    showError("通信エラーが発生しました");
  }
}

// ============================================================
// 描画
// ============================================================

/**
 * TODOリストを描画する（XSS対策: createElement + textContent）
 *
 * 受け取ったTODOの配列をもとに、画面に並べる<li>を1件ずつ組み立てる。
 *
 * 【XSS対策のポイント】
 *  innerHTML に文字列を直接入れると、入力に紛れ込んだ<script>などが
 *  実行されてしまう危険がある（XSS）。そこで textContent を使い、
 *  入力を「ただの文字」として扱うことで、この攻撃を防いでいる。
 */
function renderTodos(todos) {
  const list = document.getElementById("todo-list");
  list.innerHTML = ""; // 古い表示を一度すべて消してから描き直す

  // todos配列の1件ずつ(todo)について、リストの行を作る
  todos.forEach((todo) => {
    // <li> 完了済みなら "done" クラスを足して見た目を変える
    const li = document.createElement("li");
    li.className = "todo-item" + (todo.done ? " done" : "");

    // チェックボックスとタイトルをまとめる<label>
    const label = document.createElement("label");
    label.className = "todo-label";

    // 完了チェックボックス
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "todo-checkbox";
    checkbox.checked = todo.done; // いまの完了状態をチェックに反映
    // チェックが変わったら、完了状態を切り替える関数を呼ぶ
    checkbox.addEventListener("change", () => toggleTodo(todo.id, todo.done));

    // TODOのタイトル文字。textContent で安全に入れる（XSS対策）
    const titleSpan = document.createElement("span");
    titleSpan.className = "todo-title";
    titleSpan.textContent = todo.title;

    // label の中に [チェックボックス][タイトル] を入れる
    label.appendChild(checkbox);
    label.appendChild(titleSpan);

    // 削除ボタン。押されたら削除する関数を呼ぶ
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-button";
    deleteBtn.textContent = "削除";
    deleteBtn.addEventListener("click", () => deleteTodo(todo.id));

    // <li> の中に [label][削除ボタン] を入れて、リストに追加する
    li.appendChild(label);
    li.appendChild(deleteBtn);

    list.appendChild(li);
  });
}

// ============================================================
// メッセージ表示
// ============================================================

// エラーメッセージを画面に表示する（5秒後に自動で消える）
function showError(message) {
  const errorDiv = document.getElementById("error-message");
  errorDiv.textContent = message; // メッセージを表示
  errorDiv.style.display = "block"; // 見えるようにする
  // setTimeout: 指定したミリ秒後に処理を実行する。5000ミリ秒 = 5秒
  setTimeout(() => {
    errorDiv.style.display = "none"; // 5秒後に隠す
  }, 5000);
}

// ============================================================
// イベントリスナー
// ============================================================

// フォームが送信された（追加ボタン or Enter）ときの動き
document.getElementById("todo-form").addEventListener("submit", function (e) {
  e.preventDefault(); // ページが再読み込みされる標準動作を止める
  addTodo(); // 自分で用意した追加処理を呼ぶ
});

// ページ読み込み時に、まずTODO一覧を取得して表示する（ここがスタート地点）
loadTodos();
