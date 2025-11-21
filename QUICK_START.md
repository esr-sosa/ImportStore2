# ⚡ Quick Start - Deploy ImportStore

## 🚀 Deploy en 3 Pasos

### 1. Configurar variables de entorno

```bash
cp env.example .env
nano .env  # Completar con tus valores
```

**Generar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Deploy

```bash
./deploy.sh production
```

### 3. Crear superusuario

```bash
make createsuperuser
```

---

## 📁 Archivos Creados

### Docker
- `Dockerfile.backend` - Imagen Docker para Django
- `Dockerfile.frontend` - Imagen Docker para Next.js
- `docker-compose.yml` - Desarrollo
- `docker-compose.prod.yml` - Producción

### Configuración
- `env.example` - Template de variables de entorno
- `sistema_negocio/core/settings_production.py` - Settings de producción
- `nginx/` - Configuración de Nginx

### Scripts
- `deploy.sh` - Script de deploy automatizado
- `Makefile` - Comandos útiles
- `scripts/backup-db.sh` - Backup de base de datos

### Documentación
- `DEPLOY.md` - Guía completa de deploy
- `README_DEPLOY.md` - Guía rápida
- `PROVEEDORES.md` - Comparativa de proveedores

---

## 🎯 Comandos Principales

```bash
# Deploy completo
make deploy

# Ver logs
make logs

# Reiniciar
make restart

# Backup
make backup

# Migraciones
make migrate
```

---

## 💰 Costos Estimados

- **DigitalOcean**: $27/mes (recomendado)
- **Vultr**: $6-10/mes (económico)
- **Hetzner**: €4-8/mes (Europa)
- **Railway**: $15-25/mes (serverless)

---

## ✅ Checklist Pre-Deploy

- [ ] `.env` configurado
- [ ] `DJANGO_SECRET_KEY` generado
- [ ] `DEBUG=False`
- [ ] Dominio configurado (opcional)
- [ ] SSL configurado (recomendado)

---

**¡Listo para desplegar! 🚀**

