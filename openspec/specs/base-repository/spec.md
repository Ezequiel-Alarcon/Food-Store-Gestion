## ADDED Requirements

### Requirement: Provide a generic BaseRepository
The system MUST provide a generic BaseRepository[T] to centralize common persistence operations for SQLModel entities.

#### Scenario: Fetch entity by id
- **WHEN** a service requests an entity by its identifier through BaseRepository
- **THEN** the repository MUST return the matching entity or null/none if it does not exist

#### Scenario: Persist new entity
- **WHEN** a service creates a new entity through BaseRepository
- **THEN** the repository MUST add it to the current session and make it available for commit by the Unit of Work

### Requirement: Allow extension per module
The system MUST allow feature modules to extend BaseRepository with entity-specific queries without changing the base contract.

#### Scenario: Custom query added by module repository
- **WHEN** a module defines a repository that inherits from BaseRepository
- **THEN** it MUST be able to add custom query methods while still using the same Unit of Work session
