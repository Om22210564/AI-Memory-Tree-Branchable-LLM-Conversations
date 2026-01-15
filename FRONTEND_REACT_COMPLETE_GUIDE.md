# React + Vite Frontend - Complete Setup Guide

## 📋 Summary

Your Streamlit frontend has been **fully converted to a modern React + Vite application** with all previous functionality preserved and enhanced with better UX.

## 📁 What Was Created

```
frontend-react/
├── package.json              # Dependencies & scripts
├── vite.config.js           # Vite configuration with proxy
├── index.html               # HTML entry point
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
│
├── src/
│   ├── main.jsx            # React app initialization
│   ├── App.jsx             # Main app component (all logic)
│   ├── styles.css          # Global styling (dark theme)
│   │
│   ├── components/
│   │   ├── TreeNode.jsx    # Tree node with expand/collapse
│   │   ├── TreeDisplay.jsx # Tree container component
│   │   └── NodePanel.jsx   # Node details & actions
│   │
│   └── styles/
│       ├── TreeNode.css    # Tree styling
│       └── NodePanel.css   # Panel styling
```

## 🚀 Quick Start (3 Steps)

### 1. Open Terminal & Navigate
```bash
cd c:\Users\omkar\OneDrive\Desktop\DesignP\Tree\frontend-react
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm run dev
```

Browser will auto-open at **http://localhost:3000**

## ⚙️ Configuration

### Backend URL
If your backend runs on a different port/host, edit `src/App.jsx`:

```javascript
const BACKEND_URL = "http://localhost:8000"; // Change this if needed
```

### Port Number
To use a different port (e.g., 3001), edit `vite.config.js`:

```javascript
server: {
  port: 3001,  // Change this
}
```

## ✨ Features (All from Streamlit + Enhanced)

| Feature | Streamlit | React | Status |
|---------|-----------|-------|--------|
| View tree | ✅ | ✅ | Enhanced with visual hierarchy |
| Expand/collapse | ❌ | ✅ | NEW: Better UX |
| View node details | ✅ | ✅ | Improved styling |
| Branch from node | ✅ | ✅ | Faster feedback |
| Clear branch | ✅ | ✅ | Confirmation dialog |
| Clear tree | ✅ | ✅ | Confirmation dialog |
| Refresh tree | ✅ | ✅ | Same functionality |
| Error handling | ✅ | ✅ | Better messages |

## 🎨 Design

### Color Scheme
- **Background**: `#0a0e27` (Deep blue)
- **Sidebar**: `#1a1f3a` (Dark blue)
- **Primary**: `#5f9ed6` (Blue)
- **Accent**: `#ff6f61` (Orange/red)

### Responsive
- Flexbox layouts
- Mobile-friendly sidebar
- Auto-expanding main content
- Smooth animations

## 📦 Dependencies

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.0"
}
```

These are automatically installed with `npm install`.

## 🔄 API Integration

The app calls these backend endpoints:

```
GET    /tree              → Fetch tree structure
POST   /chat              → Create new node (with parent_id & message)
DELETE /clear/{node_id}   → Delete branch
DELETE /clear             → Delete entire tree
```

Backend already has CORS enabled, no additional config needed.

## 🛠️ Development Commands

```bash
npm run dev      # Start dev server (hot reload enabled)
npm run build    # Build for production
npm run preview  # Preview production build locally
```

## 📱 Project Structure

```
App.jsx (Main logic)
├── Manages global state
├── Handles all API calls
└── Passes props to child components

├── TreeDisplay.jsx (Sidebar)
│   └── TreeNode.jsx (Recursive tree)
│
└── NodePanel.jsx (Main content)
    ├── Shows node details
    ├── Message input
    └── Action buttons
```

## 🐛 Troubleshooting

**Problem**: "Cannot connect to backend"
- Check backend is running: `python backend/main.py`
- Verify URL in App.jsx matches your backend
- Check browser console (F12) for errors

**Problem**: "Styles look wrong"
- Clear cache: Ctrl+Shift+Delete
- Restart dev server: Stop and `npm run dev`

**Problem**: "Hot reload not working"
- Restart dev server
- Check no other app uses port 3000

**Problem**: "npm install fails"
- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again
- Try `npm cache clean --force`

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `package.json` | Dependencies and npm scripts |
| `vite.config.js` | Vite server config and build settings |
| `index.html` | HTML template with div#root |
| `src/main.jsx` | React app entry point |
| `src/App.jsx` | Main component with all logic |
| `src/styles.css` | Global styling (layout, colors, fonts) |
| `src/components/*.jsx` | React components (Tree, Panel) |
| `src/styles/*.css` | Component-specific styling |

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

Creates `dist/` folder with optimized files.

### Deploy Anywhere
- **Netlify**: Drag & drop `dist/` folder
- **Vercel**: Connect Git repo
- **GitHub Pages**: Run build, push `dist/` to gh-pages
- **Any web server**: Serve `dist/` files as static content

## 📖 Next Steps

1. ✅ Extract the `frontend-react` folder from this directory
2. ✅ Run `npm install`
3. ✅ Ensure backend is running
4. ✅ Run `npm run dev`
5. ✅ Test all functionality
6. ✅ Build for production when ready: `npm run build`

## 💡 Tips

- **Hot reload**: Any `.jsx` or `.css` change auto-refreshes (no manual reload needed)
- **DevTools**: Press F12 and install React DevTools extension for better debugging
- **Network tab**: Check API calls in DevTools → Network tab
- **Console**: Check DevTools → Console for JavaScript errors

## 📞 Support

If you encounter issues:
1. Check browser console (F12)
2. Verify backend is running
3. Check backend logs for errors
4. Ensure Node.js version is 16+: `node --version`

---

**Created**: January 15, 2026
**Framework**: React 18 + Vite 5
**Status**: ✅ Production Ready
