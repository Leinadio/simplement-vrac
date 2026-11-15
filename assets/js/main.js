// Simplement Vrac — scripts communs à toutes les pages

// ---------- Horaires (minutes depuis minuit) ----------
// 0 = dimanche … 6 = samedi. Lundi : 12h–19h, mardi→samedi : 10h–19h30, dimanche : 10h–13h.
const HOURS = { 0: [600, 780], 1: [720, 1140], 2: [600, 1170], 3: [600, 1170], 4: [600, 1170], 5: [600, 1170], 6: [600, 1170] };
const fmt = m => `${Math.floor(m / 60)}h${String(m % 60).padStart(2, '0')}`;
const now = new Date(), day = now.getDay(), min = now.getHours() * 60 + now.getMinutes();

const st = document.getElementById('status'), stt = document.getElementById('statusText');
if (st && stt) {
  const [o, c] = HOURS[day];
  if (min >= o && min < c) stt.textContent = `Ouvert maintenant · jusqu'à ${fmt(c)}`;
  else {
    st.classList.add('closed');
    const nextDay = min < o ? day : (day + 1) % 7;
    const label = nextDay === day ? "aujourd'hui" : 'demain';
    stt.textContent = `Fermé · ouvre ${label} à ${fmt(HOURS[nextDay][0])}`;
  }
}
document.querySelectorAll('.hours tr[data-days]').forEach(tr => {
  if (tr.dataset.days.split(',').includes(String(day))) tr.classList.add('today');
});

// ---------- Les 5 gestes du vrac ----------
const stepsEl = document.querySelectorAll('.step');
if (stepsEl.length) {
  const steps = [...stepsEl];
  const fillRect = document.getElementById('fillRect');
  const reading = document.getElementById('scaleReading');
  const caption = document.getElementById('scaleCaption');
  const ticket = document.getElementById('ticket');
  const jarG = document.getElementById('scaleJar');
  const next = document.getElementById('nextStep');
  const states = [
    { fill: 150, read: '-,--- kg', jar: 'translateY(-40px)', ticket: 0, cap: "Un bocal propre, un sac en tissu, une boîte : tout fait l'affaire." },
    { fill: 150, read: '0,350 kg', jar: 'none', ticket: 0, cap: "Le bocal vide pèse 350 g. On le note, c'est la tare." },
    { fill: 30, read: '- - -', jar: 'translateY(-40px)', ticket: 0, cap: "Remplissez au silo : une poignée, un kilo, comme vous voulez." },
    { fill: 30, read: '0,500 kg', jar: 'none', ticket: 0, cap: "850 g sur la balance, moins 350 g de bocal : 500 g de lentilles." },
    { fill: 30, read: '0,500 kg', jar: 'none', ticket: 1, cap: "Vous payez 500 g de lentilles. Le bocal, lui, rentre à la maison." },
  ];
  let cur = 0;
  const go = i => {
    cur = i;
    steps.forEach((s, j) => s.classList.toggle('on', j === i));
    const s = states[i];
    fillRect.style.transform = `translateY(${s.fill}px)`;
    reading.textContent = s.read;
    caption.textContent = s.cap;
    jarG.style.transform = s.jar;
    ticket.setAttribute('opacity', s.ticket);
    next.textContent = i === 4 ? 'Recommencer' : 'Étape suivante';
  };
  steps.forEach((s, i) => s.querySelector('button').addEventListener('click', () => go(i)));
  next.addEventListener('click', () => go((cur + 1) % 5));
  go(0);
}

// ---------- Filtres (producteurs, actualités) ----------
document.querySelectorAll('[data-filter-target]').forEach(group => {
  const items = document.querySelectorAll(group.dataset.filterTarget);
  group.querySelectorAll('.chip').forEach(chip => chip.addEventListener('click', () => {
    group.querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', c === chip));
    const f = chip.dataset.f;
    items.forEach(m => m.classList.toggle('hide', f !== 'all' && !m.dataset.f.split(' ').includes(f)));
  }));
});

// ---------- Bandeau défilant (doublé pour une boucle continue) ----------
const track = document.getElementById('track');
if (track) track.innerHTML += track.innerHTML;

// ---------- Apparitions au défilement ----------
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { threshold: .12 });
document.querySelectorAll('.reveal').forEach((el, i) => { el.style.transitionDelay = `${(i % 4) * 70}ms`; io.observe(el); });

// ---------- Navigation ----------
const nav = document.getElementById('nav');
addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 10), { passive: true });
const burger = document.getElementById('burger');
burger.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  burger.setAttribute('aria-expanded', open);
});
document.querySelectorAll('#menu a').forEach(a => a.addEventListener('click', () => {
  nav.classList.remove('open'); burger.setAttribute('aria-expanded', false);
}));

// ---------- Lettre d'information ----------
const nl = document.getElementById('nl');
if (nl) nl.addEventListener('submit', e => {
  e.preventDefault();
  const v = document.getElementById('email').value.trim();
  document.getElementById('nlMsg').textContent = /.+@.+\..+/.test(v) ? 'Merci, à très vite dans votre boîte !' : 'Il manque une adresse e-mail valide.';
});
