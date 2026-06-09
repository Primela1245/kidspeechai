const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, 'blog');
const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.html') && f !== 'index.html');

const posts = [];

for (const file of files) {
  const match = file.match(/^(\d{4}-\d{2}-\d{2})-(.+)\.html$/);
  if (!match) continue;
  posts.push({ date: match[1], slug: match[2], filename: file });
}

posts.sort((a, b) => b.date.localeCompare(a.date) || b.slug.localeCompare(a.slug));

const TOPIC_META = {
  'speech-milestones-by-age':       {emoji:'\u{1F4C5}', bg:'bg-blue'},
  'when-to-see-speech-therapist':   {emoji:'\u{1FA7A}', bg:'bg-mint'},
  'articulation-development':       {emoji:'\u{1F444}', bg:'bg-pink'},
  'phonological-awareness':         {emoji:'\u{1F3B5}', bg:'bg-purple'},
  'expressive-language-development':{emoji:'\u{1F4AC}', bg:'bg-yellow'},
  'receptive-language-development': {emoji:'\u{1F442}', bg:'bg-mint'},
  'late-talkers-toddlers':          {emoji:'\u{1F331}', bg:'bg-peach'},
  'encouraging-first-words':        {emoji:'\u{1F31F}', bg:'bg-yellow'},
  'reading-aloud-benefits':         {emoji:'\u{1F4D6}', bg:'bg-peach'},
  'screen-time-and-speech':         {emoji:'\u{1F4F1}', bg:'bg-blue'},
  'vocabulary-building-games':      {emoji:'\u{1F3B2}', bg:'bg-pink'},
  'bilingual-speech-development':   {emoji:'\u{1F30E}', bg:'bg-mint'},
  'autism-speech-development':      {emoji:'\u{1F9E9}', bg:'bg-purple'},
  'apraxia-of-speech-in-kids':      {emoji:'\u{1F9E0}', bg:'bg-blue'},
  'stuttering-in-toddlers':         {emoji:'\u{1F30A}', bg:'bg-mint'},
  'tongue-tie-and-speech':          {emoji:'\u{1F445}', bg:'bg-pink'},
  'hearing-and-speech':             {emoji:'\u{1F442}', bg:'bg-yellow'},
  'sign-language-and-speech':       {emoji:'\u{1F91F}', bg:'bg-purple'},
  'play-based-speech-practice':     {emoji:'\u{1F9F8}', bg:'bg-peach'},
  'car-ride-speech-games':          {emoji:'\u{1F697}', bg:'bg-blue'},
  'mealtime-vocabulary':            {emoji:'\u{1F34E}', bg:'bg-pink'},
  'bedtime-routine-vocabulary':     {emoji:'\u{1F319}', bg:'bg-purple'},
  'early-intervention-overview':    {emoji:'\u{1F331}', bg:'bg-mint'}
};
const DEFAULT_META = {emoji:'\u{1F4AC}', bg:'bg-pink'};

function titleCase(s) {
  return s.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}
function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function formatDate(iso) {
  const d = new Date(iso + 'T12:00:00Z');
  if (isNaN(d.getTime())) return iso;
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

let postsHtml = '';
if (posts.length === 0) {
  postsHtml = '<div class="empty">No posts yet &mdash; check back soon!</div>';
} else {
  postsHtml = posts.map(p => {
    const meta = TOPIC_META[p.slug] || DEFAULT_META;
    const title = titleCase(p.slug);
    return `<a class="post-card" href="/blog/${escapeHtml(p.filename)}">
<div class="post-hero ${meta.bg}">${meta.emoji}</div>
<div class="post-body">
<div class="post-date">${escapeHtml(formatDate(p.date))}</div>
<div class="post-title">${escapeHtml(title)}</div>
<span class="post-link">Read article &rarr;</span>
</div></a>`;
  }).join('');
}

// 1. Update blog/index.html
const blogIndexPath = path.join(blogDir, 'index.html');
let blogIndexContent = fs.readFileSync(blogIndexPath, 'utf8');

const replacementRegex = /(<div id="posts" class="posts">)[\s\S]*?(<\/div>\s*<\/div>\s*<footer>)/;
if (replacementRegex.test(blogIndexContent)) {
  const newContent = blogIndexContent.replace(replacementRegex, `$1\n${postsHtml}\n$2`);
  
  // Also remove the JS fetch script
  const scriptRegex = /<script>[\s\S]*?fetch\('https:\/\/api\.github\.com[\s\S]*?<\/script>/;
  const finalContent = newContent.replace(scriptRegex, '');
  
  fs.writeFileSync(blogIndexPath, finalContent, 'utf8');
  console.log('✅ Updated blog/index.html statically.');
} else {
  console.log('⚠️ Could not find posts marker in blog/index.html');
}

// 2. Generate sitemap.xml
const sitemapPath = path.join(__dirname, 'sitemap.xml');
const BASE_URL = 'https://kidspeechai.com';

const corePages = [
  { loc: '/', changefreq: 'weekly', priority: '1.0' },
  { loc: '/privacy.html', changefreq: 'monthly', priority: '0.5' },
  { loc: '/terms.html', changefreq: 'monthly', priority: '0.5' },
  { loc: '/delete-account.html', changefreq: 'monthly', priority: '0.3' },
  { loc: '/blog/', changefreq: 'daily', priority: '0.8' },
];

let sitemapXml = '<?xml version="1.0" encoding="UTF-8"?>\n';
sitemapXml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

for (const page of corePages) {
  sitemapXml += `  <url>\n    <loc>${BASE_URL}${page.loc}</loc>\n    <changefreq>${page.changefreq}</changefreq>\n    <priority>${page.priority}</priority>\n  </url>\n`;
}

for (const post of posts) {
  sitemapXml += `  <url>\n    <loc>${BASE_URL}/blog/${post.filename}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n`;
}

sitemapXml += '</urlset>\n';

fs.writeFileSync(sitemapPath, sitemapXml, 'utf8');
console.log(`✅ Generated sitemap.xml with ${corePages.length + posts.length} URLs.`);
