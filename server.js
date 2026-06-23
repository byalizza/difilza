const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;
const ADMIN_KEY = process.env.ADMIN_KEY || 'difilza-admin-2026';

let films = [];

app.use(cors());
app.use(express.json());

app.get('/api/films', (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const search = req.query.search || '';
    const category = req.query.category || '';

    let filtered = films;

    if (search) {
        filtered = filtered.filter(f =>
            f.title.toLowerCase().includes(search.toLowerCase()) ||
            f.originalTitle.toLowerCase().includes(search.toLowerCase())
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
    res.json({ message: 'Film silindi' });
});

app.get('/api/categories', (req, res) => {
    const categories = [...new Set(films.map(f => f.category))];
    res.json(categories);
});

app.get('/', (req, res) => {
    res.json({ message: 'Difilza API calisiyor', version: '1.0.0', filmCount: films.length });
});

app.listen(PORT, () => {
    console.log(`Difilza API ${PORT} portunda calisiyor`);
});
