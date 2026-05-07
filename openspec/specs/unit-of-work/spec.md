## ADDED Requirements

### Requirement: Transaction boundary via Unit of Work
The system MUST provide a Unit of Work abstraction that defines a transaction boundary for a use case execution, ensuring atomic commit or rollback.

#### Scenario: Commit on successful execution
- **WHEN** a service completes its use case within a Unit of Work without raising exceptions
- **THEN** the Unit of Work MUST commit the transaction exactly once

#### Scenario: Rollback on error
- **WHEN** an exception occurs during a use case within a Unit of Work
- **THEN** the Unit of Work MUST rollback the transaction and MUST NOT commit

### Requirement: Session exposure for repositories
The system MUST allow repositories to access the database session associated with the active Unit of Work.

#### Scenario: Repository uses active session
- **WHEN** a repository is instantiated within an active Unit of Work
- **THEN** the repository MUST receive the session from that Unit of Work
