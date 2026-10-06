# Skope website

Complete source and assets for the Skope landing page, exported October 6, 2026.

## Files

- `dist/index.html`: page content and scroll animations.
- `dist/style.css`: Arsenal typography, gradient, responsive layout, and styling.
- `dist/assets/`: app icon, logo, creator portraits, and the previously supplied Rive animation/player files.
- `dist/character.js` and `dist/character.png`: retained from the earlier character animation. The current page displays the static app icon.

## Preview locally

From this folder, run:

```sh
python3 -m http.server 8000 --directory dist
```

Visit http://localhost:8000. No npm installation or build step is required. Arsenal loads from Google Fonts.

## Add to GitHub

1. Create an empty repository on GitHub, for example `skope-website`.
2. Extract this ZIP.
3. Upload `README.md` and the entire `dist` folder to the repository. Upload the extracted files, rather than this ZIP.

To push using Git instead, from this folder run:

```sh
git init
git add README.md dist
git commit -m "Add Skope website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/skope-website.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username, using the URL of the repository you created.

## Hosting

Use `dist` as the static website directory. No build command is needed.

The private Sites hosting manifest and Git credentials are excluded from this export.
