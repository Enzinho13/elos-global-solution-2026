'use strict';
// Fotos externas podem falhar; mantém o carrossel visível com foto local.
const fallbackPhoto = document.querySelector('.hero-image')?.getAttribute('src') || 'img/logo-elos.jpeg';
document.querySelectorAll('.hero-image, .photo-slide img, .audience-photo img').forEach((photo) => {
  const useFallback = () => {
    if (!photo.getAttribute('src').endsWith(fallbackPhoto)) {
      photo.src = fallbackPhoto;
      photo.alt = 'Frutas e verduras expostas em um mercado';
    }
  };
  photo.addEventListener('error', useFallback);
  if (photo.complete && photo.naturalWidth === 0) useFallback();
});

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.site-nav');

if (menuButton && navigation) {
  menuButton.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!expanded));
    menuButton.setAttribute('aria-label', expanded ? 'Abrir menu' : 'Fechar menu');
    navigation.classList.toggle('is-open', !expanded);
  });
  navigation.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Abrir menu');
  }));
}

const slides = [...document.querySelectorAll('.photo-slide')];
const slideStatus = document.getElementById('slide-status');
let activeSlide = 0;
function showSlide(index) {
  if (!slides.length) return;
  activeSlide = (index + slides.length) % slides.length;
  slides.forEach((slide, i) => slide.classList.toggle('is-active', i === activeSlide));
  if (slideStatus) slideStatus.textContent = `${String(activeSlide + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
}
const previous = document.getElementById('slide-prev');
const next = document.getElementById('slide-next');
if (previous) previous.addEventListener('click', () => showSlide(activeSlide - 1));
if (next) next.addEventListener('click', () => showSlide(activeSlide + 1));

const form = document.getElementById('interest-form');
const response = document.getElementById('form-response');
if (form && response) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const comercio = form.elements.comercio;
    const bairro = form.elements.bairro;
    const caixas = form.elements.caixas;
    const produto = form.elements.produto;
    const fields = [comercio, bairro, caixas, produto];
    fields.forEach((field) => field.removeAttribute('aria-invalid'));
    const invalid = fields.filter((field) => !field.value.trim());
    if (invalid.length) {
      invalid.forEach((field) => field.setAttribute('aria-invalid', 'true'));
      response.className = 'form-response error';
      response.textContent = 'Preencha todos os campos para simular seu pedido.';
      invalid[0].focus();
      return;
    }
    if (!/\p{L}/u.test(produto.value) || !Number.isInteger(Number(caixas.value)) || Number(caixas.value) < 1) {
      response.className = 'form-response error';
      response.textContent = 'Informe o nome de um produto e uma quantidade inteira maior que zero.';
      return;
    }
    response.className = 'form-response';
    response.textContent = `Simulação criada: ${caixas.value} caixa(s) de ${produto.value.trim()} para ${comercio.value.trim()}, em ${bairro.value}. Nenhum dado foi enviado.`;
    form.reset();
  });
}

const fotoReservaElos = 'https://images.unsplash.com/photo-1542838132-92c53300491e?fit=crop&w=900&q=75';

document.querySelectorAll('.photo-slide img').forEach(img => {
    img.addEventListener('error', () => {
        if (img.src !== fotoReservaElos) {
            img.src = fotoReservaElos;
        }
    });
    if (img.complete && img.naturalWidth === 0) {
        img.src = fotoReservaElos;
    }
});

/* Revisao FIAP - secao atual */
const linksElos = [...document.querySelectorAll('.site-nav a[href^="#"]')];

const observadorElos = new IntersectionObserver((entries) => {
    for (const entry of entries) {
        if (!entry.isIntersecting) continue;

        linksElos.forEach((link) => {
            if (link.getAttribute('href') === '#' + entry.target.id) {
                link.setAttribute('aria-current', 'location');
            } else {
                link.removeAttribute('aria-current');
            }
        });
    }
}, {
    rootMargin: '-15% 0px -65% 0px'
});

document.querySelectorAll('main > section[id]').forEach(
    (section) => observadorElos.observe(section)
);
