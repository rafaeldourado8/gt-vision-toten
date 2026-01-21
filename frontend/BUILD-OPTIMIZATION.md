# Frontend - GT-Vision Toten

## 🚀 Otimizações de Build

### Docker Build Cache
- Usa `corepack` nativo do Node 20 (mais rápido que npm install -g pnpm)
- Cache mount para pnpm store (reutiliza downloads entre builds)
- Multi-stage build (imagem final apenas com nginx + arquivos estáticos)

### Vite Optimizations
- Code splitting automático (vendor, ui chunks)
- Tree shaking de dependências não utilizadas
- Minificação com esbuild (mais rápido que terser)

### Tamanho Final
- Imagem Docker: ~50MB (nginx:alpine + dist)
- Bundle JS: ~285KB (gzipped: ~92KB)
- Bundle CSS: ~21KB (gzipped: ~4.5KB)

## 📦 Build Local

```bash
# Desenvolvimento
pnpm dev

# Build de produção
pnpm build

# Preview do build
pnpm preview
```

## 🐳 Build Docker

```bash
# Build otimizado com cache
docker build -t gt-vision-frontend .

# Build sem cache (limpo)
docker build --no-cache -t gt-vision-frontend .
```

## 🔧 Melhorias Futuras

- [ ] Lazy loading de rotas
- [ ] Service Worker para cache offline
- [ ] Compressão Brotli no nginx
- [ ] CDN para assets estáticos
