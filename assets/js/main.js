'use strict';
const search = document.getElementById('phrase-search');
if (search) {
  const cards = Array.from(document.querySelectorAll('.phrase-grid .searchable'));
  const status = document.getElementById('search-status');
  search.addEventListener('input', () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const matched = card.textContent.toLocaleLowerCase().includes(query);
      card.hidden = !matched;
      if (matched) visible++;
    });
    status.textContent = `找到 ${visible} 条表达 / 共 ${cards.length} 条`;
    document.getElementById('no-results').hidden = visible !== 0;
  });
}
document.querySelectorAll('.print').forEach(button => button.addEventListener('click', () => window.print()));
