# LoveGram Django Chat Project

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]() [![License](https://img.shields.io/badge/license-MIT-blue)]() \[![Version](https://img.shields.io/badge/version-1.0.0-lightgrey)]

A **Django-based chat and social networking platform** called LoveGram. This project features custom user authentication, private and group chats, messaging with file attachments, notifications, and user profiles.

---

## Table of Contents

* [About](#about)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Environment Variables](#environment-variables)
  * [Running Locally](#running-locally)
* [Templates (Frontend)](#templates-frontend)
* [URL Routes](#url-routes)
* [File Structure](#file-structure)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)

---

## About

LoveGram is a **real-time chat and social networking platform** built with Django 5.1.3. Users can register with a phone number, login, verify their account, create private or group chats, send messages with files, and manage their profile.

---

## Features

* Custom user model with phone number, verification status, and online presence.
* Private and group chat support.
* Send messages with text and file attachments.
* Notifications for new messages.
* User profile management with avatars and bios.
* Chat creation, adding participants, editing and deleting messages.
* Authentication with registration, login, logout, and verification.

---

## Tech Stack

* **Framework:** Django 5.1.3
* **Language:** Python 3.11+
* **Database:** SQLite (default)
* **Frontend:** Django Templates (HTML, CSS, Bootstrap optional)
* **Other Libraries:** Pillow (for image uploads)

---

## Getting Started

### Prerequisites

* Python 3.11+
* pip
* Git

### Installation

```bash
# Clone repository
git clone https://github.com/<your-org>/<repo>.git
cd <repo>

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser
```

### Environment Variables

* `SECRET_KEY` → Django secret key (set in settings.py)
* `DEBUG` → True for development, False for production
* `ALLOWED_HOSTS` → List of allowed hosts for deployment

### Running Locally

```bash
python manage.py runserver
```

Access the project at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Templates (Frontend)

The application includes the following **HTML templates**:

* `add_participant.html` — Add a user to an existing group chat.
* `chat_detail.html` — Display messages in a chat, send messages, view notifications.
* `chat_list.html` — List of all chats the user is part of.
* `create_chat.html` — Form to create a private chat.
* `create_edit_profile.html` — Form to create or edit user profile.
* `create_group.html` — Form to create a group chat.
* `edit_message.html` — Edit a sent message.
* `find_user.html` — Search for a user to start a chat.
* `login.html` — User login form.
* `profile_detail.html` — Display user profile.
* `register.html` — User registration form.
* `verify.html` — Verification code input page.

---

## URL Routes

| Path                           | View                         | Description                       |
| ------------------------------ | ---------------------------- | --------------------------------- |
| `/register/`                   | `register`                   | Register a new user               |
| `/verify/`                     | `verify`                     | Verify account using phone number |
| `/login/`                      | `login_view`                 | Login page                        |
| `/`                            | `chat_list`                  | List all chats                    |
| `/chat/<id>/`                  | `chat_detail`                | Display a chat's messages         |
| `/chat/create/`                | `create_chat`                | Create a private chat             |
| `/chats/create_group/`         | `create_group`               | Create a group chat               |
| `/edit_message/<id>/`          | `edit_message`               | Edit a message                    |
| `/delete_message/<id>/`        | `delete_message`             | Delete a message                  |
| `/add_participant/<id>/`       | `add_participant`            | Add participant to group          |
| `/mark_notifications_as_read/` | `mark_notifications_as_read` | Mark all notifications as read    |
| `/find_user/`                  | `find_user_and_create_chat`  | Search user and create chat       |
| `/profile/`                    | `create_or_edit_profile`     | Edit or create profile            |
| `/profile/<id>/`               | `profile_detail`             | View profile details              |
| `/delete_chat/<id>/`           | `delete_chat`                | Delete a chat                     |
| `/profile/delete-avatar/`      | `delete_avatar`              | Remove profile avatar             |
| `/admin/`                      | Django Admin                 | Admin dashboard                   |

---

## File Structure

```
project_root/
├─ DJ_lovegram/             # Django project config
│  ├─ settings.py           # Project settings
│  ├─ urls.py               # Project URLs
│  ├─ wsgi.py
│
├─ lovegram/               # Main app
│  ├─ models.py             # User, Chat, Message, Notification, Profile
│  ├─ views.py              # Views for authentication, chat, profile
│  ├─ forms.py              # Forms for chat, message, profile
│  ├─ middleware.py         # Last activity middleware
│  ├─ urls.py               # App-specific routes
│  ├─ templates/            # Frontend templates
│  │  ├─ add_participant.html
│  │  ├─ chat_detail.html
│  │  ├─ chat_list.html
│  │  ├─ create_chat.html
│  │  ├─ create_edit_profile.html
│  │  ├─ create_group.html
│  │  ├─ edit_message.html
│  │  ├─ find_user.html
│  │  ├─ login.html
│  │  ├─ profile_detail.html
│  │  ├─ register.html
│  │  └─ verify.html
│
├─ media/                  # Uploaded files (avatars, messages)
├─ manage.py
├─ requirements.txt
```

---

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/awesome-feature`)
3. Commit changes (`git commit -m "Add awesome feature"`)
4. Push to branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

---

## Authors

* **arash** — *Initial Work* — [arashey](https://github.com/arashey)
 

---


