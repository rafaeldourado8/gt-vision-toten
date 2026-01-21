# 🎨 PROMPT PARA FRONTEND - GT-Vision Toten

## 📋 Visão Geral

Crie um **sistema web/mobile responsivo** para monitoramento de presença escolar com reconhecimento facial.

**Stack Tecnológica:**
- React 18 + TypeScript
- TailwindCSS (design minimalista corporativo)
- React Query (data fetching)
- Zustand (state management)
- React Router (navegação)
- Axios (HTTP client)
- Socket.io-client (WebSocket)

---

## 🎨 Design System

### Paleta de Cores (Neutras e Corporativas)
```css
/* Cores Principais */
--primary: #2563EB      /* Azul corporativo */
--secondary: #64748B    /* Cinza azulado */
--accent: #10B981       /* Verde sucesso */
--danger: #EF4444       /* Vermelho alerta */
--warning: #F59E0B      /* Amarelo aviso */

/* Neutros */
--gray-50: #F9FAFB
--gray-100: #F3F4F6
--gray-200: #E5E7EB
--gray-300: #D1D5DB
--gray-500: #6B7280
--gray-700: #374151
--gray-900: #111827

/* Backgrounds */
--bg-primary: #FFFFFF
--bg-secondary: #F9FAFB
--bg-dark: #111827
```

### Tipografia
```css
/* Fontes */
font-family: 'Inter', sans-serif;

/* Tamanhos */
--text-xs: 0.75rem
--text-sm: 0.875rem
--text-base: 1rem
--text-lg: 1.125rem
--text-xl: 1.25rem
--text-2xl: 1.5rem
--text-3xl: 1.875rem
```

### Componentes Base
- Botões: arredondados (rounded-lg), sombra sutil
- Cards: fundo branco, borda cinza clara, sombra suave
- Inputs: borda cinza, focus azul, altura 40px
- Tabelas: zebrada, hover cinza claro
- Modais: overlay escuro 50%, card centralizado

---

## 📱 Páginas e Funcionalidades

### 1. 🔐 Login Page (`/login`)

**Layout:**
- Tela dividida: 50% imagem/logo, 50% formulário
- Centralizado vertical e horizontalmente
- Logo "GT-Vision Toten" no topo
- Formulário minimalista

**Campos:**
- Email (input com ícone)
- Senha (input com toggle show/hide)
- Checkbox "Lembrar-me"
- Botão "Entrar" (azul, largura total)
- Link "Esqueci minha senha"

**Validações:**
- Email válido
- Senha mínimo 6 caracteres
- Mensagens de erro em vermelho

**API:**
```
POST /auth/login
Body: { email, password }
Response: { access_token, user }
```

---

### 2. 📊 Dashboard (`/dashboard`)

**Layout:**
- Sidebar esquerda (fixa)
- Header superior (nome usuário, notificações, logout)
- Conteúdo principal (grid responsivo)

**Cards de Estatísticas (4 cards no topo):**
1. Total de Alunos (ícone 👥)
2. Câmeras Online (ícone 📹)
3. Presentes Hoje (ícone ✅)
4. Ausentes Hoje (ícone ❌)

**Gráfico de Presença:**
- Gráfico de linhas (últimos 7 dias)
- Legenda: Presentes, Atrasados, Ausentes
- Cores: verde, amarelo, vermelho

**Últimas Detecções (tabela):**
- Foto do aluno (thumbnail)
- Nome
- Horário
- Câmera
- Status (badge colorido)

**API:**
```
GET /dashboard/stats
GET /dashboard/attendance-chart
```

---

### 3. 📹 Câmeras (`/cameras`)

**Layout:**
- Grid de cards (3 colunas desktop, 1 mobile)
- Botão "Adicionar Câmera" (canto superior direito)

**Card de Câmera:**
- Preview do stream (HLS player)
- Nome da câmera
- Localização
- Status (badge: ONLINE verde, OFFLINE cinza)
- Botões: Ver Stream, Editar, Excluir

**Modal Adicionar Câmera:**
- Nome (input)
- URL RTSP ou Webcam (input com helper text)
- Localização (input)
- Botões: Cancelar, Salvar

**Stream Player:**
- Player HLS fullscreen
- Controles: play/pause, volume, fullscreen
- Overlay com detecções em tempo real (bounding boxes)

**API:**
```
GET /cameras
POST /cameras
DELETE /cameras/{id}
GET /cameras/{id}/stream
```

---

### 4. 🎓 Alunos (`/students`)

**Layout:**
- Barra de busca (topo)
- Filtros: Turma, Status (ativo/inativo)
- Botões: Adicionar Aluno, Importar Excel
- Tabela de alunos

**Tabela:**
- Foto (thumbnail circular)
- Nome
- Turma
- Status Face (✅ com foto, ❌ sem foto)
- Ações: Ver, Editar, Upload Foto, Excluir

**Modal Adicionar Aluno:**
- Nome (input)
- Série (select)
- Turma (input)
- Botões: Cancelar, Salvar

**Modal Upload Foto:**
- Drag & drop ou click para upload
- Preview da foto
- Crop tool (opcional)
- Botão "Processar Face" (extrai encoding)
- Feedback: "Face detectada com sucesso!"

**Importar Excel:**
- Upload de arquivo
- Preview dos dados (tabela)
- Validação de erros
- Botão "Importar X alunos"

**API:**
```
GET /students
POST /students
PUT /students/{id}/photo
DELETE /students/{id}
POST /students/import
```

---

### 5. ✅ Presença (`/attendance`)

**Layout:**
- Filtros: Data, Turma, Status
- Botão "Exportar Excel"
- Cards de resumo (presente, ausente, atrasado)
- Tabela de registros

**Tabela:**
- Foto do aluno
- Nome
- Turma
- Horário
- Status (badge colorido)
- Confiança (barra de progresso)
- Câmera

**Filtros:**
- Date picker (data única ou range)
- Select de turma
- Select de status

**Exportar:**
- Gera Excel com filtros aplicados
- Download automático

**API:**
```
GET /attendance/report/{date}
GET /attendance/student/{id}
GET /attendance/export/{date}
```

---

### 6. 📈 Relatórios (`/reports`)

**Layout:**
- Tabs: Diário, Semanal, Mensal, Personalizado
- Filtros por turma
- Gráficos e tabelas

**Gráficos:**
1. Taxa de presença por turma (barras)
2. Evolução semanal (linhas)
3. Horários de pico (heatmap)

**Tabela Resumo:**
- Turma
- Total alunos
- % Presença
- % Atrasos
- % Faltas

**API:**
```
GET /reports/daily
GET /reports/weekly
GET /reports/monthly
```

---

### 7. 🔔 Notificações (`/notifications`)

**Layout:**
- Lista de notificações (mais recentes primeiro)
- Badge de não lidas no ícone do header

**Card de Notificação:**
- Ícone (tipo de notificação)
- Título
- Mensagem
- Timestamp (relativo: "há 5 minutos")
- Indicador de lida/não lida

**Tipos:**
- Presença registrada (verde)
- Aluno ausente (vermelho)
- Câmera offline (amarelo)
- Sistema (azul)

**API:**
```
GET /notifications
PUT /notifications/{id}/read
```

---

### 8. ⚙️ Configurações (`/settings`)

**Tabs:**
1. Perfil (nome, email, senha)
2. Sistema (horário de aula, tolerância atraso)
3. Notificações (preferências)
4. Usuários (admin only)

---

## 🎯 Componentes Reutilizáveis

### Button
```tsx
<Button variant="primary|secondary|danger" size="sm|md|lg">
  Texto
</Button>
```

### Card
```tsx
<Card title="Título" subtitle="Subtítulo">
  Conteúdo
</Card>
```

### Table
```tsx
<Table
  columns={[...]}
  data={[...]}
  onRowClick={...}
/>
```

### Modal
```tsx
<Modal isOpen={...} onClose={...} title="Título">
  Conteúdo
</Modal>
```

### Badge
```tsx
<Badge variant="success|warning|danger|info">
  Texto
</Badge>
```

### Avatar
```tsx
<Avatar src="..." name="João Silva" size="sm|md|lg" />
```

---

## 📱 Responsividade

### Breakpoints
```css
sm: 640px   /* Mobile */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large Desktop */
```

### Mobile
- Sidebar vira menu hamburguer
- Grid de 1 coluna
- Cards empilhados
- Tabelas com scroll horizontal
- Botões flutuantes (FAB)

---

## 🔄 Estados e Loading

### Loading States
- Skeleton screens (não spinners)
- Shimmer effect em cards
- Progress bar no topo da página

### Empty States
- Ilustração + mensagem
- Botão de ação primária
- Exemplo: "Nenhum aluno cadastrado. Adicione o primeiro!"

### Error States
- Mensagem clara
- Botão "Tentar novamente"
- Ícone de erro

---

## 🌐 WebSocket (Tempo Real)

**Eventos:**
```javascript
socket.on('face.detected', (data) => {
  // Atualizar dashboard em tempo real
  // Mostrar notificação toast
})

socket.on('camera.status', (data) => {
  // Atualizar status da câmera
})

socket.on('attendance.registered', (data) => {
  // Atualizar lista de presença
  // Tocar som de confirmação
})
```

---

## 🎬 Animações

- Transições suaves (300ms)
- Fade in ao carregar
- Slide in para modais
- Hover effects sutis
- Loading skeletons

---

## 📦 Estrutura de Pastas

```
src/
├── components/
│   ├── common/        # Button, Card, Modal, etc
│   ├── layout/        # Sidebar, Header, Footer
│   └── features/      # Componentes específicos
├── pages/
│   ├── Login/
│   ├── Dashboard/
│   ├── Cameras/
│   ├── Students/
│   ├── Attendance/
│   └── Reports/
├── hooks/             # Custom hooks
├── services/          # API calls
├── stores/            # Zustand stores
├── types/             # TypeScript types
├── utils/             # Helpers
└── styles/            # Global CSS
```

---

## 🔒 Autenticação

- JWT token no localStorage
- Axios interceptor para adicionar token
- Redirect para /login se 401
- Protected routes (HOC)

---

## ✅ Checklist de Implementação

- [ ] Setup projeto (Vite + React + TS)
- [ ] Configurar TailwindCSS
- [ ] Criar componentes base
- [ ] Implementar autenticação
- [ ] Página de login
- [ ] Dashboard
- [ ] Gerenciamento de câmeras
- [ ] Gerenciamento de alunos
- [ ] Registro de presença
- [ ] Relatórios
- [ ] Notificações
- [ ] WebSocket tempo real
- [ ] Responsividade mobile
- [ ] Testes (opcional)

---

**API Base URL**: `http://localhost:8000`  
**Documentação API**: Ver `docs/API-ENDPOINTS.md`

**Design**: Minimalista, corporativo, cores neutras, profissional, clean, moderno.
