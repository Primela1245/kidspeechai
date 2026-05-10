// Mobile nav toggle
const toggle = document.getElementById('mobile-toggle');
const nav = document.getElementById('main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    nav.classList.toggle('active');
    toggle.setAttribute('aria-expanded', nav.classList.contains('active'));
  });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id.length > 1) {
      e.preventDefault();
      const el = document.querySelector(id);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (nav && nav.classList.contains('active')) nav.classList.remove('active');
    }
  });
});

// Scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.stat-card, .feature-card, .step-card, .pledge-card, .faq-item-home, .glass-feature, .post-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});

// Hero particles
const particleContainer = document.getElementById('hero-particles');
if (particleContainer) {
  const colors = ['#8b5cf6', '#06d6a0', '#ec4899', '#f97316'];
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 6 + 2;
    p.style.width = size + 'px';
    p.style.height = size + 'px';
    p.style.left = Math.random() * 100 + '%';
    p.style.top = (60 + Math.random() * 40) + '%';
    p.style.background = colors[Math.floor(Math.random() * colors.length)];
    p.style.animationDuration = (6 + Math.random() * 10) + 's';
    p.style.animationDelay = (Math.random() * 8) + 's';
    particleContainer.appendChild(p);
  }
}

// Header scroll effect
const header = document.getElementById('site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.style.borderBottomColor = window.scrollY > 50 ? 'rgba(139,92,246,0.2)' : '';
  });
}
