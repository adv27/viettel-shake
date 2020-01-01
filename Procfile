release: python manage.py migrate
web: gunicorn config.wsgi:application
worker: celery worker --app=config.celery_app --loglevel=info --pool=gevent --concurrency=$CELERY_CONCURRENCY
