# React Frontend Setup Guide

## Installation & Running

### Prerequisites
- Node.js 16+ installed
- Backend running on http://localhost:8000

### Quick Start

1. **Navigate to frontend directory:**
   ```bash
   cd frontend-react
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```
   
   This installs:
   - `react` & `react-dom` - UI library
   - `vite` - Build tool
   - `@vitejs/plugin-react` - Vite React plugin

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Browser opens automatically** to `http://localhost:3000`

## What's New Compared to Streamlit

### Advantages
✅ **Faster performance** - Vite provides near-instant HMR (hot reload)
✅ **Better UX** - Smooth animations and instant feedback
✅ **Visual tree layout** - Expandable tree with node hierarchy
✅ **Single Page App** - No full page reloads
✅ **Better styling** - Complete CSS control with flexbox
✅ **Smaller bundle** - Efficient React+Vite build
✅ **Modern stack** - Industry standard React + Vite setup

### Features Preserved
✔️ View conversation tree
✔️ View node prompts and responses
✔️ Branch from any node
✔️ Clear individual branches
✔️ Clear entire tree
✔️ Refresh tree data
✔️ Error handling

## Project Components

### App.jsx (Main)
- Manages global state (tree, selectedNodeId, message)
- Handles all API calls (fetch, send, delete)
- Routes between TreeDisplay and NodePanel

### TreeDisplay.jsx
- Renders tree structure recursively
- Uses TreeNode components

### TreeNode.jsx
- Individual node with expand/collapse
- Shows node preview and ID
- Clickable to select node

### NodePanel.jsx
- Shows full prompt and response
- Message input for branching
- Clear branch and clear tree buttons

### CSS Organization
```
src/
├── styles.css           (Global: app layout, colors, fonts)
├── styles/
│   ├── TreeNode.css    (Tree sidebar styling)
│   └── NodePanel.css   (Main panel styling)
```

## Configuration

### Change Backend URL
Edit `src/App.jsx` line 8:
```javascript
const BACKEND_URL = "http://your-backend-url";
```

### Customize Colors
Edit `src/styles.css`:
```css
/* Primary blue */
--primary: #5f9ed6;
/* Accent orange */
--accent: #ff6f61;
```

## Building for Production

```bash
npm run build
```

Creates optimized files in `dist/` folder ready for deployment.

## Deployment Options

### Static Hosting (Netlify, Vercel, GitHub Pages)
1. Run `npm run build`
2. Deploy `dist/` folder
3. Configure backend URL in environment

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Can't connect to backend | Check backend URL in App.jsx, ensure backend is running |
| Styles not loading | Clear cache (Ctrl+Shift+Delete), restart dev server |
| White screen | Check browser console for errors, ensure Node.js version 16+ |
| Hot reload not working | Restart `npm run dev` |
| Port 3000 already in use | Change port in vite.config.js: `port: 3001` |

## Development Tips

- **DevTools**: Open Chrome DevTools (F12) to inspect React components
- **React DevTools**: Install React DevTools browser extension
- **Network Tab**: Check API calls in Network tab for debugging
- **Auto-reload**: Changes to `.jsx` and `.css` files reload automatically

## Next Steps

1. ✅ Install dependencies: `npm install`
2. ✅ Start dev server: `npm run dev`
3. ✅ Open browser: http://localhost:3000
4. ✅ Test tree functionality
5. ✅ Build for production: `npm run build`

Enjoy the new React frontend! 🚀
