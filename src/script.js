// 新しいタスクを追加する関数
function addTask() {
    // ユーザーが入力したタスクのテキストを取得
    const taskText = document.getElementById('new-task').value;
    
    // 入力フィールドが空のときはアラートを表示して処理を終了
    if (taskText === "") {
      alert("タスクを入力してください");
      return;
    }
  
    // 新しいタスクを作成してリストに追加
    const taskList = document.getElementById('task-list');
    const newTask = document.createElement('li');
    newTask.textContent = taskText;
  
    // 完了ボタンの作成
    const completeButton = document.createElement('button');
    completeButton.textContent = "完了";
    completeButton.addEventListener('click', () => {
      // 完了ボタンを押すとタスクに取り消し線を引く
      newTask.style.textDecoration = "line-through";
    });
  
    // 削除ボタンの作成
    const deleteButton = document.createElement('button');
    deleteButton.textContent = "削除";
    deleteButton.addEventListener('click', () => {
      // 削除ボタンを押すとタスクをリストから削除
      taskList.removeChild(newTask);
    });
  
    // タスクにボタンを追加
    newTask.appendChild(completeButton);
    newTask.appendChild(deleteButton);
  
    // タスクリストに新しいタスクを追加
    taskList.appendChild(newTask);
  
    // 入力フィールドをクリア
    document.getElementById('new-task').value = "";
  }
  
  // ボタンがクリックされたときにタスクを追加
  document.getElementById('add-task-btn').addEventListener('click', addTask);