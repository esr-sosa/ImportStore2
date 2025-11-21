.PHONY: help build up down restart logs shell migrate collectstatic createsuperuser backup restore clean

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?##' Makefile | awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir imágenes Docker
	docker-compose -f docker-compose.prod.yml build

up: ## Iniciar todos los servicios
	docker-compose -f docker-compose.prod.yml up -d

down: ## Detener todos los servicios
	docker-compose -f docker-compose.prod.yml down

restart: ## Reiniciar todos los servicios
	docker-compose -f docker-compose.prod.yml restart

logs: ## Ver logs de todos los servicios
	docker-compose -f docker-compose.prod.yml logs -f

logs-backend: ## Ver logs del backend
	docker-compose -f docker-compose.prod.yml logs -f backend

logs-frontend: ## Ver logs del frontend
	docker-compose -f docker-compose.prod.yml logs -f frontend

shell: ## Abrir shell en el contenedor backend
	docker-compose -f docker-compose.prod.yml exec backend bash

migrate: ## Ejecutar migraciones
	docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

makemigrations: ## Crear nuevas migraciones
	docker-compose -f docker-compose.prod.yml exec backend python manage.py makemigrations

collectstatic: ## Recopilar archivos estáticos
	docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

createsuperuser: ## Crear superusuario
	docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

backup: ## Hacer backup de la base de datos
	docker-compose -f docker-compose.prod.yml exec db pg_dump -U $$(grep DB_USER .env | cut -d '=' -f2) $$(grep DB_NAME .env | cut -d '=' -f2) > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup guardado en backup_$$(date +%Y%m%d_%H%M%S).sql"

restore: ## Restaurar backup (uso: make restore FILE=backup.sql)
	docker-compose -f docker-compose.prod.yml exec -T db psql -U $$(grep DB_USER .env | cut -d '=' -f2) $$(grep DB_NAME .env | cut -d '=' -f2) < $(FILE)

clean: ## Limpiar contenedores, imágenes y volúmenes no usados
	docker-compose -f docker-compose.prod.yml down -v
	docker system prune -af

ps: ## Ver estado de los contenedores
	docker-compose -f docker-compose.prod.yml ps

deploy: ## Deploy completo (build + up + migrate + collectstatic)
	@echo "🚀 Iniciando deploy..."
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml up -d
	@echo "⏳ Esperando a que los servicios estén listos..."
	sleep 10
	docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
	docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
	@echo "✅ Deploy completado!"

