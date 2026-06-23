const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const https = require('https');

const app = express();
const PORT = process.env.PORT || 3000;
const ADMIN_KEY = process.env.ADMIN_KEY || '123456';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '';
const GITHUB_REPO = process.env.GITHUB_REPO || 'byalizza/difilza';
const GITHUB_FILE = 'films.json';
const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'main';

let films = [];
let lastCommitSha = null;
let saveTimeout = null;

app.use(cors());
app.use(express.json({ limit: '10mb' }));

function githubRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'api.github.com',
            path: `/repos/${GITHUB_REPO}${path}`,
            method: method,
            headers: {
                'User-Agent': 'Difilza-Backend',
                'Authorization': `token ${GITHUB_TOKEN}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    resolve({ status: res.statusCode, data: JSON.parse(body) });
                } catch (e) {
                    resolve({ status: res.statusCode, data: body });
                }
            });
        });

        req.on('error', reject);
        if (data) req.write(JSON.stringify(data));
        req.end();
    });
}

async function loadFilmsFromGitHub() {
    if (!GITHUB_TOKEN) {
        console.log('GITHUB_TOKEN tanimli degil, bos basliyor');
        return;
    }

    try {
        const res = await githubRequest('GET', `/contents/${GITHUB_FILE}?ref=${GITHUB_BRANCH}`);
        if (res.status === 200 && res.data.content) {
            const content = Buffer.from(res.data.content, 'base64').toString('utf-8');
            films = JSON.parse(content);
            lastCommitSha = res.data.sha;
            console.log(`GitHub'dan ${films.length} film yuklendi`);
        } else {
            console.log('GitHub dosyasi bulunamadi, bos basliyor');
            films = [];
        }
    } catch (e) {
        console.log('GitHub yukleme hatasi:', e.message);
        films = [];
    }
}

async function saveFilmsToGitHub() {
    if (!GITHUB_TOKEN) return;

    try {
        const content = Buffer.from(JSON.stringify(films, null, 2)).toString('base64');

        const data = {
            message: `Films updated (${films.length} films)`,
            content: content,
            branch: GITHUB_BRANCH
        };

        if (lastCommitSha) {
            data.sha = lastCommitSha;
        }

        const res = await githubRequest('PUT', `/contents/${GITHUB_FILE}`, data);
        if (res.status === 200 || res.status === 201) {
            lastCommitSha = res.data.content.sha;
            console.log('GitHub kaydedildi');
        } else {
            console.log('GitHub kayit hatasi:', res.data);
        }
    } catch (e) {
        console.log('GitHub kayit hatasi:', e.message);
    }
}

function scheduleSave() {
    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(async () => {
        await saveFilmsToGitHub();
    }, 2000);
}

app.get('/api/films', (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const search = req.query.search || '';
    const category = req.query.category || '';

    let filtered = films;

    if (search) {
        filtered = filtered.filter(f =>
            f.title.toLowerCase().includes(search.toLowerCase()) ||
            (f.originalTitle && f.originalTitle.toLowerCase().includes(search.toLowerCase()))
        );
    }

    if (category) {
        filtered = filtered.filter(f => f.category === category);
    }

    const total = filtered.length;
    const start = (page - 1) * limit;
    const end = start + limit;
    const paged = filtered.slice(start, end);

    res.json({
        films: paged,
        total,
        page,
        totalPages: Math.ceil(total / limit)
    });
});

app.get('/api/films/:id', (req, res) => {
    const film = films.find(f => f.id === req.params.id);
    if (!film) {
        return res.status(404).json({ error: 'Film bulunamadi' });
    }
    res.json(film);
});

app.get('/api/films/:id/embed', (req, res) => {
    const film = films.find(f => f.id === req.params.id);
    if (!film) {
        return res.status(404).json({ error: 'Film bulunamadi' });
    }
    res.json({ embedUrl: film.embedUrl });
});

app.post('/api/films', (req, res) => {
    const key = req.headers['x-admin-key'];
    if (key !== ADMIN_KEY) {
        return res.status(401).json({ error: 'Yetkisiz erisim' });
    }

    const { title, originalTitle, embedUrl, poster, category, year, imdb, description } = req.body;

    if (!title || !embedUrl) {
        return res.status(400).json({ error: 'Film adi ve embed linki zorunludur' });
    }

    const newFilm = {
        id: uuidv4(),
        title,
        originalTitle: originalTitle || '',
        embedUrl,
        poster: poster || '',
        category: category || 'Genel',
        year: year || '',
        imdb: imdb || '',
        description: description || '',
        createdAt: new Date().toISOString()
    };

    films.unshift(newFilm);
    scheduleSave();
    res.status(201).json(newFilm);
});

app.put('/api/films/:id', (req, res) => {
    const key = req.headers['x-admin-key'];
    if (key !== ADMIN_KEY) {
        return res.status(401).json({ error: 'Yetkisiz erisim' });
    }

    const index = films.findIndex(f => f.id === req.params.id);

    if (index === -1) {
        return res.status(404).json({ error: 'Film bulunamadi' });
    }

    const { title, originalTitle, embedUrl, poster, category, year, imdb, description } = req.body;

    films[index] = {
        ...films[index],
        title: title || films[index].title,
        originalTitle: originalTitle || films[index].originalTitle,
        embedUrl: embedUrl || films[index].embedUrl,
        poster: poster || films[index].poster,
        category: category || films[index].category,
        year: year || films[index].year,
        imdb: imdb || films[index].imdb,
        description: description || films[index].description,
        updatedAt: new Date().toISOString()
    };

    scheduleSave();
    res.json(films[index]);
});

app.delete('/api/films/:id', (req, res) => {
    const key = req.headers['x-admin-key'];
    if (key !== ADMIN_KEY) {
        return res.status(401).json({ error: 'Yetkisiz erisim' });
    }

    const index = films.findIndex(f => f.id === req.params.id);

    if (index === -1) {
        return res.status(404).json({ error: 'Film bulunamadi' });
    }

    films.splice(index, 1);
    scheduleSave();
    res.json({ message: 'Film silindi' });
});

app.post('/api/films/bulk', (req, res) => {
    const key = req.headers['x-admin-key'];
    if (key !== ADMIN_KEY) {
        return res.status(401).json({ error: 'Yetkisiz erisim' });
    }

    const { films: newFilms } = req.body;

    if (!Array.isArray(newFilms) || newFilms.length === 0) {
        return res.status(400).json({ error: 'Film listesi bos olamaz' });
    }

    let added = 0;
    let skipped = 0;

    for (const film of newFilms) {
        if (!film.title || !film.embedUrl) {
            skipped++;
            continue;
        }

        const exists = films.some(f =>
            f.title.toLowerCase() === film.title.toLowerCase()
        );

        if (exists) {
            skipped++;
            continue;
        }

        films.unshift({
            id: uuidv4(),
            title: film.title,
            originalTitle: film.originalTitle || '',
            embedUrl: film.embedUrl,
            poster: film.poster || '',
            category: film.category || 'Genel',
            year: film.year || '',
            imdb: film.imdb || '',
            description: film.description || '',
            createdAt: new Date().toISOString()
        });
        added++;
    }

    if (added > 0) scheduleSave();

    res.json({
        message: `${added} film eklendi, ${skipped} atlandi`,
        added,
        skipped,
        total: films.length
    });
});

app.get('/api/categories', (req, res) => {
    const categories = [...new Set(films.map(f => f.category))];
    res.json(categories);
});

app.get('/', (req, res) => {
    res.json({
        message: 'Difilza API calisiyor',
        version: '2.0.0',
        filmCount: films.length,
        storage: GITHUB_TOKEN ? 'GitHub JSON' : 'In-Memory'
    });
});

app.listen(PORT, async () => {
    console.log(`Difilza API ${PORT} portunda calisiyor`);
    await loadFilmsFromGitHub();
});
