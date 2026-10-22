const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, 'blog');
const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.html') && f !== 'index.html');

const posts = [];

for (const file of files) {
  const match = file.match(/^(\d{4}-\d{2}-\d{2})-(.+)\.html$/);
  if (!match) continue;
  const content = fs.readFileSync(path.join(blogDir, file), 'utf8');
  const titleMatch = content.match(/<h1 class="post-title">([\s\S]*?)<\/h1>/);
  const descMatch = content.match(/<meta name="description" content="([^"]*)"/);
  const heroMatch = content.match(/<div class="post-hero (bg-[a-z]+)"><div class="post-hero-emoji">([\s\S]*?)<\/div><\/div>/);

  posts.push({
    date: match[1],
    slug: match[2],
    filename: file,
    title: titleMatch ? titleMatch[1].trim() : match[2].replace(/-/g, ' '),
    description: descMatch ? descMatch[1].trim() : '',
    bg: heroMatch ? heroMatch[1] : 'bg-pink',
    emoji: heroMatch ? heroMatch[2].trim() : '📚'
  });
}

posts.sort((a, b) => b.date.localeCompare(a.date) || b.slug.localeCompare(a.slug));

function formatDate(iso) {
  const d = new Date(iso + 'T12:00:00Z');
  if (isNaN(d.getTime())) return iso;
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

const postsHtml = posts.map(p => `<a class="post-card" href="/blog/${p.filename}">
  <div class="post-hero ${p.bg}">${p.emoji}</div>
  <div class="post-body">
    <div class="post-date">${formatDate(p.date)}</div>
    <div class="post-title">${p.title}</div>
    <p style="font-size:14px;color:var(--text-muted);margin-bottom:10px;line-height:1.5">${p.description}</p>
    <span class="post-link">Read Parent Guide &rarr;</span>
  </div>
</a>`).join('\n');

const blogIndexPath = path.join(blogDir, 'index.html');
let blogIndexContent = fs.readFileSync(blogIndexPath, 'utf8');
const replacementRegex = /(<div id="posts" class="posts">)[\s\S]*?(<\/div>\s*<\/div>\s*<footer>)/;
if (replacementRegex.test(blogIndexContent)) {
  const newContent = blogIndexContent.replace(replacementRegex, `$1\n${postsHtml}\n$2`);
  fs.writeFileSync(blogIndexPath, newContent, 'utf8');
  console.log('✅ Updated blog/index.html statically.');
}

const sitemapPath = path.join(__dirname, 'sitemap.xml');
const BASE_URL = 'https://kidspeechai.com';
const corePages = [
  { loc: '/', changefreq: 'weekly', priority: '1.0' },
  { loc: '/blog/', changefreq: 'daily', priority: '0.9' },
  { loc: '/privacy.html', changefreq: 'monthly', priority: '0.5' },
  { loc: '/terms.html', changefreq: 'monthly', priority: '0.5' }
];

const todayIso = new Date().toISOString().split('T')[0];
let sitemapXml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
for (const page of corePages) {
  sitemapXml += `  <url>\n    <loc>${BASE_URL}${page.loc}</loc>\n    <lastmod>${todayIso}</lastmod>\n    <changefreq>${page.changefreq}</changefreq>\n    <priority>${page.priority}</priority>\n  </url>\n`;
}
for (const post of posts) {
  sitemapXml += `  <url>\n    <loc>${BASE_URL}/blog/${post.filename}</loc>\n    <lastmod>${post.date}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
}
sitemapXml += '</urlset>\n';
fs.writeFileSync(sitemapPath, sitemapXml, 'utf8');
console.log(`✅ Generated sitemap.xml with ${corePages.length + posts.length} URLs.`);
