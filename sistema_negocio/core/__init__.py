"""Configuración base del paquete core."""

import pymysql

pymysql.install_as_MySQLdb()

__all__ = ["pymysql"]

