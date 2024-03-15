up:
	sudo docker-compose up -d --build

migrate:
	sudo docker-compose exec -T app python3 manage.py migrate --no-input

collectstatic:
	sudo docker-compose exec -T app python3 manage.py collectstatic --no-input

restart:
	sudo docker-compose restart

deploy: 
	make up migrate collectstatic restart
