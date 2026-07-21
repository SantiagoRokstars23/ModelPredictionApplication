"""Paquete config -- configuracion transversal del proyecto.

Responsabilidad (docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 4):
centralizar configuracion (cadena de conexion, version del modelo). Nunca
contiene logica de negocio ni de calculo.

Bootstrap oficial (BUILD-001): unicamente lectura de variables de entorno
(seccion 6 del brief: "Preparar unicamente: conexion por variables de
entorno. No crear tablas. No ejecutar migraciones."). Ver settings.py.
"""
