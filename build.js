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

function escapeXml(str) {
  return String(str || '')
    .replace(/&amp;/g, '&')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// 1. Inject / Update "Related Parent Guides & Checklists" Internal Cross-Linking Mesh across all blog posts
const pillarFilenames = [
  '2026-10-17-first-100-words-for-toddlers-parent-checklist.html',
  '2026-11-08-total-conceptual-vocabulary-for-bilingual-toddlers-counting-spanish-and-english-words.html',
  '2026-10-21-toddler-points-and-grunts-instead-of-talking-how-to-help.html',
  '2026-11-05-sequence-words-for-kids-first-next-then-last-daily-routine-storytelling-ages-2-to-7.html'
];
const postByFilename = new Map(posts.map(p => [p.filename, p]));

let crossLinkedCount = 0;
for (let i = 0; i < posts.length; i++) {
  const current = posts[i];
  const filePath = path.join(blogDir, current.filename);
  let html = fs.readFileSync(filePath, 'utf8');

  // Pick 6 unique related guides: 2 pillar guides + 4 rotating mesh neighbors so every post gets incoming links
  const related = [];
  const seen = new Set([current.filename]);

  for (const pf of pillarFilenames) {
    if (related.length >= 2) break;
    if (!seen.has(pf) && postByFilename.has(pf)) {
      related.push(postByFilename.get(pf));
      seen.add(pf);
    }
  }

  const offsets = [1, 2, 5, 11, 19, 29, 41];
  for (const off of offsets) {
    if (related.length >= 6) break;
    const candidate = posts[(i + off) % posts.length];
    if (candidate && !seen.has(candidate.filename)) {
      related.push(candidate);
      seen.add(candidate.filename);
    }
  }

  const cardsHtml = related.map(r => `      <a href="/blog/${r.filename}" style="display:block;background:#FFFFFF;border:2px solid #E2DCFF;border-radius:16px;padding:16px 18px;text-decoration:none;color:#1E243B;transition:transform 0.15s ease,box-shadow 0.15s ease;box-shadow:0 4px 12px rgba(30,36,59,0.04)">
        <div style="font-size:12.5px;font-weight:800;color:#4338CA;margin-bottom:6px">${r.emoji} ${formatDate(r.date)}</div>
        <div style="font-family:Fredoka,sans-serif;font-size:16.5px;font-weight:700;line-height:1.35;color:#1E243B;margin-bottom:6px">${r.title}</div>
        <span style="font-size:13.5px;font-weight:800;color:#4338CA">Read Guide &rarr;</span>
      </a>`).join('\n');

  const relatedSection = `<section id="related-parent-guides" class="container" style="margin-top:8px;margin-bottom:32px">
  <div style="background:#F7F4FF;border:2px solid #E2DCFF;border-radius:22px;padding:26px 24px">
    <h2 style="font-family:Fredoka,sans-serif;font-size:22px;font-weight:700;color:#1E243B;margin:0 0 6px">More Toddler Speech &amp; Vocabulary Parent Guides</h2>
    <p style="font-size:14.5px;color:#5A607F;font-weight:600;margin:0 0 18px">Explore related first-word checklists, daily play routines, and milestone guides:</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px">
${cardsHtml}
    </div>
  </div>
</section>\n\n`;

  // Remove any previous related-parent-guides section before re-inserting
  html = html.replace(/<section id="related-parent-guides"[\s\S]*?<\/section>\s*/g, '');
  if (html.includes('<footer')) {
    html = html.replace('<footer', relatedSection + '<footer');
    fs.writeFileSync(filePath, html, 'utf8');
    crossLinkedCount++;
  }
}
console.log(`✅ Injected 6-link internal SEO cross-linking mesh into ${crossLinkedCount} blog posts.`);

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
  { loc: '/', changefreq: 'weekly', priority: '1.0', hasVideo: true },
  { loc: '/blog/', changefreq: 'daily', priority: '0.9' },
  { loc: '/privacy.html', changefreq: 'monthly', priority: '0.5' },
  { loc: '/terms.html', changefreq: 'monthly', priority: '0.5' }
];

const todayIso = new Date().toISOString().split('T')[0];
let sitemapXml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n';
for (const page of corePages) {
  sitemapXml += `  <url>\n    <loc>${BASE_URL}${page.loc}</loc>\n    <lastmod>${todayIso}</lastmod>\n    <changefreq>${page.changefreq}</changefreq>\n    <priority>${page.priority}</priority>\n`;
  if (page.hasVideo) {
    sitemapXml += `    <video:video>\n      <video:thumbnail_loc>${BASE_URL}/images/demo-poster.jpg</video:thumbnail_loc>\n      <video:title>Kid Speech AI: Play &amp; Learn — Turn Screen Time &amp; Playtime Into Real Words</video:title>\n      <video:description>Watch how Kid Speech AI helps toddlers and young learners build vocabulary with pop-up image and video flashcards, custom family cards, real-time AI camera object naming, action narration, and 3D AR exercise.</video:description>\n      <video:player_loc>https://www.youtube.com/embed/db_PPy6n7H8</video:player_loc>\n      <video:publication_date>2026-10-15T00:00:00+00:00</video:publication_date>\n      <video:family_friendly>yes</video:family_friendly>\n    </video:video>\n`;
  }
  sitemapXml += `  </url>\n`;
}
for (const post of posts) {
  sitemapXml += `  <url>\n    <loc>${BASE_URL}/blog/${post.filename}</loc>\n    <lastmod>${post.date}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
}
sitemapXml += '</urlset>\n';
fs.writeFileSync(sitemapPath, sitemapXml, 'utf8');
console.log(`✅ Generated sitemap.xml with ${corePages.length + posts.length} URLs + Video Sitemap metadata.`);

// Generate rss.xml so Google Search Console rss.xml sitemap succeeds with all blog posts
const rssPath = path.join(__dirname, 'rss.xml');
const nowRfc822 = new Date().toUTCString();
let rssXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.com/2005/Atom">
  <channel>
    <title>Kid Speech AI — Toddler Vocabulary &amp; Late-Talker Parent Guides</title>
    <link>${BASE_URL}/blog/</link>
    <description>Practical, playful parent guides on helping toddlers and kids ages 2 to 7 build vocabulary at home with real-world object naming, action narration, custom family flashcards, and active screen-time routines.</description>
    <language>en-us</language>
    <lastBuildDate>${nowRfc822}</lastBuildDate>
    <atom:link href="${BASE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
`;
for (const post of posts) {
  const pubDate = new Date(post.date + 'T12:00:00Z').toUTCString();
  const postUrl = `${BASE_URL}/blog/${post.filename}`;
  rssXml += `    <item>
      <title>${escapeXml(post.title)}</title>
      <link>${postUrl}</link>
      <guid isPermaLink="true">${postUrl}</guid>
      <pubDate>${pubDate}</pubDate>
      <description>${escapeXml(post.description)}</description>
    </item>\n`;
}
rssXml += `  </channel>\n</rss>\n`;
fs.writeFileSync(rssPath, rssXml, 'utf8');
console.log(`✅ Generated rss.xml with ${posts.length} items.`);
