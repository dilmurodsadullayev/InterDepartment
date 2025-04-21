const langSelect = document.querySelector('.language-select');
  const selected = document.querySelector('.selected-lang');
  const options = document.querySelectorAll('.lang-options li');

  selected.addEventListener('click', () => {
    langSelect.classList.toggle('open');
  });

  options.forEach(option => {
    option.addEventListener('click', () => {
      selected.innerHTML = option.innerHTML;
      langSelect.classList.remove('open');
      // Tilni o‘zgartirish kodi shu yerda yoziladi
      console.log("Tanlangan til:", option.dataset.lang);
    });
  });

  document.addEventListener('click', (e) => {
    if (!langSelect.contains(e.target)) {
      langSelect.classList.remove('open');
    }
  });

  document.querySelectorAll('.faq-question').forEach(item => {
    item.addEventListener('click', () => {
      // Barcha itemlardan 'active' klassini olib tashlaymiz
      document.querySelectorAll('.faq-item').forEach(faq => {
        if (faq !== item.parentElement) {
          faq.classList.remove('active');
        }
      });

      // Tanlangan itemni almashtiramiz (toggle)
      item.parentElement.classList.toggle('active');
    });
  });
  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('navMenu');

  hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('open');
  });