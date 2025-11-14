from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AssistantKnowledgeArticle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=140)),
                ("resumen", models.TextField(help_text="Resumen breve que se mostrará en la tarjeta")),
                ("contenido", models.TextField(help_text="Detalle completo del procedimiento o política")),
                (
                    "tags",
                    models.CharField(
                        blank=True,
                        help_text="Lista de etiquetas separadas por coma para facilitar la búsqueda",
                        max_length=200,
                    ),
                ),
                ("destacado", models.BooleanField(default=False)),
                ("actualizado", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-destacado", "titulo"],
                "verbose_name": "Artículo de conocimiento",
                "verbose_name_plural": "Artículos de conocimiento",
            },
        ),
        migrations.CreateModel(
            name="AssistantPlaybook",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=120)),
                ("descripcion", models.TextField()),
                (
                    "pasos",
                    models.JSONField(
                        default=list,
                        help_text="Lista ordenada de pasos con titulo y descripcion",
                    ),
                ),
                (
                    "es_template",
                    models.BooleanField(
                        default=True,
                        help_text="Marca si el playbook aparece en la sección de flujos recomendados",
                    ),
                ),
                ("actualizado", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["titulo"],
                "verbose_name": "Playbook del asistente",
                "verbose_name_plural": "Playbooks del asistente",
            },
        ),
        migrations.CreateModel(
            name="AssistantQuickReply",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=80)),
                (
                    "prompt",
                    models.TextField(
                        help_text="Instrucción que se enviará a ISAC cuando el usuario pulse la tarjeta",
                    ),
                ),
                (
                    "categoria",
                    models.CharField(
                        choices=[
                            ("inventario", "Inventario"),
                            ("ventas", "Ventas"),
                            ("soporte", "Soporte"),
                            ("finanzas", "Finanzas"),
                            ("general", "General"),
                        ],
                        default="general",
                        max_length=20,
                    ),
                ),
                ("orden", models.PositiveIntegerField(default=0)),
                ("activo", models.BooleanField(default=True)),
                ("creado", models.DateTimeField(auto_now_add=True)),
                ("actualizado", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["categoria", "orden", "titulo"],
                "verbose_name": "Respuesta rápida",
                "verbose_name_plural": "Respuestas rápidas",
            },
        ),
    ]
