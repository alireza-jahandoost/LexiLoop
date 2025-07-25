# 🇮🇹 LexiLoop — Smart Italian Language Bot

LexiLoop is a Telegram automation system designed to enrich your Italian language Telegram channel with smart, engaging posts — including vocabulary, grammar tips, and false friends. It automatically generates, reviews, and publishes content while keeping your content buffer healthy.
<p align="center">
  <img src="/logo.png" alt="LexiLoop Logo" width="200" style="border-radius: 50%;" />
</p>

---

## ✨ Features

- 📚 **Vocabulary Posts** — Introduce Italian words with context and examples.
- 🧠 **Grammar Tips** — Concise insights with examples to help users improve.
- ⚠️ **False Friends** — Clarify tricky Italian-English lookalikes.
- ✅ **Post Review** — Built-in AI agent judges the quality of each post before publication.
- 🗂️ **Smart Topic History** — Prevents repetition with recent topic memory.
- 📤 **Telegram Publishing** — Sends formatted posts to a Telegram channel.
- ♻️ **Maintenance Mode** — Automatically fills the queue if content is low.
- 📊 **Admin Alerts** — Sends stats and status updates to the channel owner.
- 🕰️ **Cron-Based Scheduling** — Publish different post types at specific times.

---

Here's the updated `README.md` with the **Quick Start** section rewritten for **Docker** users. This assumes you want a simple way to run the app with Docker and use `.env` variables for configuration.

---
## 🚀 Quick Start (with Docker)

### 1. Clone the project
```bash
git clone https://github.com/yourusername/lexiloop.git
cd lexiloop
````

### 2. Create a `.env` file

```env
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=@your_channel_or_user_id
ADMIN_ID=123456789

MONGO_USER=your_user
MONGO_PASS=your_password
MONGO_CLUSTER=your_cluster.mongodb.net
MONGO_DB=db_name

# UTC-based hours for cron_runner
MAINTAIN_HOUR=4
CHECK_HOUR=7
PUBLISH_VOCAB_HOUR=8
PUBLISH_FALSE_HOUR=10
PUBLISH_GRAMMAR_HOUR=15
```

### 3. Build the Docker image

```bash
docker build -t lexiloop .
```

### 4. Run any command

Generate vocabulary posts:

```bash
docker run --env-file .env lexiloop python main.py generate --type vocab --count 5
```

Run the cron handler:

```bash
docker run --env-file .env lexiloop python cron_runner.py
```

Send a test message to Telegram:

```bash
docker run --env-file .env lexiloop python scripts/test_message.py
```

> ℹ️ Make sure your `.env` file is in the root directory when running Docker.

## 🧠 CLI Usage

### 🛠 Generate new posts

```bash
python main.py generate --type vocab --count 5
python main.py generate --type grammar --count 2
python main.py generate --type false_friend
```

### 🚀 Publish to Telegram

```bash
python main.py publish --type vocab
```

### 🧼 Maintain buffer if under threshold

```bash
python main.py maintain --type vocab grammar --threshold 10 --count 10
```

### 📊 Admin check of buffer status

```bash
python main.py check
```

---

## 🕰️ Cron Scheduling (e.g., in Railway)

Use the hourly cron job to run:

```bash
python cron_runner.py
```

And LexiLoop will decide what to do based on current UTC time and `.env`.

---

## 🧱 Project Structure

```
.
├── agents/
│   ├── generators/
│   └── review/
├── commands/
├── helper_functions/
├── storage/
├── data/
│   ├── categories/
│   └── prompts/
├── logs/
├── scripts/
├── main.py
├── cron_runner.py
```

---

## 📦 Deployment (Railway Recommended)

* Railway offers **free cron job runners**
* Set the hourly schedule: `0 * * * *`
* Start command: `python cron_runner.py`
* Use `.env` to set publish hours in UTC

---

## 🤖 Telegram Bot Permissions

Make sure your bot:

* Is an **admin** in the target channel
* Has permissions to **send messages** and **markdown formatting**

---

## 🛡️ Security Note

If using `0.0.0.0/0` for MongoDB access during development, restrict IPs in production or use VPC Peering with Atlas.

---

## 🧑‍💻 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feat/new-stuff`)
3. Commit your changes (`git commit -m "add amazing thing"`)
4. Push to the branch (`git push origin feat/new-stuff`)
5. Open a Pull Request ✅

---

## 📜 License

MIT License © 2025 \ Alireza Jahandoost
