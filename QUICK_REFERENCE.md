# Quick Reference Card

## 🚀 Start Here (3 Commands)

```bash
cd frontend-react
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser.

---

## 📂 Important Files

| File | What to Edit |
|------|-------------|
| `src/App.jsx` | Backend URL, main logic |
| `src/styles.css` | Colors, layout, fonts |
| `vite.config.js` | Port number, build settings |
| `package.json` | Dependencies |

---

## 🎨 Change Colors

Edit `src/styles.css`:

```css
/* Change primary blue */
.main-content h1 {
  color: #5f9ed6;  /* ← Change this */
}

/* Change accent orange */
.node-button {
  background: #2a2f4a;  /* ← Or this */
}
```

---

## 🔧 Change Backend URL

Edit `src/App.jsx` line 8:

```javascript
const BACKEND_URL = "http://your-backend-url:port";
```

---

## 📦 npm Commands

```bash
npm install      # Install dependencies (run once)
npm run dev      # Start dev server (hot reload)
npm run build    # Build for production
npm run preview  # Preview production build
```

---

## 🗂️ File Structure

```
frontend-react/
├── package.json          ← Dependencies
├── vite.config.js        ← Config
├── index.html            ← Template
└── src/
    ├── main.jsx          ← Entry point
    ├── App.jsx           ← Main component
    ├── styles.css        ← Global styles
    ├── components/
    │   ├── TreeNode.jsx
    │   ├── TreeDisplay.jsx
    │   └── NodePanel.jsx
    └── styles/
        ├── TreeNode.css
        └── NodePanel.css
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to backend | Check `BACKEND_URL` in App.jsx |
| Port 3000 in use | Change `port` in vite.config.js |
| Styles don't load | `Ctrl+Shift+Delete` → clear cache |
| npm install fails | Delete `node_modules`, `package-lock.json`, try again |
| Nothing appears | Check browser console (F12) for errors |

---

## 🎯 All Features

✅ View conversation tree with expand/collapse
✅ View node prompt & LLM response
✅ Create new branches from any node
✅ Clear individual branches
✅ Clear entire tree
✅ Refresh tree data
✅ Dark theme UI
✅ Real-time updates
✅ Error handling

---

## 📱 Browser Support

Works on:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)

---

## 🚀 Deployment

Build for production:
```bash
npm run build
```

Upload `dist/` folder to:
- Netlify
- Vercel
- GitHub Pages
- Any web server

---

## 💡 Pro Tips

1. **Hot Reload**: Changes save automatically (no manual refresh)
2. **DevTools**: Press F12 for browser tools
3. **Network Tab**: Debug API calls here
4. **Console**: Check for JavaScript errors
5. **React DevTools**: Install extension for better debugging

---

## 🔌 Backend Endpoints

```
GET    /tree              Get tree
POST   /chat              Send message
DELETE /clear/{id}        Delete branch
DELETE /clear             Delete tree
```

All endpoints return JSON responses.

---

## 📞 Need Help?

1. Check browser console (F12)
2. Check backend logs
3. Ensure backend is running on `http://localhost:8000`
4. Restart dev server: `npm run dev`

---

**Last Updated**: January 15, 2026
**Status**: ✅ Ready to Use
