install:
	pip3 install -r requirements.txt
	cd frontend && npm install
	@make build-front

build-front:
	cd frontend && npm run build
	rm -rf backend/dist
	mv frontend/dist backend/dist

up:
	python3 application.py

reload:
	@make build-front
	@make up

