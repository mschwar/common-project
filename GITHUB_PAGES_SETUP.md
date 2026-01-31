# GitHub Pages Setup Guide

## Quick Setup (5 minutes)

### 1. Initialize Git Repository

```bash
cd c:\Users\Matty\Documents\common-projects\common-projects
git init
git add .
git commit -m "Initial commit: Common Projects with 5 concept entries"
```

### 2. Create GitHub Repository

1. Go to <https://github.com/new>
2. Repository name: `common-projects`
3. Description: "PhD-level concepts in kindergarten-simple language"
4. Public repository
5. Do NOT initialize with README (we already have one)
6. Click "Create repository"

### 3. Push to GitHub

```bash
git remote add origin https://github.com/Matthew41785338/common-projects.git
git branch -M main
git push -u origin main
```

### 4. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
3. Click **Save**

### 5. Wait for Deployment

- Check Actions tab to see deployment progress (~2-3 minutes)
- Once complete, site will be live at: `https://matthew41785338.github.io/common-projects/`

---

## Alternative: Use GitHub Actions (Recommended)

The repository already has a workflow file (`.github/workflows/deploy.yml`) that automates deployment.

### Enable GitHub Actions Deployment

1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: **GitHub Actions**
3. Push any change to `main` branch
4. Workflow automatically:
   - Converts markdown to HTML
   - Updates index
   - Deploys to Pages

---

## Verification

After deployment, verify:

- ✅ Homepage loads at your GitHub Pages URL
- ✅ Progress bar shows 10% (5/50 concepts)
- ✅ All 5 entry cards are visible
- ✅ Clicking an entry opens the detailed page
- ✅ Navigation back to homepage works
- ✅ Styling and animations display correctly

---

## Troubleshooting

### Site Not Loading?

- Check Actions tab for deployment errors
- Verify Pages is enabled in Settings
- Confirm `/docs` folder exists and has `index.html`

### Styling Missing?

- Clear browser cache
- Check browser console for errors
- Verify `styles.css` is in `/docs/` directory

### Entries Not Showing?

- Run `python scripts/convert_to_html.py` locally
- Check `/docs/entries/` has `.html` files
- Update `script.js` with correct entry data

---

## Next Steps

1. **Add More Entries**: Create new markdown files in `/entries/`
2. **Run Converter**: `python scripts/convert_to_html.py`
3. **Commit & Push**: Deployment happens automatically
4. **Share**: Post your website link on social media!

---

*Repository ready for public launch!* 🚀
