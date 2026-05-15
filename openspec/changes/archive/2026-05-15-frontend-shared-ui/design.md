## Context

El proyecto Food Store usa Tailwind CSS pero no tiene una biblioteca de componentes reutilizables. Cada开发者 implementa sus propios patrones, causando inconsistencias. La Fase 4 necesita una base sólida para implementar HomePage y ProfilePage.

## Goals / Non-Goals

**Goals:**
- Crear 4 componentes UI base: Button, Input, Modal, Card
- Implementar sistema de variantes consistente (colores, sizes, estados)
- Asegurar accesibilidad (ARIA, keyboard navigation, focus management)
- Proveer tipado TypeScript strict
- Usar solo Tailwind CSS (sin nuevas dependencias)

**Non-Goals:**
- No incluir lógica de negocio en componentes
- No crear sistema de theming completo (colores hardcoded al brand actual)
- No implementar Storybook o documentación interactiva
- No crear variantes de tamaño para móviles (responsive handled per caso)

## Decisions

### D1: Composición vs Inheritance
**Elegido:** Composición (props children + slots)  
**Alternativa:** Slot objects (complicated, overkill para este scope)  
**Rationale:** React standard, más intuitivo, menos código

### D2: Estilos con Tailwind vs CSS-in-JS
**Elegido:** Tailwind CSS classes  
**Alternativa:** Styled-components, CSS modules  
**Rationale:** Ya disponible en el proyecto, consistent con el resto del codebase

### D3: Tipado de props
**Elegido:** TypeScript interfaces exportadas  
**Alternativa:** Zod schemas  
**Rationale:** Más simple, no necesitamos validación runtime, el proyecto ya usa TypeScript

### D4: Modal implementation
**Elegido:** Portal + useEffect para escape/click-outside  
**Alternativa:** Native dialog element (partial support)  
**Rationale:** Más control sobre animaciones y cross-browser consistency

## Risks / Trade-offs

- **[R1]** Diferentes developers pueden preferir patrones distintos → Mitigación: Documentar convenciones en cada componente
- **[R2]** Componentes muy genéricos pueden complicarse → Mitigación: Mantener API simple, máximo 8-10 props por componente
- **[R3]** Sin Storybook, testing visual manual → Mitigación: Props bien tipados permiten testing unitario básico
- **[T]** No habrá documentación visual interactive hasta hacer Storybook en future → Aceptado, no es prioritario ahora