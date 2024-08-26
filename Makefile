no-cache-restart:
	docker-compose down && docker-compose build --no-cache && docker-compose up
restart:
	docker-compose down && docker-compose up
start:
	docker-compose up
dev-start:
	cd weather && flask run
init:
	cd weather && pip install -r requirements.txt && flask run