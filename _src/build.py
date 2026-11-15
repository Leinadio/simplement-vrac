#!/usr/bin/env python3
"""Génère les pages statiques du site Simplement Vrac.

Usage : python3 _src/build.py   (depuis la racine du projet)
Les fichiers produits (index.html, notre-epicerie/index.html, …) sont servis tels quels par Vercel.
"""
import json
import os
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_src")
read = lambda name: open(os.path.join(SRC, name), encoding="utf-8").read()

SHOP = "https://www.simplement-vrac.fr"
ESHOP = f"{SHOP}/epicerie-en-ligne/"
EXT = ' target="_blank" rel="noopener"'
MAPS = "https://www.google.com/maps/dir/?api=1&destination=134+rue+Pierre+Brossolette+93160+Noisy-le-Grand"

# ---------------------------------------------------------------- icônes
I = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "ext": '<svg class="ext" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12zm0-9a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8h3V4h-3a5 5 0 0 0-5 5v2H7v4h2v7h4v-7h3l1-4h-4V9a1 1 0 0 1 1-1z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16 3c.4 2.4 2 4 4.5 4.3v3.4a8 8 0 0 1-4.4-1.4v6.2a6 6 0 1 1-6-6h.6v3.5a2.6 2.6 0 1 0 1.9 2.5V3z"/></svg>',
    "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
    "burger": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h10"/></svg>',
    "leaf": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 26C6 13 14 6 27 5c0 13-7 21-20 21z"/><path d="M6 26 18 14"/></svg>',
    "route": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="8" cy="24" r="3"/><circle cx="24" cy="8" r="3"/><path d="M11 24h8a4 4 0 0 0 0-8h-6a4 4 0 0 1 0-8h8"/></svg>',
    "tag": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 16V5h11l13 13-11 11z"/><circle cx="10" cy="11" r="2"/></svg>',
    "coin": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="16" cy="16" r="11"/><path d="M20 11.5a5 5 0 1 0 0 9M10 14.5h8M10 17.5h8"/></svg>',
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/></svg>',
    "office": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 21V4h10v17M14 9h6v12M8 8h2M8 12h2M8 16h2"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="9" width="18" height="12" rx="1"/><path d="M3 13h18M12 9v12M12 9C9 9 7 4 10 4s2 5 2 5 0-5 3-5 1 5-3 5"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
}

# ---------------------------------------------------------------- données
HOURS_ROWS = [
    ("1", "Lundi", "12h00 – 19h00"),
    ("2,3,4,5,6", "Du mardi au samedi", "10h00 – 19h30"),
    ("0", "Dimanche", "10h00 – 13h00"),
]

NAV = [
    ("/notre-epicerie/", "L'épicerie", "epicerie"),
    ("/le-vrac/", "Le vrac, c'est quoi ?", "vrac"),
    ("/nos-producteurs/", "Nos producteurs", "producteurs"),
    ("/actualites/", "Actualités", "actus"),
    ("/contact/", "Nous trouver", "contact"),
]

# Producteurs : textes réécrits à partir des informations du site actuel.
PRODUCERS = [
    dict(n="Fromaville", logo="fromaville", f="idf", where="Saint-Ouen (93)", what="Yaourts et fromages",
         story="La première laiterie de Seine-Saint-Denis. Xavier y fabrique nos yaourts en pot de verre consigné et des fromages comme le Claquos de Saint-Ouen, avec le lait bio de deux fermes voisines."),
    dict(n="Belledonne", logo=None, f="idf", where="Santeny (94)", what="Pain bio",
         story="Du pain bio fait chaque jour, avec des paysans et un moulin d'Île-de-France. Les farines sont achetées selon les principes du commerce équitable."),
    dict(n="C.Q.F.D.", logo="cqfd", f="idf", where="Villenoy (77)", what="Pâtes et sauces",
         story="Un atelier ouvert en 2022 près de Meaux, que nous sommes allés voir. Pâtes au blé dur bio francilien tréfilées au bronze, et ravioles aux produits du terroir, comme le Brie et la moutarde de Meaux."),
    dict(n="Duchamps à ton assiette", logo="duchamps", f="idf", where="Vert-Saint-Denis et Courquetaine (77)", what="Farines et pâtes",
         story="Deux fermes en bio depuis 2016, qui transforment elles-mêmes leurs céréales depuis 2019. Farines moulues sur meules de pierre, et pâtes faites seulement de farine et d'eau."),
    dict(n="La Parisienne", logo=None, f="idf", where="Pantin (93)", what="Bières artisanales",
         story="Brasserie indépendante, pionnière de la bière artisanale à Paris depuis 2014 et premier houblonnier de la capitale. Nous avons visité leur brasserie de Pantin."),
    dict(n="La Ottanta", logo="la-ottanta", f="idf", where="Île-de-France", what="Mozzarella et burrata bio",
         story="Des artisans italiens installés en Île-de-France, qui travaillent un lait bio produit à 80 km de Paris par deux élevages qu'ils suivent de près."),
    dict(n="Sacré Willy", logo="sacre-willy", f="fr", where="Alpes", what="Produits laitiers",
         story="Maîtres laitiers de père en fils depuis plus d'un siècle. Le lait vient de fermes de montagne situées à moins de 25 km de leur atelier."),
    dict(n="Promis Juré", logo="promis-jure", f="fr", where="Hauts-de-France", what="Glaces et sorbets",
         story="Des crèmes glacées et des sorbets pleins fruits, faits en circuit court. Leur glace vanille a été classée troisième meilleure de France par Gault&Millau."),
    dict(n="Endro Cosmétiques", logo="endro", f="fr", where="Lannion (22)", what="Cosmétiques bio",
         story="Boris et Marion fabriquent en Bretagne des cosmétiques bio d'origine 100 % naturelle, vendus en bocaux de verre consignés. Un produit acheté, un mètre carré de plage nettoyé."),
    dict(n="Château La Brande", logo="chateau-la-brande", f="fr", where="Saillans (33)", what="Vins de Fronsac",
         story="Après avoir traversé l'Atlantique à la rame, Benoît et Maud Soulies ont repris ce domaine fondé en 1730. Leurs vins sont vinifiés sans soufre, et certains sans soufre ajouté."),
    dict(n="Le Temps des Oliviers", logo="le-temps-des-oliviers", f="fr", where="Lyon · Méditerranée", what="Huiles d'olive, olives, antipasti",
         story="Depuis 2012, Guillaume et Gautier parcourent le bassin méditerranéen à la rencontre de producteurs passionnés. Huiles d'olive, olives, vinaigres et antipasti bio."),
    dict(n="Pierre & Tim", logo="pierre-et-tim", f="fr", where="France", what="Cookies",
         story="Deux amis et une même gourmandise. Des cookies faits à la main avec des ingrédients d'artisans français, dans des emballages soignés."),
    dict(n="Pur etc.", logo="pur-etc", f="fr", where="France", what="Plats cuisinés de saison",
         story="Fondé par Héloïse Chalvignac et Vincent Viaud pour prouver qu'on peut manger local, sain et vite. Une cuisine de saison à partir de produits frais, sans surgelé."),
    dict(n="Loumaë", logo="loumae", f="fr", where="France", what="Céréales du petit déjeuner",
         story="Des céréales croustillantes sans sucre raffiné, sans huile et sans additif, faites avec des ingrédients de filières bio."),
    dict(n="Naé Food", logo="nae-food", f="fr", where="France", what="Boissons à l'hibiscus",
         story="Infusions et boissons artisanales à base d'hibiscus, sans colorant ni conservateur. Leur infusion pétillante se marie très bien avec d'autres boissons."),
    dict(n="Savons Arthur", logo="savons-arthur", f="fr", where="France", what="Savons artisanaux",
         story="Passionné de chimie depuis le collège, Arthur a fait de la saponification son métier. Une entreprise familiale, de fils en père, depuis 2015."),
    dict(n="Gaiia", logo="gaiia", f="fr", where="France", what="Savons saponifiés à froid",
         story="Des savons faits à la main par saponification à froid, la méthode qui garde la glycérine naturelle. Un surgras d'au moins 6,5 % pour une grande douceur."),
    dict(n="Kasana", logo="kasana", f="eq", where="Burkina Faso · Ouganda", what="Fruits secs et vanille",
         story="Augustin et François-Xavier forment des agriculteurs au séchage solaire et valorisent les surplus de fruits. Des filières en commerce équitable, sans intermédiaire inutile."),
    dict(n="Terra Kahwa", logo="terra-kahwa", f="eq", where="Éthiopie", what="Cafés",
         story="Quatre amis partis en 2008 suivre le grain de café jusqu'en Éthiopie. Cinq cafés des hauts plateaux, cueillis à la main, torréfiés et moulus sur place."),
]
DARK_LOGOS = {"fromaville", "duchamps"}  # logos clairs, posés sur fond sombre
BADGE = {"idf": "Île-de-France", "fr": "France", "eq": "Commerce équitable"}

# Actualités : titres, dates et images du site actuel, résumés réécrits.
CATS = {"b": "La boutique", "p": "Produits", "r": "Recettes & bien-être"}
SUMMARIES = {
    2539: ("b", "Le bon de commande des fêtes est arrivé : réservez votre repas de fin d'année en boutique ou en ligne."),
    2531: ("r", "Quelles farines choisir pour remplacer le blé dans vos gâteaux, et dans quelles proportions."),
    2526: ("p", "Un chocolat aussi bon qu'équitable, à découvrir dans nos rayons."),
    2518: ("b", "Le bon de commande des fêtes 2024 pour préparer votre réveillon sans stress."),
    2503: ("r", "Ses vertus, ses usages, et pourquoi il remplace si bien le sucre blanc."),
    2499: ("r", "Frais ou en poudre en vrac, une épice aux nombreux bienfaits."),
    2493: ("p", "Le curcuma frais est arrivé en magasin : ses bienfaits et comment le cuisiner."),
    2489: ("p", "L'histoire de ce petit agrume d'hiver, et tout ce qu'il a de bon."),
    2478: ("b", "Le bon de commande des fêtes 2023."),
    2474: ("r", "Une recette d'automne prête en 35 minutes, plébiscitée par nos clients."),
    2470: ("p", "Le pomelo vert, doux et très sucré : comment le choisir et le déguster."),
    2466: ("r", "Une infusion connue depuis l'Antiquité, alliée de la digestion."),
    2456: ("r", "Le thym, plante aromatique et remède de toujours, en infusion."),
    2452: ("r", "Une plante au parfum citronné pour les petits maux de l'hiver."),
    2448: ("b", "Simplement Vrac a posé pour le projet photo de Mary-Lou Mauricio sur la hausse du CO2."),
    2442: ("b", "Simplement Vrac en reportage sur les courses en vrac au quotidien."),
    2417: ("r", "Vert, noir, blanc : ce que chaque thé apporte à notre santé."),
    2413: ("r", "Fraîcheur et gourmandise : nos idées de thé glacé pour l'été."),
    2403: ("b", "L'association des commerçants du centre-ville de Noisy-le-Grand."),
    2395: ("p", "Formes, couleurs et saveurs : la belle saison des tomates anciennes."),
    2389: ("r", "Un allié naturel du jardinier bio pour garder un potager sain."),
    2386: ("p", "De l'ail fermenté au goût doux et sucré, plein de bienfaits."),
    2383: ("p", "Des jus 100 % bio et purs, en bouteilles consignées."),
    2374: ("b", "En avril 2023, un bon d'achat offert chez notre partenaire Noisy Liens."),
    2343: ("b", "Parmi les quatre finalistes du prix de la création d'entreprise à impact en Seine-Saint-Denis."),
    2328: ("p", "Sauces, biscuits siciliens, parmesan, pesto de Gênes : nos sélections italiennes."),
    2325: ("b", "Nos horaires d'ouverture à l'automne 2022."),
    2313: ("b", "Notre premier bon de commande des fêtes."),
    2212: ("p", "Des œufs extra-frais bio d'une ferme d'Égreville, à 40 km de la boutique."),
    2259: ("b", "Ateliers gastronomie bio et zéro déchet avec Stéphanie et Bruno."),
    2253: ("r", "La recette d'une moutarde maison, avec des graines achetées en vrac."),
    704: ("b", "Animations et dégustations du mois de septembre 2022."),
    2228: ("p", "Près de 30 artisans et producteurs, dont la moitié à moins de 200 km de la boutique."),
}
POSTS = json.load(open(os.path.join(SRC, "posts.json"), encoding="utf-8"))
for p in POSTS:
    p["cat"], p["sum"] = SUMMARIES[p["id"]]
    if p["id"] == 2526:
        p["img"] = "img/actus/sunshine-chocolats-boutique.jpg"

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
def fdate(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"

# ---------------------------------------------------------------- gabarit
def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="icon" type="image/png" href="/img/logo/favicon.png">
<link rel="apple-touch-icon" href="/img/logo/apple-touch-icon.png">
<meta name="theme-color" content="#F5EFE3">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Young+Serif&family=Hanken+Grotesk:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
"""

def header(active):
    cur = ' aria-current="page"'
    links = "\n".join(
        f'        <li><a href="{h}"{cur if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    return f"""<div class="infobar">
  <div class="wrap">
    <span class="status" id="status"><span class="dot"></span><span id="statusText">Ouvert 7 jours sur 7</span></span>
    <span class="meta">
      <a class="addr" href="/contact/">134, rue Pierre Brossolette · Noisy-le-Grand</a>
      <a href="tel:+33141675365">01 41 67 53 65</a>
    </span>
  </div>
</div>

<header class="nav" id="nav">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Simplement Vrac, accueil">
      <img src="/img/logo/logo.png" alt="Simplement Vrac, épicerie bio" width="256" height="88">
    </a>
    <nav aria-label="Navigation principale">
      <ul id="menu">
{links}
        <li class="menu-cta"><a class="btn btn-primary" href="{ESHOP}" target="_blank" rel="noopener">Boutique en ligne</a></li>
      </ul>
    </nav>
    <div class="actions">
      <a class="icon-btn" href="{SHOP}/my-account/" target="_blank" rel="noopener" aria-label="Mon compte">{I["user"]}</a>
      <a class="btn btn-primary" href="{ESHOP}" target="_blank" rel="noopener">Boutique en ligne</a>
      <button class="icon-btn burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu" style="background:none;cursor:pointer;color:inherit">{I["burger"]}</button>
    </div>
  </div>
</header>
"""

def footer():
    return f"""<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo logo-badge" href="/"><img src="/img/logo/logo.png" alt="Simplement Vrac, épicerie bio" width="256" height="88" loading="lazy"></a>
        <p style="margin-top:1rem;max-width:30ch">Épicerie bio, zéro déchet et locale. 134, rue Pierre Brossolette, 93160 Noisy-le-Grand.</p>
        <div class="socials">
          <a href="https://www.instagram.com/simplement_vrac" aria-label="Instagram" target="_blank" rel="noopener">{I["insta"]}</a>
          <a href="https://www.facebook.com/bruno.cuigniez" aria-label="Facebook" target="_blank" rel="noopener">{I["fb"]}</a>
          <a href="https://www.tiktok.com/@simplementvrac" aria-label="TikTok" target="_blank" rel="noopener">{I["tiktok"]}</a>
        </div>
      </div>
      <div>
        <h4>L'épicerie</h4>
        <ul><li><a href="/notre-epicerie/">Notre épicerie</a></li><li><a href="/nos-producteurs/">Nos producteurs</a></li><li><a href="/le-vrac/">Le vrac, c'est quoi ?</a></li><li><a href="/actualites/">Actualités</a></li></ul>
      </div>
      <div>
        <h4>Pratique</h4>
        <ul><li><a href="/contact/">Horaires et accès</a></li><li><a href="{ESHOP}" target="_blank" rel="noopener">Boutique en ligne</a></li><li><a href="{SHOP}/my-account/" target="_blank" rel="noopener">Mon compte</a></li><li><a href="https://reseauconsigne.gogocarto.fr/map#/fiche/SIMPLEMENT-VRAC/qy/" target="_blank" rel="noopener">Réseau Consigne</a></li></ul>
      </div>
      <div>
        <h4>Informations</h4>
        <ul><li><a href="{SHOP}/cgv-mentions-legales/" target="_blank" rel="noopener">CGV et mentions légales</a></li><li><a href="{SHOP}/politique-de-confidentialite/" target="_blank" rel="noopener">Politique de confidentialité</a></li><li><a href="{SHOP}/wp-content/uploads/2023/09/Epiciers-de-France-Affiche-Mediateur-consommation.pdf" target="_blank" rel="noopener">Médiateur de la consommation</a></li><li><a href="/credits/">Crédits photos</a></li></ul>
      </div>
    </div>
    <div class="bottom"><span>© Simplement Vrac</span><span>Paiement sécurisé · Visa · Mastercard · Stripe</span></div>
    <div class="bigword" aria-hidden="true">Simplement Vrac</div>
  </div>
</footer>

<script src="/assets/js/main.js"></script>
</body>
</html>
"""

def page(active, title, desc, body, patterns=False):
    return head(title, desc) + (read("patterns.html") if patterns else "") + header(active) + "\n<main>\n" + body + "\n</main>\n\n" + footer()

def page_hero(crumb, kicker, h1, lead, img=None, alt=""):
    band = f'\n      <div class="band"><img src="/{img}" alt="{alt}" fetchpriority="high"></div>' if img else ""
    return f"""  <section class="page-hero">
    <div class="wrap">
      <div class="crumbs"><a href="/">Accueil</a> · {crumb}</div>
      <span class="tag">{kicker}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>{band}
    </div>
  </section>
"""

def hours_table():
    rows = "\n".join(f'            <tr data-days="{d}"><td>{t}</td><td>{h}</td></tr>' for d, t, h in HOURS_ROWS)
    return f"""        <table class="hours" aria-label="Horaires d'ouverture">
          <tbody>
{rows}
          </tbody>
        </table>"""

def contact_lines():
    return f"""        <div class="contact-lines">
          <a href="tel:+33141675365">{I["phone"]}01 41 67 53 65</a>
          <a href="mailto:bruno@simplement-vrac.fr">{I["mail"]}bruno@simplement-vrac.fr</a>
        </div>"""

def post_card(p, cat=True, lazy=True):
    lz = ' loading="lazy"' if lazy else ""
    img = f'<img src="/{p["img"]}" alt=""{lz}>' if p.get("img") else ""
    badge = f'<span class="cat">{CATS[p["cat"]]}</span>' if cat else ""
    return f"""        <a class="post reveal" href="{p["link"]}" target="_blank" rel="noopener" data-f="{p["cat"]}">
          <div class="art">{badge}{img}</div>
          <div class="body"><time datetime="{p["date"]}">{fdate(p["date"])}</time><h3>{escape(p["title"])}</h3><p class="sum">{escape(p["sum"])}</p><span class="more">Lire l'article {I["ext"]}</span></div>
        </a>"""

def logos_wall():
    tiles = []
    for p in PRODUCERS:
        inner = f'<img src="/img/producteurs/{p["logo"]}.png" alt="{escape(p["n"])}" loading="lazy">' if p["logo"] else f'<span class="wordmark">{escape(p["n"])}</span>'
        dk = ' class="dk"' if p["logo"] in DARK_LOGOS else ""
        tiles.append(f'<a{dk} href="/nos-producteurs/#{slug(p["n"])}" title="{escape(p["n"])}">{inner}</a>')
    return '      <div class="logos reveal">\n        ' + "\n        ".join(tiles[:18]) + "\n      </div>"

def slug(s):
    import re, unicodedata
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

NEWSLETTER = """  <div class="letter" id="lettre">
    <div class="wrap">
      <div class="box reveal">
        <div>
          <h2>Une petite lettre,<br>de temps en temps.</h2>
          <p>Les événements, les nouveautés, les bons plans et quelques recettes, directement dans votre boîte mail.</p>
        </div>
        <div>
          <form id="nl" novalidate>
            <label for="email" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Votre adresse e-mail</label>
            <input id="email" type="email" placeholder="votre@email.fr" autocomplete="email" required>
            <button class="btn btn-primary" type="submit">Je m'inscris</button>
          </form>
          <p class="ok" id="nlMsg" role="status"></p>
        </div>
      </div>
    </div>
  </div>"""

def gestes_section(title_html, intro, notes=True):
    notes_html = """      <div class="how-notes reveal">
        <div><b>La juste quantité</b>Une cuillère d'épices pour une recette, ou de quoi tenir le mois : c'est vous qui décidez.</div>
        <div><b>Moins d'emballages</b>Pas d'emballage superflu, et des contenants consignés quand le vrac ne s'y prête pas.</div>
        <div><b>Une origine connue</b>Des produits bio dont vous savez d'où ils viennent et combien de kilomètres ils ont parcouru.</div>
      </div>""" if notes else ""
    return f"""  <section class="how" id="gestes">
    <div class="wrap">
      <div class="section-head reveal">
        <div><span class="kicker">Le vrac, c'est quoi ?</span><h2>{title_html}</h2></div>
        <p>{intro}</p>
      </div>
{read("gestes.html")}{notes_html}
    </div>
  </section>"""

# ================================================================ ACCUEIL
def home():
    latest = "\n".join(post_card(p, cat=False) for p in POSTS[:3])
    marquee = "".join(f"<span>{t}</span>" for t in [
        "Pain bio de Belledonne", "Yaourts Fromaville en verre consigné", "Pâtes C.Q.F.D. de Seine-et-Marne", "Café Terra Kahwa",
        "Glaces Promis Juré", "Burrata La Ottanta", "Bières La Parisienne", "Savons Arthur", "Fruits et légumes de saison", "Plus de 2000 produits bio"])
    body = f"""  <section class="hero" style="padding-bottom:3rem">
    <div class="wrap">
      <div class="intro">
        <span class="tag">Au centre de Noisy-le-Grand</span>
        <h1>
          <span class="line"><span>Épicerie bio,</span></span>
          <span class="line"><span><em class="hand">zéro déchet</em></span></span>
          <span class="line"><span>et locale.</span></span>
        </h1>
        <p class="lead">Plus de 2000 produits bio en circuit court, en vrac ou en contenants consignés, dans une épicerie de quartier où l'on vient avec ses bocaux.</p>
        <div class="ctas">
          <a class="btn btn-primary" href="/notre-epicerie/">Découvrir l'épicerie {I["arrow"]}</a>
          <a class="btn btn-ghost" href="/le-vrac/">Le vrac, c'est quoi ?</a>
        </div>
        <div class="proofs">
          <div class="proof"><b>95 %</b><span>de produits<br>bio</span></div>
          <div class="proof"><b>2000+</b><span>produits<br>en rayon</span></div>
          <div class="proof"><b>7/7</b><span>ouvert<br>tous les jours</span></div>
        </div>
      </div>

      <div class="front">
        <div class="shopfront">
          <img class="hero-photo" src="/img/boutique/interieur.jpg" alt="L'intérieur de l'épicerie Simplement Vrac : rayons en bois, silos de vrac et cagettes du primeur" fetchpriority="high">
          <div class="sign">Épicerie · Noisy-le-Grand</div>
        </div>
        <figure class="round"><img src="/img/boutique/devanture.jpg" alt="La devanture de Simplement Vrac, rue Pierre Brossolette"></figure>
        <div class="hang h1"><b>Bocal oublié ?</b>On vous en prête un.</div>
        <div class="hang h2"><b>Pesé, rempli,</b>vous payez le contenu.</div>
      </div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true"><div class="track" id="track">{marquee}</div></div>

  <section id="epicerie">
    <div class="wrap split">
      <div class="prose reveal">
        <span class="kicker">Notre épicerie</span>
        <h2>Tout pour vos courses,<br>sans le suremballage.</h2>
        <p>Simplement Vrac est une épicerie <strong>bio, vrac et locale</strong> au cœur du centre-ville de Noisy-le-Grand. Épicerie en vrac, primeur, fromagerie, produits frais, boissons, hygiène et cosmétiques : vous pouvez y faire l'essentiel de vos courses.</p>
        <p>Sur chaque étiquette : la composition, les labels, la provenance et les kilomètres parcourus jusqu'à la boutique.</p>
        <a class="btn btn-primary" href="/notre-epicerie/">Découvrir l'épicerie {I["arrow"]}</a>
      </div>
      <div class="split-media reveal">
        <div class="duo"><img src="/img/boutique/silos.jpg" alt="Silos de vrac remplis de céréales et de légumineuses" loading="lazy"><img src="/img/boutique/primeur.jpg" alt="Le rayon primeur et ses cagettes de fruits et légumes" loading="lazy"></div>
        <div class="sticker" style="left:-14px;bottom:18%"><b>95 % bio</b>et le plus local possible</div>
      </div>
    </div>
  </section>

{gestes_section("Cinq gestes,<br>et c'est déjà une habitude.", "Néophyte du vrac ? On pèse le contenant vide, on le remplit, et vous ne payez que ce qu'il y a dedans. Une autre façon de faire ses courses, bonne pour la planète et pour le porte-monnaie.")}

  <section id="producteurs">
    <div class="wrap">
      <div class="section-head reveal">
        <div><span class="kicker">Nos producteurs</span><h2>Ceux qui remplissent<br>nos rayons.</h2></div>
        <p>Nous cherchons toujours les meilleurs producteurs pour vous proposer le top du bio et du local. Ils sont majoritairement français, et certains travaillent à quelques kilomètres de la boutique.</p>
      </div>
{logos_wall()}
      <div style="margin-top:2rem;text-align:center" class="reveal"><a class="btn btn-ghost" href="/nos-producteurs/">Découvrir leurs histoires {I["arrow"]}</a></div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="founder reveal">
        <figure><img src="/img/equipe/bruno.jpg" alt="Bruno, fondateur de Simplement Vrac, dans la boutique devant les silos de vrac" loading="lazy"><figcaption>Bruno · fondateur</figcaption></figure>
        <div>
          <span class="kicker">Derrière le comptoir</span>
          <h2>Bruno, fondateur de Simplement Vrac.</h2>
          <p>C'est lui qui vous accueille à la boutique, sélectionne les produits et va à la rencontre des producteurs.</p>
          <p>Ses coups de cœur, les nouveautés et les dégustations à venir, il les partage chaque semaine en vidéo sur Instagram.</p>
          <a class="btn btn-ghost" href="https://www.instagram.com/simplement_vrac" target="_blank" rel="noopener">Suivre @simplement_vrac {I["ext"]}</a>
        </div>
      </div>
    </div>
  </section>

  <section id="actus" style="padding-top:0">
    <div class="wrap">
      <div class="section-head reveal">
        <div><span class="kicker">Nos actualités</span><h2>L'épicerie évolue<br>constamment.</h2></div>
        <a class="btn btn-ghost" href="/actualites/">Toute l'actualité</a>
      </div>
      <div class="news">
{latest}
      </div>
    </div>
  </section>

  <section id="venir" style="padding-top:0">
    <div class="wrap visit-grid">
      <div class="reveal">
        <div class="storefront" style="margin:0;box-shadow:0 30px 50px -30px rgba(0,0,0,.6)"><img src="/img/boutique/devanture.jpg" alt="La devanture de Simplement Vrac au 134, rue Pierre Brossolette" loading="lazy"></div>
      </div>
      <div class="reveal">
        <span class="kicker">Nous trouver</span>
        <h2>134, rue<br>Pierre Brossolette.</h2>
{hours_table()}
{contact_lines()}
        <a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">Itinéraire {I["arrow"]}</a>
      </div>
    </div>
  </section>

{NEWSLETTER}"""
    return page("home", "Simplement Vrac · Épicerie bio, zéro déchet et locale à Noisy-le-Grand",
                "Épicerie bio, zéro déchet et locale au centre de Noisy-le-Grand : vrac, primeur, fromagerie, consigne et plus de 2000 produits bio.",
                body, patterns=True)

# ================================================================ L'ÉPICERIE
def epicerie():
    rayons = [
        ("big over", "silos", "Silos de vrac remplis de céréales, de pâtes et de légumineuses", "01", "L'épicerie en vrac", "Céréales, légumineuses, pâtes, farines, fruits secs, café, thé, huiles… en vrac ou en contenants consignés."),
        ("big over", "primeur", "Le rayon primeur et ses cagettes", "02", "Primeur", "Fruits et légumes bio et de saison, dont ceux d'une maraîchère de Chelles, à 5 km."),
        ("card", "rayons", "Étagères de produits frais et d'épicerie", "03", "Fromagerie & frais", "Fromages, yaourts, pâtes fraîches et plats cuisinés en libre-service."),
        ("card", "vins", "Bouteilles de vin et de bière", "04", "Boissons", "Vins, bières artisanales, jus et infusions, pour les petits comme pour les grands."),
        ("card", "cookies", "Bocaux de cookies et de gâteaux", "05", "Pains & douceurs", "Pains et cakes bio à la coupe, cookies, biscuits et chocolats."),
    ]
    cards = []
    for cls, img, alt, n, t, d in rayons:
        if "over" in cls:
            cards.append(f'        <article class="aisle {cls} reveal"><img src="/img/boutique/{img}.jpg" alt="{alt}" loading="lazy"><div class="txt"><span class="num">{n}</span><h3>{t}</h3><p>{d}</p></div></article>')
        else:
            cards.append(f'        <article class="aisle {cls} reveal"><div class="ph"><img src="/img/boutique/{img}.jpg" alt="{alt}" loading="lazy"></div><div class="txt"><span class="num">{n}</span><h3>{t}</h3><p>{d}</p></div></article>')
    cards.append(f"""        <article class="aisle wide reveal"><div class="ph"><img src="/img/boutique/hygiene.jpg" alt="Rayon hygiène : gourdes, savons et cosmétiques" loading="lazy"></div><div class="txt"><span class="num">06</span><h3>Hygiène, cosmétiques & maison</h3><p>Savons, shampoings, cosmétiques en circuit court, produits d'entretien et ustensiles réutilisables. Prêts à l'emploi ou de quoi les fabriquer vous-même.</p><a class="btn btn-ghost" href="/actualites/">Nos recettes maison</a></div></article>""")
    values = [
        ("#E6EFD6", "#2D5A3B", "route", "Produits locaux", "Nous privilégions les productions locales pour réduire l'impact des transports."),
        ("#FBEBC6", "#B57A12", "leaf", "Agriculture bio", "La quasi-totalité de nos produits, 95 %, est issue de l'agriculture biologique."),
        ("#F6DDD5", "#B4442C", "tag", "Origine garantie", "Le producteur, le lieu de récolte et les kilomètres parcourus sont toujours indiqués."),
        ("#DCEBEA", "#2C6B66", "coin", "Économique", "Acheter la juste quantité évite la surconsommation et le gaspillage."),
    ]
    vals = "\n".join(f'        <div class="value reveal"><div class="ico" style="background:{bg};color:{fg}">{I[ic]}</div><h3>{t}</h3><p>{d}</p></div>' for bg, fg, ic, t, d in values)
    services = [
        ("bag", "Click & collect", "Commandez sur la boutique en ligne et récupérez vos courses en magasin.", ESHOP, "Commander"),
        ("truck", "Point de livraison", "Un point de retrait aux Richardets pour les habitants du quartier.", "/contact/", "Nous contacter"),
        ("heart", "Livraison à domicile", "Nous livrons les personnes à mobilité réduite, les personnes âgées, les femmes enceintes et les personnes alitées.", "tel:+33141675365", "Appeler la boutique"),
        ("office", "Entreprises", "Nous livrons aussi les entreprises : demandez-nous un devis adapté à vos besoins.", "mailto:bruno@simplement-vrac.fr", "Demander un devis"),
        ("gift", "Coffrets cadeaux", "Un coffret composé selon vos envies et votre budget : cosmétique, alimentaire, végétal ou vegan.", "/contact/", "En parler en boutique"),
        ("cal", "Commandes des fêtes", "Chaque fin d'année, un bon de commande pour préparer vos repas de fête sereinement.", "/actualites/", "Voir les actualités"),
    ]
    svcs = "\n".join(f'        <div class="svc-item reveal"><div class="ico">{I[ic]}</div><h3>{t}</h3><p>{d}</p><a href="{h}"{EXT if h.startswith("http") else ""}>{l} →</a></div>' for ic, t, d, h, l in services)
    body = page_hero("Notre épicerie", "Notre épicerie", "Des produits bons, bio, locaux et sans emballage.",
                     "Faire ses courses en vrac, c'est limiter, voire supprimer, les emballages à usage unique, tout en sachant d'où viennent les produits.",
                     "img/boutique/interieur.jpg", "L'intérieur de l'épicerie Simplement Vrac") + f"""
  <section style="padding-top:clamp(2rem,4vw,3rem)">
    <div class="wrap split">
      <div class="prose reveal">
        <span class="kicker">Votre magasin bio de centre-ville</span>
        <h2>Faites 100 % de vos courses au même endroit.</h2>
        <p>Devenez consom'acteur dans un commerce de proximité : Simplement Vrac vous accueille <strong>tous les jours</strong> pour vos achats du quotidien, en boutique, en click & collect ou sur notre point de livraison aux Richardets.</p>
        <p>Vous y trouverez une offre alimentaire complète en vrac ou en contenants consignés, un primeur, une fromagerie, un libre-service de plats cuisinés, yaourts et pâtes fraîches, une belle sélection de boissons, et un rayon hygiène, cosmétique et ustensiles réutilisables.</p>
        <p>Une question sur un produit ou sur le fonctionnement du vrac ? Nous sommes là pour vous répondre, pour que tout soit plus simple.</p>
      </div>
      <div class="split-media reveal">
        <img class="tall" src="/img/boutique/silos-2.jpg" alt="Rangée de silos de vrac dans la boutique" loading="lazy">
        <div class="sticker" style="right:-12px;top:12%"><b>Étiquettes claires</b>composition · labels<br>provenance · kilomètres</div>
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="section-head reveal">
        <div><span class="kicker">Nos rayons</span><h2>De l'épicerie<br>à la salle de bain.</h2></div>
        <p>Une offre pensée pour le quotidien, avec des produits prêts à l'emploi et de quoi tout fabriquer soi-même.</p>
      </div>
      <div class="aisles">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="section-head reveal">
        <div><span class="kicker">Nos engagements</span><h2>Bon, bio, local<br>et transparent.</h2></div>
        <p>Une sélection de produits de qualité, de provenance locale et cultivés en agriculture biologique dès que c'est possible.</p>
      </div>
      <div class="values">
{vals}
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="founder reveal">
        <figure><img src="/img/equipe/bruno.jpg" alt="Bruno, fondateur de Simplement Vrac, dans la boutique" loading="lazy"><figcaption>Bruno · fondateur</figcaption></figure>
        <div>
          <span class="kicker">Le fondateur</span>
          <h2>Bruno, de Simplement Vrac.</h2>
          <p>C'est lui qui vous accueille, sélectionne les produits et va à la rencontre des producteurs, dans leurs ateliers comme dans les salons professionnels.</p>
          <p>Il anime aussi la vie de la boutique : dégustations avec les producteurs, ateliers, et des nouvelles régulières en vidéo sur Instagram.</p>
          <a class="btn btn-ghost" href="https://www.instagram.com/simplement_vrac" target="_blank" rel="noopener">Suivre @simplement_vrac {I["ext"]}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="services" id="services">
    <div class="wrap">
      <div class="section-head reveal">
        <div><span class="kicker">Les services</span><h2>Plus simple<br>qu'on ne le croit.</h2></div>
        <p>Pas le temps de passer, ou pas la possibilité de vous déplacer ? Il y a sûrement une solution.</p>
      </div>
      <div class="svc-list">
{svcs}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap visit-grid">
      <div class="reveal"><div class="storefront" style="margin:0"><img src="/img/boutique/devanture.jpg" alt="La devanture de Simplement Vrac" loading="lazy"></div></div>
      <div class="reveal">
        <span class="kicker">Horaires et adresse</span>
        <h2>Vente directe au<br>134, rue Pierre Brossolette.</h2>
{hours_table()}
{contact_lines()}
        <a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">Itinéraire {I["arrow"]}</a>
      </div>
    </div>
  </section>

{NEWSLETTER}"""
    return page("epicerie", "Notre épicerie · Simplement Vrac", "Épicerie bio en vrac au centre de Noisy-le-Grand : rayons, engagements, services et horaires.", body)

# ================================================================ PRODUCTEURS
def producteurs():
    cards = []
    for p in PRODUCERS:
        logo = f'<img src="/img/producteurs/{p["logo"]}.png" alt="Logo {escape(p["n"])}" loading="lazy">' if p["logo"] else f'<span class="wordmark">{escape(p["n"])}</span>'
        cards.append(f"""        <article class="pcard reveal" id="{slug(p["n"])}" data-f="{p["f"]}">
          <div class="logo-tile{' dk' if p["logo"] in DARK_LOGOS else ''}">{logo}</div>
          <div class="body">
            <div class="top"><span class="where">{I["pin"]}{escape(p["where"])}</span><span class="badge">{BADGE[p["f"]]}</span></div>
            <h3>{escape(p["n"])}</h3>
            <span class="what">{escape(p["what"])}</span>
            <p class="story">{escape(p["story"])}</p>
          </div>
        </article>""")
    crit = [
        ("#FBEBC6", "#B57A12", "coin", "Rapport qualité/prix", "Disponibilité des produits, qualité et prix de vente stable : ce sont nos critères de sélection."),
        ("#E6EFD6", "#2D5A3B", "leaf", "Du bio local si possible", "Priorité au bio, et aux productions locales pour réduire l'impact des transports."),
        ("#F6DDD5", "#B4442C", "heart", "Des producteurs passionnés", "Nous choisissons aussi des entrepreneurs et des producteurs pour la passion de leur métier."),
    ]
    crits = "\n".join(f'        <div class="value reveal"><div class="ico" style="background:{bg};color:{fg}">{I[ic]}</div><h3>{t}</h3><p>{d}</p></div>' for bg, fg, ic, t, d in crit)
    body = page_hero("Nos producteurs", "Nos producteurs", "Des producteurs passionnés par leur métier.",
                     "Au-delà des produits bio vendus en vrac, Simplement Vrac, c'est une sélection de producteurs aux parcours souvent atypiques, et à l'éthique de fabrication exigeante.") + f"""
  <section style="padding-top:clamp(1rem,3vw,2rem)">
    <div class="wrap split">
      <div class="prose reveal">
        <span class="kicker">Notre sélection</span>
        <h2>En circuit court, avec au plus un intermédiaire de confiance.</h2>
        <p>Nous sélectionnons des producteurs qui proposent des produits <strong>bons et accessibles</strong>. Bonne nouvelle : ils sont majoritairement français. Certains produisent en Île-de-France, et d'autres sont même installés à Noisy-le-Grand, comme pour le poivre de Kampot et le jus d'hibiscus pétillant.</p>
        <p>Nous visitons leurs ateliers dès que possible : la brasserie La Parisienne à Pantin, ou plus récemment l'atelier de pâtes C.Q.F.D. en Seine-et-Marne.</p>
        <p>Et plusieurs fois par an, les producteurs viennent eux-mêmes à la boutique faire déguster leurs produits et raconter leur histoire.</p>
      </div>
      <div class="split-media reveal">
        <img class="wide" src="/img/boutique/savons-arthur.jpg" alt="Les savons artisanaux Savons Arthur en boutique" loading="lazy">
        <div class="sticker" style="left:-12px;bottom:-18px"><b>Près de 30</b>artisans et producteurs</div>
      </div>
    </div>
  </section>

  <section style="padding-top:clamp(2rem,4vw,3rem)">
    <div class="wrap">
      <div class="values" style="grid-template-columns:repeat(3,1fr)">
{crits}
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="section-head reveal">
        <div><span class="kicker">Histoires de producteurs</span><h2>Ils ont toujours<br>une belle histoire.</h2></div>
        <div class="filters" role="group" aria-label="Filtrer les producteurs" data-filter-target=".pcard">
          <button class="chip" aria-pressed="true" data-f="all">Tous</button>
          <button class="chip" aria-pressed="false" data-f="idf">Île-de-France</button>
          <button class="chip" aria-pressed="false" data-f="fr">France</button>
          <button class="chip" aria-pressed="false" data-f="eq">Commerce équitable</button>
        </div>
      </div>
      <div class="pgrid">
{chr(10).join(cards)}
      </div>
      <div class="also-box reveal">
        <h3>Nouveaux venus, à découvrir en boutique</h3>
        <ul>
          <li>Une maraîchère bio de Chelles, à 5 km de Noisy-le-Grand.</li>
          <li>Les cookies de Chloé, cuits à Noisy-le-Grand.</li>
          <li>Les miels des Ruchetons, une coopérative d'apiculteurs du Sud-Ouest.</li>
          <li>Un torréfacteur local de cafés de spécialité bio.</li>
        </ul>
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="cta-band reveal">
        <h2>Vous êtes producteur ou artisan ?</h2>
        <a class="btn" href="mailto:bruno@simplement-vrac.fr?subject=Proposition%20producteur">Écrire à Bruno {I["arrow"]}</a>
      </div>
    </div>
  </section>
"""
    return page("producteurs", "Nos producteurs · Simplement Vrac", "Les producteurs bio et locaux de Simplement Vrac, à Noisy-le-Grand : leurs histoires et leurs produits.", body)

# ================================================================ LE VRAC
def vrac():
    products = ["Céréales et légumineuses", "Fruits et légumes", "Yaourts et produits laitiers", "Pâtes et farines", "Fruits secs", "Café et thé",
                "Huiles et vinaigres", "Épices", "Cosmétiques bio en circuit court", "Savons et shampoings", "Bicarbonate et entretien",
                "Gourdes, pailles, brosses", "Pains et cakes bio à la coupe"]
    chips = "".join(f"<span>{p}</span>" for p in products)
    faq = [
        ("Peut-on vraiment remplacer tous les produits du quotidien ?", "Oui, presque tous : de l'alimentaire aux produits d'hygiène, en passant par les cosmétiques. On les achète en vrac (vous apportez vos contenants), en consigne (vous rapportez les contenants fournis) ou en version réutilisable."),
        ("Faut-il tout changer d'un coup ?", "Non. Le zéro déchet est une démarche personnelle : chacun avance à son rythme, selon son organisation et ses valeurs. Certains sont passés au 100 % zéro déchet, d'autres commencent par quelques produits."),
        ("J'ai oublié mes contenants, comment faire ?", "Pas de souci : des contenants sont mis à votre disposition dans la boutique."),
        ("D'où viennent les produits ?", "Ils sont bio et de préférence régionaux. Les rares produits qui viennent de hors de l'Union européenne sont issus du commerce équitable. Chaque étiquette indique la provenance et les kilomètres parcourus."),
        ("Donnez-vous des conseils pour fabriquer ses produits soi-même ?", "Oui. Nos actualités partagent régulièrement des recettes, et nous organisons des ateliers : produits d'hygiène, cosmétiques, savon, cuisine vegan, aromathérapie…"),
    ]
    faqs = "\n".join(f'        <details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    body = page_hero("Le vrac, c'est quoi ?", "Zéro déchet", "Le vrac, c'est quoi ?",
                     "Un mode de consommation qui réduit à zéro les emballages jetables : vous ne payez que le produit. Néophyte ? Voici comment ça marche.") + f"""
  <section style="padding-top:clamp(1rem,3vw,2rem)">
    <div class="wrap split rev">
      <div class="prose reveal">
        <span class="kicker">Le concept</span>
        <h2>Une épicerie pour se faciliter la vie.</h2>
        <p>Simplement Vrac réunit des produits <strong>bio, locaux et sans emballage</strong> dans une boutique de centre-ville, avec une philosophie : le zéro déchet.</p>
        <p>Au final, vous achetez la juste quantité, vous laissez de côté les emballages superflus, et vous mangez des produits bio dont vous connaissez l'origine.</p>
        <a class="btn btn-primary" href="#gestes">Voir comment ça marche {I["arrow"]}</a>
      </div>
      <div class="split-media reveal"><img class="tall" src="/img/boutique/silos.jpg" alt="Silos de vrac dans la boutique" loading="lazy"></div>
    </div>
  </section>

{gestes_section("Cinq gestes,<br>et c'est tout.", "Vous venez avec vos contenants, ou vous empruntez les nôtres. On les pèse, vous les remplissez, on les repèse, et vous ne payez que le contenu.")}

  <section>
    <div class="wrap split">
      <div class="prose reveal">
        <span class="kicker">En rayon</span>
        <h2>Quels produits trouve-t-on en vrac ?</h2>
        <p>Des produits issus de l'agriculture biologique, de préférence régionaux, en vrac ou en contenants consignés, et bien d'autres belles découvertes.</p>
        <div class="chips-list">{chips}</div>
      </div>
      <div class="split-media reveal"><img class="wide" src="/img/boutique/cookies.jpg" alt="Bocaux de cookies et de gâteaux en vrac" loading="lazy"></div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="section-head reveal" style="justify-content:center;text-align:center">
        <div><span class="kicker">Vos questions</span><h2>Bon à savoir.</h2></div>
      </div>
      <div class="faq">
{faqs}
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="cta-band reveal">
        <h2>Prêt à essayer ? Venez avec un ou deux bocaux.</h2>
        <a class="btn" href="/contact/">Horaires et accès {I["arrow"]}</a>
      </div>
    </div>
  </section>
"""
    return page("vrac", "Le vrac, c'est quoi ? · Simplement Vrac", "Comment faire ses courses en vrac chez Simplement Vrac à Noisy-le-Grand : les gestes, les produits, vos questions.", body, patterns=True)

# ================================================================ ACTUALITÉS
def actualites():
    cards = "\n".join(post_card(p, lazy=i > 5) for i, p in enumerate(POSTS))
    body = page_hero("Actualités", "Actualités", "L'épicerie évolue constamment.",
                     "Événements, nouveautés, producteurs, recettes et bien-être : toute la vie de Simplement Vrac. Pour ne rien rater, suivez aussi nos nouvelles sur Instagram.") + f"""
  <section style="padding-top:clamp(1rem,3vw,2rem)">
    <div class="wrap">
      <div class="filters-row">
        <div class="filters" role="group" aria-label="Filtrer les actualités" data-filter-target=".posts .post">
          <button class="chip" aria-pressed="true" data-f="all">Tout</button>
          <button class="chip" aria-pressed="false" data-f="b">La boutique</button>
          <button class="chip" aria-pressed="false" data-f="p">Produits</button>
          <button class="chip" aria-pressed="false" data-f="r">Recettes & bien-être</button>
        </div>
      </div>
      <div class="posts">
{cards}
      </div>
    </div>
  </section>

{NEWSLETTER}"""
    return page("actus", "Actualités · Simplement Vrac", "Les actualités de Simplement Vrac : événements, nouveautés, producteurs et recettes.", body)

# ================================================================ CONTACT
def contact():
    body = page_hero("Nous trouver", "Nous trouver", "Passez nous voir, même sans bocal.",
                     "Votre magasin bio du centre-ville de Noisy-le-Grand, ouvert 7 jours sur 7.") + f"""
  <section style="padding-top:clamp(1rem,3vw,2rem)">
    <div class="wrap contact-grid">
      <div class="reveal">
        <div class="storefront"><img src="/img/boutique/devanture.jpg" alt="La devanture de Simplement Vrac, avec son enseigne verte" fetchpriority="high"></div>
        <div class="map"><iframe title="Simplement Vrac sur la carte" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Simplement+Vrac,+134+rue+Pierre+Brossolette,+93160+Noisy-le-Grand&output=embed"></iframe></div>
      </div>
      <div class="info-card reveal">
        <span class="kicker">Simplement Vrac</span>
        <h2>Épicerie bio, zéro déchet et locale</h2>
        <p class="addr">134, rue Pierre Brossolette<br>93160 Noisy-le-Grand</p>
        <a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">Itinéraire {I["arrow"]}</a>
{hours_table()}
        <p class="note">Les horaires peuvent changer les jours fériés et pendant les congés : nous les annonçons sur Instagram.</p>
{contact_lines()}
        <div class="socials-row">
          <a href="https://www.instagram.com/simplement_vrac" aria-label="Instagram" target="_blank" rel="noopener">{I["insta"]}</a>
          <a href="https://www.facebook.com/bruno.cuigniez" aria-label="Facebook" target="_blank" rel="noopener">{I["fb"]}</a>
          <a href="https://www.tiktok.com/@simplementvrac" aria-label="TikTok" target="_blank" rel="noopener">{I["tiktok"]}</a>
        </div>
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="svc-list">
        <div class="svc-item reveal"><div class="ico">{I["bag"]}</div><h3>Click & collect</h3><p>Commandez en ligne et récupérez vos courses en boutique.</p><a href="{ESHOP}" target="_blank" rel="noopener">Boutique en ligne →</a></div>
        <div class="svc-item reveal"><div class="ico">{I["truck"]}</div><h3>Point de livraison</h3><p>Un point de retrait aux Richardets.</p><a href="tel:+33141675365">Nous appeler →</a></div>
        <div class="svc-item reveal"><div class="ico">{I["heart"]}</div><h3>Livraison à domicile</h3><p>Pour les personnes à mobilité réduite, âgées, alitées et les femmes enceintes.</p><a href="tel:+33141675365">Nous appeler →</a></div>
      </div>
    </div>
  </section>

{NEWSLETTER}"""
    return page("contact", "Nous trouver · Simplement Vrac", "Adresse, horaires, téléphone et accès de l'épicerie Simplement Vrac à Noisy-le-Grand.", body)

# ================================================================ CRÉDITS
def credits():
    body = page_hero("Crédits photos", "Crédits", "Crédits photos.", "D'où viennent les images de ce site.") + """
  <section style="padding-top:1rem">
    <div class="wrap prose" style="max-width:760px">
      <p>Les photos de la boutique, les logos des producteurs et les images des actualités proviennent du site actuel de Simplement Vrac (simplement-vrac.fr). Certaines images d'articles sont issues de banques d'images sous licence de Simplement Vrac.</p>
      <p>La photo de Bruno est extraite d'une vidéo publiée sur le compte Instagram @simplement_vrac.</p>
      <p>Le logo est celui de Simplement Vrac.</p>
    </div>
  </section>
"""
    return page("", "Crédits photos · Simplement Vrac", "Crédits des photos du site Simplement Vrac.", body)

# ================================================================ écriture
PAGES = {
    "index.html": home,
    "notre-epicerie/index.html": epicerie,
    "nos-producteurs/index.html": producteurs,
    "le-vrac/index.html": vrac,
    "actualites/index.html": actualites,
    "contact/index.html": contact,
    "credits/index.html": credits,
}
if __name__ == "__main__":
    for path, fn in PAGES.items():
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(fn())
        print("écrit", path)
