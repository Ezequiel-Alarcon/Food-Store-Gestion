# frontend-setup

## Descripción

Configuración base del proyecto frontend de Food Store: React + Vite + TypeScript + Tailwind +工具.

## Comportamiento Esperado

- El proyecto compila sin errores TypeScript con strict:true
- `npm run dev` levanta el servidor en http://localhost:5173
- `npm run build` genera el bundle de producción

## Dependencias Requeridas

```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.x.x",
    "@tanstack/react-query": "^5.x.x",
    "@tanstack/react-form": "^0.x.x",
    "zustand": "^4.x.x",
    "axios": "^1.x.x",
    "recharts": "^2.x.x",
    "tailwindcss": "^3.x.x",
    "@mercadopago/sdk-js": "^0.0.x"
  },
  "devDependencies": {
    "typescript": "^5.x.x",
    "vite": "^5.x.x",
    "@types/react": "^18.x.x",
    "@types/react-dom": "^18.x.x",
    "autoprefixer": "^10.x.x",
    "postcss": "^8.x.x"
  }
}
```

## Configuraciones

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### vite.config.ts

Debe incluir:
- Plugin react() con @vitejs/plugin-react
- Proxy hacia backend en http://localhost:8000

### Variables de Entorno Requeridas

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_MERCADOPAGO_PUBLIC_KEY=TEST-xxxxx
```

## Criterios de Éxito

- [ ] npm install corre sin errores
- [ ] npm run dev inicia en puerto 5173
- [ ] No hay errores TypeScript con strict
- [ ] build genera archivos en dist/