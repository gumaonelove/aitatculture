# Проект с хакатона AiTatCulture
Генерация изображений одежды смешанного стиля современное и старо-татарское

## Датасеты:
+ https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small
+ https://drive.google.com/drive/folders/13rbKnATof4tMHE3vTzUSyhVrxs3EfKp3

## Используемая модель
+ https://github.com/lstein/stable-diffusion

## Описание репозитория
### Директория config
1. **aitatculture.conf** - supervisor config
2. **gunicorn.conf.py** - gunicorn config
3. В которых *gumaonelove* это sudo пользователь системы
4. Локальный сервер 127.0.0.1:8000, проксировать с **kiem.saf.tatar**

### Прочее
1. **req.txt** - файл зависимостей
2. **db.sqlite3** - файл Базы Данных

### Команды администрирования
* `sudo apt install nginx git supervisor`
* `git clone https://github.com/gumaonelove/aitatculture.git`
* `cd aitatculture`
* `sudo apt-get install python3-venv`
* `python3 -m venv venv`
* `source venv/bin/activate`
* `pip install -r req.txt`
* `cd /etc/supervisor/conf.d/`
* `sudo ln /home/gumaonelove/aitatculture/config/aitatculture.conf`
* `sudo update-rc.d supervisor enable`