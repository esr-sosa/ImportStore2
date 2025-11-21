# 🚀 Guía de Deploy - ImportStore

Esta guía te ayudará a desplegar ImportStore en la nube de forma profesional y económica.

## 📋 Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración Inicial](#configuración-inicial)
3. [Proveedores Recomendados](#proveedores-recomendados)
4. [Deploy con Docker](#deploy-con-docker)
5. [Deploy Manual](#deploy-manual)
6. [Configuración de SSL](#configuración-de-ssl)
7. [Mantenimiento](#mantenimiento)

---

## 📦 Requisitos Previos

- Docker y Docker Compose instalados
- Git
- Un dominio (opcional pero recomendado)
- Acceso SSH a tu servidor

---

## ⚙️ Configuración Inicial

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd ImportStore
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
nano .env  # o tu editor preferido
```

**Variables críticas a configurar:**

```env
DJANGO_SECRET_KEY=genera-una-key-segura-aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

DB_NAME=importstore
DB_USER=importstore_user
DB_PASSWORD=password-super-segura

NEXT_PUBLIC_API_URL=https://api.tu-dominio.com
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### 3. Generar Secret Key de Django

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 💰 Proveedores Recomendados (Económicos)

### 🥇 Opción 1: DigitalOcean (Recomendado)

**Ventajas:**
- Muy fácil de usar
- Precios transparentes
- Excelente documentación
- Soporte 24/7

**Costos estimados:**
- Droplet (VPS): $6-12/mes (1GB-2GB RAM)
- Managed PostgreSQL: $15/mes (1GB RAM)
- **Total: ~$21-27/mes**

**Pasos:**
1. Crear cuenta en [DigitalOcean](https://www.digitalocean.com/)
2. Crear un Droplet (Ubuntu 22.04, mínimo 2GB RAM)
3. Crear una base de datos PostgreSQL Managed
4. Seguir [guía de deploy](#deploy-con-docker)

---

### 🥈 Opción 2: Vultr

**Ventajas:**
- Muy económico
- Buena performance
- Múltiples ubicaciones

**Costos estimados:**
- VPS: $5-10/mes (1GB-2GB RAM)
- Base de datos: Incluida en VPS o externa
- **Total: ~$5-10/mes**

---

### 🥉 Opción 3: Hetzner Cloud

**Ventajas:**
- Muy económico (Europa)
- Excelente performance
- Precios en EUR

**Costos estimados:**
- VPS: €4-8/mes (2GB-4GB RAM)
- Base de datos: Incluida o externa
- **Total: ~€4-8/mes**

---

### 🌐 Opción 4: Railway / Render (Serverless)

**Ventajas:**
- Deploy automático desde Git
- Sin configuración de servidor
- Escalado automático

**Costos estimados:**
- Railway: $5/mes + uso
- Render: $7/mes por servicio
- **Total: ~$15-25/mes**

---

## 🐳 Deploy con Docker (Recomendado)

### Deploy en un solo comando:

```bash
chmod +x deploy.sh
./deploy.sh production
```

### Pasos manuales:

```bash
# 1. Construir imágenes
docker-compose -f docker-compose.prod.yml build

# 2. Iniciar servicios
docker-compose -f docker-compose.prod.yml up -d

# 3. Ejecutar migraciones
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# 4. Crear superusuario
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# 5. Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🔧 Deploy Manual (Sin Docker)

### Backend (Django)

```bash
# 1. Instalar dependencias
cd sistema_negocio
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
pip install gunicorn psycopg2-binary

# 2. Configurar base de datos
export DJANGO_SETTINGS_MODULE=core.settings_production
python manage.py migrate

# 3. Recopilar archivos estáticos
python manage.py collectstatic --noinput

# 4. Iniciar con Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 core.wsgi:application
```

### Frontend (Next.js)

```bash
# 1. Instalar dependencias
cd frontend
npm install

# 2. Build de producción
NEXT_PUBLIC_API_URL=https://api.tu-dominio.com npm run build

# 3. Iniciar servidor
npm start
```

---

## 🔒 Configuración de SSL (HTTPS)

### Opción 1: Certbot (Let's Encrypt - Gratis)

```bash
# Instalar Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovación automática
sudo certbot renew --dry-run
```

### Opción 2: Cloudflare (Gratis)

1. Registrar dominio en Cloudflare
2. Configurar DNS
3. Activar SSL/TLS (modo Flexible o Full)
4. Configurar proxy en Cloudflare

---

## 📊 Monitoreo y Logs

### Ver logs en tiempo real:

```bash
# Todos los servicios
docker-compose -f docker-compose.prod.yml logs -f

# Solo backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Solo frontend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Monitoreo de recursos:

```bash
# Uso de recursos
docker stats

# Estado de contenedores
docker-compose -f docker-compose.prod.yml ps
```

---

## 🔄 Actualizaciones

### Actualizar código:

```bash
# 1. Hacer pull del código
git pull origin main

# 2. Reconstruir y reiniciar
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Ejecutar migraciones si hay cambios
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

---

## 🛠️ Comandos Útiles

```bash
# Reiniciar un servicio específico
docker-compose -f docker-compose.prod.yml restart backend

# Ver logs de un servicio
docker-compose -f docker-compose.prod.yml logs backend

# Ejecutar comandos Django
docker-compose -f docker-compose.prod.yml exec backend python manage.py <comando>

# Backup de base de datos
docker-compose -f docker-compose.prod.yml exec db pg_dump -U importstore_user importstore > backup.sql

# Restaurar backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U importstore_user importstore < backup.sql

# Limpiar recursos no usados
docker system prune -a
```

---

## 🚨 Troubleshooting

### Error: Puerto ya en uso

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :80
sudo lsof -i :443

# Cambiar puertos en .env
NGINX_HTTP_PORT=8080
NGINX_HTTPS_PORT=8443
```

### Error: Base de datos no conecta

```bash
# Verificar que el contenedor de DB esté corriendo
docker-compose -f docker-compose.prod.yml ps db

# Ver logs de DB
docker-compose -f docker-compose.prod.yml logs db

# Verificar variables de entorno
docker-compose -f docker-compose.prod.yml exec backend env | grep DB_
```

### Error: Permisos de archivos

```bash
# Ajustar permisos
sudo chown -R $USER:$USER media/ staticfiles/
chmod -R 755 media/ staticfiles/
```

---

## 📝 Checklist Pre-Deploy

- [ ] Variables de entorno configuradas (.env)
- [ ] SECRET_KEY generado y seguro
- [ ] DEBUG=False en producción
- [ ] ALLOWED_HOSTS configurado
- [ ] Base de datos configurada
- [ ] SSL/HTTPS configurado
- [ ] Backup de base de datos configurado
- [ ] Monitoreo configurado
- [ ] Dominio apuntando al servidor
- [ ] Firewall configurado (solo puertos 80, 443, 22)

---

## 🆘 Soporte

Si tenés problemas con el deploy:

1. Revisá los logs: `docker-compose logs`
2. Verificá las variables de entorno
3. Consultá la documentación de tu proveedor
4. Revisá los issues del repositorio

---

**¡Listo para desplegar! 🚀**

