# Learning management system backend (API) using django rest framework

# Requirements:

> The following programs are required to run the project

- [Python3.8+](https://www.python.org/downloads/)
- [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)
- [Database](any)

# Installation

- Clone the repo with

```bash
git clone https://github.com/ngerakam/iLearn_lms_backend.git
```

- Create and activate a python virtual environment

```bash
pip install -r requirements.txt
```

- Create `.env` file inside the root directory and include the following variables

```bash
# Database config
DB_NAME=[YOUR_DB_NAME]
DB_USER=[DB_ADMIN_NAME]
DB_PASSWORD=[DB_ADMIN_PASSWORD]
DB_HOST=localhost
DB_PORT=[YOUR_POSTGRES_PORT ]

# Email config
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=[]
EMAIL_PORT=[]
EMAIL_USE_TLS=[True]
EMAIL_HOST_USER=[your_email@example.com]
EMAIL_HOST_PASSWORD=[your_email_password]

# Other
SECRET_KEY=[YOUR_SECRET_KEY]
```

## Migration order

```python
python manage.py makemigrations authentication
python manage.py migrate authentication

python manage.py makemigrations course
python manage.py migrate course

python manage.py makemigrations activity
python manage.py migrate activity

python manage.py makemigrations quiz
python manage.py migrate quiz

python manage.py makemigrations notifications
python manage.py migrate notifications

python manage.py makemigrations stats
python manage.py migrate stats

```

Then migrate the whole app with no arguments to migrate dependancy apps

```python
python manage.py makemigrations
python manage.py migrate
```
