install:
	pip3 install -r requirements.txt
	cd frontend && npm install && npm run build
	mv frontend/dist backend/dist

build-front:
	cd frontend && npm run build
	mv frontend/dist backend/dist

up:
	python3 application.py

reload:
	@make build-front
	@make up

