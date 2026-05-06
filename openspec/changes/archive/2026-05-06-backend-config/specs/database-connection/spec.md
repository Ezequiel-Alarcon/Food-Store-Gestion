## ADDED Requirements

### Requirement: Conexión a PostgreSQL mediante SQLModel
La aplicación debe establecer conexión a PostgreSQL usando SQLModel con pool de conexiones.

#### Scenario: Conexión exitosa
- **WHEN** aplicación inicia con DATABASE_URL válida
- **THEN** engine se crea sin errores y permite queries

#### Scenario: Conexión fallida
- **WHEN** DATABASE_URL es inválida o PostgreSQL no está disponible
- **THEN** excepción de conexión con mensaje descriptivo

### Requirement: Session factory para UoW
La aplicación debe proporcionar una sesión de base de datos inyectable en el patrón Unit of Work.

#### Scenario: Crear sesión
- **WHEN** código llama a SessionLocal()
- **THEN** retorna una sesión activa lista para operaciones

#### Scenario: Cerrar sesión
- **WHEN** sesión se cierra con close()
- **THEN** conexión retorna al pool

### Requirement: Settings con pydantic-settings
La configuración debe cargarse desde variables de entorno con tipado.

#### Scenario: Cargar setting existente
- **WHEN** código accede a Settings().DATABASE_URL
- **THEN** retorna el valor del .env

#### Scenario: Setting no existe
- **WHEN** código accede a Setting inexistente
- **THEN** Pydantic lanza error de validación al iniciar