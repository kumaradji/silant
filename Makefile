.PHONY: all

VENV_DIR = /Users/kumar_air/WebstormProjects/silant/venv
VENV_ACTIVATE = source $(VENV_DIR)/bin/activate &&

PROJECT_DIR = /Users/kumar_air/WebstormProjects/silant

all:
	cd $(PROJECT_DIR) && \
	$(VENV_ACTIVATE) python manage.py makemigrations && \
	$(VENV_ACTIVATE) python manage.py migrate && \
	$(VENV_ACTIVATE) python manage.py runserver
