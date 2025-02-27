// 必要なライブラリを読み込む
const express = require('express');
const app = express();
const PORT = 3000;

// データをJSON形式でやり取りできるように設定
app.use(express.json());

// タスクを保存するための仮のデータ（配列）
let tasks = [];

// タスクを取得するためのエンドポイント（GETリクエスト）
app.get('/tasks', (req, res) => {
  res.json(tasks);
});

// 新しいタスクを追加するためのエンドポイント（POSTリクエスト）
app.post('/tasks', (req, res) => {
  const newTask = req.body;
  tasks.push(newTask);
  res.status(201).json(newTask);  // ステータス201は「作成成功」を意味する
});

// サーバーを起動する
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});