# Usage

## Login in CLI

```sh
    mysql -h${dbaddress} -u${username} -p${password} ${dbname}
```

- start tongji VPN before login

## Connect with Django

### 1. Modify Django Settings

In `sailing/settings.py`, change

```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
```

into

```python
    DATABASES = {
        'default': {
            #'ENGINE': 'django.db.backends.sqlite3',
            #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'ENGINE': 'django.db.backends.mysql',
            'NAME': dbname,
            'USER': username,
            'PASSWORD': password,
            'HOST': dbaddress,
            'PORT': '3306',
            'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
            'charset': 'utf8mb4'
            },
        }
    }
```

### 2. Install and Import MySQLdb

```bash
    conda install mysqlclient
```

After installation, modify the `sailing\__init__.py`, add

``` python
    import MySQLdb
```
### 3. Synchronize Tables

If models.py of Apps has been changed, run the following commands before start Django Server

``` python
    python manage.py makemigrations
    python manage.py migrate
```

reference: <https://www.cnblogs.com/zijiyanxi/p/7599052.html>
