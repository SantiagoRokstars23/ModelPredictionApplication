"""Motor (Engine) de SQLAlchemy -- única forma oficial de conectar con PostgreSQL.

Ver docs/33-Modelo-Fisico-PostgreSQL.md; docs/35-Arquitectura-Oficial-del-Proyecto-Python.md,
seccion 4 (app/persistence: "ejecutar consultas y escrituras contra PostgreSQL...
nunca ejecuta lógica matemática o de negocio").

BUILD-003: únicamente la creación y configuración del Engine -- ninguna
consulta, ningún repositorio específico (ver repositories/).
"""

from sqlalchemy import Engine, create_engine

from app.config.settings import DATABASE_URL

_engine: Engine | None = None


def get_engine() -> Engine:
    """Devuelve el único Engine de la aplicación, creándolo la primera vez.

    Única función de todo el proyecto autorizada a instanciar un Engine de
    SQLAlchemy (validación obligatoria de BUILD-003: "Engine único"). La
    creación es perezosa (lazy) -- no se ejecuta al importar este módulo,
    para que el paquete pueda importarse (ej. en pruebas que no requieren
    base de datos) incluso sin `DATABASE_URL` configurada todavía.

    La configuración del Engine queda aislada aquí (`pool_pre_ping`, `echo`)
    -- ningún otro módulo decide estos parámetros, conforme a "aislamiento de
    configuración" (brief de BUILD-003, sección database.py).
    """
    global _engine
    if _engine is None:
        if not DATABASE_URL:
            raise RuntimeError(
                "DATABASE_URL no está configurada. Ver .env.example (BUILD-001) "
                "y app/config/settings.py."
            )
        _engine = create_engine(
            DATABASE_URL,
            # Evita errores por conexiones inactivas reaprovechadas del pool
            # -- valor por defecto ampliamente recomendado, no una decisión
            # de negocio.
            pool_pre_ping=True,
            # Sin eco de SQL por defecto. El tamaño del pool y otras
            # afinaciones de rendimiento se dejan para una misión futura,
            # cuando exista evidencia real de carga (no hay hoy ninguna,
            # `data/results/` sigue vacío) -- no se inventa un valor sin
            # justificación (`CLAUDE.md`).
            echo=False,
            future=True,
        )
    return _engine
