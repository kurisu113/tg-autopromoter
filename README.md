# 🚀 TG-AutoPromoter & Group Parser

A modular and customizable Python suite powered by **Telethon** (Telegram Client API) for discovering public Telegram groups and automating post distribution.

## 📌 Features

- **`parser.py`**: Searches public Telegram groups by keywords (`keywords.txt`), filters channels, and saves active megagroups with member counts.
- **`poster.py`**: Automated messaging using multi-template rotation (`templates.txt`). Includes auto-joining, flood-wait handling, and auto-removal of read-only/restricted chats.
- **DevSecOps Ready**: Credential isolation via environment variables (`python-dotenv`).

## 🛠 Setup & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/tg-autopromoter.git](https://github.com/YOUR_USERNAME/tg-autopromoter.git)
   cd tg-autopromoter