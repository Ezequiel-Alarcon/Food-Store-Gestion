# Shared UI Components - Specification Notes

Los 4 componentes (Button, Input, Modal, Card) son componentes UI fundamentales que no requieren especificación formal detallada más allá de:

- **Proposal**: Define qué componentes y sus capacidades
- **Design**: Define decisiones técnicas y estructura

Cada componente se implementa con:
- Props interfaces en TypeScript
- Variantes via Tailwind classes
- Estados (loading, disabled, error) 
- Accesibilidad básica (aria attributes, focus management)

No se necesitan specs adicionales para estos componentes baseline.