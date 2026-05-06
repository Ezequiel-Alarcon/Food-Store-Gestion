## ADDED Requirements

### Requirement: Alembic configurado con alembic.ini
El proyecto debe tener Alembic configurado para migraciones versionadas.

#### Scenario: Alembic inicializado
- **WHEN** se ejecuta alembic init migrations
- **THEN** crea alembic.ini y estructura migrations/

#### Scenario: Generar migración
- **WHEN** se ejecuta alembic revision --autogenerate -m "initial"
- **THEN** crea archivo en migrations/versions/ con Upgrade/Downgrade

### Requirement: Migraciones pueden aplicar todos los modelos
Las migraciones deben incluir todas las tablas definidas en los modelos SQLModel.

#### Scenario: Aplicar migraciones
- **WHEN** se ejecuta alembic upgrade head
- **THEN** crea todas las tablas en PostgreSQL

#### Scenario: Revertir migración
- **WHEN** se ejecuta alembic downgrade -1
- **THEN** revierte la última migración aplicada

### Requirement: Importación de modelos en env.py
Alembic debe poder importar todos los modelos para detectar cambios.

#### Scenario: Importar modelos
- **WHEN** alembic env.py se ejecuta
- **THEN** puede importar todos los modelos de backend.app.modules.*