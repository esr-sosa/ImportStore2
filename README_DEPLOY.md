# 🚀 Guía Rápida de Deploy - ImportStore

## ⚡ Deploy en un Solo Comando

```bash
./deploy.sh production
```

O usando Make:

```bash
make deploy
```

---

## 📋 Pasos Previos

### 1. Configurar variables de entorno

```bash
cp env.example .env
nano .env  # Completar con tus valores
```

**Variables obligatorias:**
- `DJANGO_SECRET_KEY` - Generar con: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DJANGO_ALLOWED_HOSTS` - Tu dominio (ej: `tu-dominio.com,www.tu-dominio.com`)
- `DB_PASSWORD` - Password segura para PostgreSQL
- `NEXT_PUBLIC_API_URL` - URL de tu API

### 2. Instalar Docker y Docker Compose

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

---

## 🎯 Proveedores Recomendados

### 💰 Opción Más Económica: DigitalOcean

1. **Crear Droplet** (Ubuntu 22.04, 2GB RAM, $12/mes)
2. **Crear Base de Datos PostgreSQL** ($15/mes)
3. **Configurar dominio** (apuntar DNS al Droplet)
4. **Ejecutar deploy**

**Total: ~$27/mes**

### 🌍 Alternativas Económicas:

- **Vultr**: $5-10/mes (VPS)
- **Hetzner**: €4-8/mes (Europa)
- **Railway**: $5/mes + uso (Serverless)

---

## 🔧 Comandos Útiles

```bash
# Ver logs
make logs

# Reiniciar servicios
make restart

# Ejecutar migraciones
make migrate

# Crear superusuario
make createsuperuser

# Backup de base de datos
make backup

# Ver estado
make ps
```

---

## 🔒 Configurar SSL (HTTPS)

### Con Certbot (Let's Encrypt - Gratis):

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Luego actualizar `.env`:
```env
DJANGO_CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
NEXT_PUBLIC_API_URL=https://api.tu-dominio.com
```

---

## 📊 Estructura del Deploy

```
┌─────────────┐
│   Nginx     │  ← Puerto 80/443 (Reverse Proxy)
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼───┐ ┌─▼──────┐
│Front │ │Backend │
│Next  │ │Django  │
└──┬───┘ └───┬────┘
   │         │
   └────┬────┘
        │
    ┌───▼───┐
    │  DB   │
    │Postgre│
    └───────┘
```

---

## 🆘 Problemas Comunes

### Error: Puerto 80 en uso
```bash
sudo lsof -i :80
# Cambiar puerto en .env: NGINX_HTTP_PORT=8080
```

### Error: Base de datos no conecta
```bash
# Verificar que DB esté corriendo
make ps
# Ver logs
make logs-backend
```

### Error: Permisos
```bash
sudo chown -R $USER:$USER .
```

---

## 📝 Checklist Pre-Deploy

- [ ] `.env` configurado con valores reales
- [ ] `DJANGO_SECRET_KEY` generado
- [ ] `DEBUG=False` en producción
- [ ] Dominio apuntando al servidor
- [ ] SSL configurado (HTTPS)
- [ ] Backup de base de datos configurado
- [ ] Firewall abierto (puertos 80, 443, 22)

---

**¡Listo para desplegar! 🚀**

Para más detalles, ver [DEPLOY.md](./DEPLOY.md)

