web: gunicorn --pythonpath src --bind=0.0.0.0:$PORT --timeout=60 --graceful-timeout=60 --workers=4 src.appserver:app
