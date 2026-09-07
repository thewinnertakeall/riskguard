# RiskGuard Architecture

## Architectural Style

RiskGuard follows a modular architecture inspired by:

- Clean Architecture
- Hexagonal Architecture
- Domain-Driven Design
- Object-Oriented Design
- SOLID principles

## Layers

### Domain

Contains:

- Entities
- Value Objects
- Domain Events
- Ports / Interfaces
- Business rules

### Application

Contains:

- DTOs
- Use Cases
- Application Services
- Strategies

### Infrastructure

Contains:

- SQL repositories
- RDF adapters
- Event bus
- Database implementations

### Presentation

Contains:

- Controllers
- API routes
- Request/response schemas

### Agents

Contains:

- Abstract Agent
- Risk Analysis Agent
- Control Analysis Agent
- Incident Analysis Agent
- Recommendation Agent
- Coordinator
- Factory

### Frontend

React + Vite dashboard.

## Main Flow

User
  |
  v
React Dashboard
  |
  v
FastAPI
  |
  v
Controller
  |
  v
DTO
  |
  v
Use Case
  |
  v
Application Service
  |
  +----------------------+
  |                      |
  v                      v
Repository          Semantic Adapter
  |                      |
  v                      v
SQLite               RDF / OWL
                         |
                         v
                       SPARQL
                         |
                         v
                     Reasoning
                         |
                         v
                    Multi-Agent
                         |
                         v
                  Recommendation
                         |
                         v
                    Dashboard

## Design Patterns

- Repository Pattern
- Factory Pattern
- Strategy Pattern
- Adapter Pattern
- Dependency Injection
- Event-driven design
- DTO Pattern

## Important Principle

The domain must not depend directly on:

- FastAPI
- SQLAlchemy
- SQLite
- RDFLib
- React
- RabbitMQ

Infrastructure depends on domain interfaces.

This keeps the system replaceable and extensible.
