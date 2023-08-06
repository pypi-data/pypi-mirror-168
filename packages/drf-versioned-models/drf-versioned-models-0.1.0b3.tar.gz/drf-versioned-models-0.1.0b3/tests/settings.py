"""
测试模拟声明式配置文件
"""

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    "tests",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    }
}

ROOT_URLCONF = "tests.urls"
