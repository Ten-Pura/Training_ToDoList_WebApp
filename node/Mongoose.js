const express = require('express');
const mongoose = require('mongoose');
const app = express();
const PORT = 3000;

//MongoDBに接続
mongoose.connect('mongodb+srv://taichi1166:<db_password>@cluster0.jslmr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

//タスクのスキーマ（データ構造）を定義
const taskSchema = new mongoose.Schema({
    text: String,
    completed: Boolean,
});

//モデルを作成
const Task = mongoose.model('Task', taskSchema);

app.use(express.json());

//タスクを取得するエンドポイント（GETリクエスト）
app.get('/tasks', async (req, res) => {
    const tasks = await Task.find();
    res.json(tasks);
});

//新しいタスクを追加するエンドポイント（POSTリクエスト）
app.post('/tasks', async (req, res) => {
    const newTask = new Task(req.body);
    await nwsTask.save();
    res.status(201).json(newTask);
});

//サーバーを起動する
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});