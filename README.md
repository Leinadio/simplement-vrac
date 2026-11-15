# Simplement Vrac — refonte du site

Site statique de plusieurs pages, déployé sur Vercel.

- `_src/build.py` génère toutes les pages (`index.html`, `notre-epicerie/`, `nos-producteurs/`, `le-vrac/`, `actualites/`, `contact/`, `credits/`).
- Les textes, producteurs, horaires et résumés d'articles sont dans `_src/build.py` ; la liste des articles dans `_src/posts.json`.
- Styles communs : `assets/css/style.css` ; scripts communs : `assets/js/main.js` (dont les horaires d'ouverture utilisés par l'indicateur « Ouvert / Fermé »).

Après une modification : `python3 _src/build.py`, puis commit et push (Vercel redéploie automatiquement).
