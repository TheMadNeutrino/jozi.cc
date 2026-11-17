const menu = document.querySelector('.menu');
const nav = document.querySelector('.nav');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
});
document.addEventListener('keydown', e => {
  if(e.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    menu.setAttribute('aria-expanded','false'); nav.classList.remove('open'); menu.focus();
  }
});
const filters = document.querySelectorAll('.filter');
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  document.querySelectorAll('[data-category]').forEach(card => {
    card.hidden = button.dataset.filter !== 'all' && button.dataset.filter !== card.dataset.category;
  });
  const count = [...document.querySelectorAll('[data-category]')].filter(c => !c.hidden).length;
  const status = document.querySelector('#filter-status');
  if(status) status.textContent = document.documentElement.lang === 'cs' ? `Počet projektů: ${count}` : `Projects shown: ${count}`;
}));
