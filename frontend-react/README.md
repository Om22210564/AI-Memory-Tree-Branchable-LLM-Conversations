# AI Memory Tree Chat - React + Vite Frontend

This is the React + Vite frontend for the AI Memory Tree Chat application. It provides an interactive tree visualization of conversation nodes with full branching and management capabilities.

## Tech Stack

- **React 18**: Modern UI library with hooks
- **Vite**: Ultra-fast build tool and development server
- **CSS Flexbox**: Flexible layouts and styling
- **Axios**: HTTP client (optional, uses fetch by default)

## Features

✨ **Core Features:**
- Interactive tree visualization with expand/collapse
- View node prompts and LLM responses
- Create new branches from any node
- Clear individual branches
- Clear entire tree with confirmation
- Real-time tree updates
- Responsive dark theme UI

## Project Structure

```
frontend-react/
├── index.html              # Entry point
├── package.json           # Dependencies
├── vite.config.js         # Vite configuration
├── src/
│   ├── main.jsx           # React app entry
│   ├── App.jsx            # Main app component
│   ├── styles.css         # Global styles
│   ├── components/
│   │   ├── TreeNode.jsx   # Individual tree node
│   │   ├── TreeDisplay.jsx # Tree container
│   │   └── NodePanel.jsx  # Node details & actions
│   └── styles/
│       ├── TreeNode.css   # Tree node styling
│       └── NodePanel.css  # Panel styling
└── .gitignore
```

## Getting Started

### 1. Install Dependencies

```bash
cd frontend-react
npm install
```

### 2. Configure Backend URL

Edit `src/App.jsx` if your backend is on a different host:

```javascript
const BACKEND_URL = "http://localhost:8000"; // Change if needed
```

### 3. Start Development Server

```bash
npm run dev
```

The app will open at `http://localhost:3000` automatically.

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## API Integration

The frontend communicates with the FastAPI backend at:

- `GET /tree` - Fetch entire conversation tree
- `POST /chat` - Send message and create new node
- `DELETE /clear/{node_id}` - Delete branch from node
- `DELETE /clear` - Clear entire tree

## Backend CORS

The backend already has CORS enabled to accept requests from any origin. If you deploy to a different domain, ensure CORS is properly configured.

## Styling

The app uses a modern dark theme with:
- Primary color: `#5f9ed6` (Blue)
- Accent color: `#ff6f61` (Orange/Red)
- Background: `#0a0e27` (Deep Blue)
- Sidebar: `#1a1f3a` (Dark Blue)

All colors can be customized in `src/styles.css` and component-specific CSS files.

## Browser Support

Works on all modern browsers (Chrome, Firefox, Safari, Edge) with ES2020+ support.

## Development Notes

- Hot Module Replacement (HMR) is enabled by default in dev mode
- The API proxy is configured in `vite.config.js` for `/api/*` routes
- Tree state is fetched on app load and after mutations
- Selected node persists during the session

## Building for Production

```bash
npm run build
npm run preview
```

The `dist/` folder contains the production-ready files for deployment.

## Troubleshooting

**Backend not connecting?**
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify API_KEY in backend is valid

**Styles not loading?**
- Clear browser cache (Ctrl+Shift+Delete)
- Check that CSS files exist in `src/styles/`

**App not updating after mutations?**
- Check network tab in DevTools
- Verify backend responses are successful (200 OK)
- Try clicking "Refresh Tree" button
