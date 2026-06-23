const API_URL = 'https://difilza.onrender.com';

let currentPage = 1;
let currentCategory = '';
let currentSearch = '';

async function fetchFilms(page = 1, search = '', category = '') {
    try {
        let url = `${API_URL}/api/films?page=${page}&limit=20`;
        if (search) url += `&search=${encodeURIComponent(search)}`;
        if (category) url += `&category=${encodeURIComponent(category)}`;

        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        return { films: [], total: 0, totalPages: 0 };
    }
}

function renderFilms(films) {
    const grid = document.getElementById('filmsGrid');

    if (!films.length) {
        grid.innerHTML = '<div class="loading" style="grid-column:1/-1">Film bulunamadı</div>';
        return;
    }

    grid.innerHTML = films.map(f => `
        <a href="film.html?id=${f.id}" class="film-card">
            <div class="category-badge">${f.category || 'Genel'}</div>
            <div class="poster">
                ${f.poster ? `<img src="${f.poster}" alt="${f.title}" loading="lazy">` : '🎬'}
                <div class="play-overlay"><span>▶</span></div>
            </div>
            <div class="info">
                <h3>${f.title}</h3>
                <div class="meta">
                    <span>⭐ ${f.imdb || '-'}</span>
                    <span>📅 ${f.year || '-'}</span>
                </div>
            </div>
        </a>
    `).join('');
}

function renderPagination(totalPages, current) {
    const container = document.getElementById('pagination');
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = '';
    const start = Math.max(1, current - 2);
    const end = Math.min(totalPages, current + 2);

    if (current > 1) {
        html += `<button onclick="goToPage(${current - 1})">‹</button>`;
    }

    if (start > 1) {
        html += `<button onclick="goToPage(1)">1</button>`;
        if (start > 2) html += `<button style="background:transparent;border:none;color:#555;cursor:default">...</button>`;
    }

    for (let i = start; i <= end; i++) {
        html += `<button class="${i === current ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
    }

    if (end < totalPages) {
        if (end < totalPages - 1) html += `<button style="background:transparent;border:none;color:#555;cursor:default">...</button>`;
        html += `<button onclick="goToPage(${totalPages})">${totalPages}</button>`;
    }

    if (current < totalPages) {
        html += `<button onclick="goToPage(${current + 1})">›</button>`;
    }

    container.innerHTML = html;
}

async function goToPage(page) {
    currentPage = page;
    const grid = document.getElementById('filmsGrid');
    grid.innerHTML = '<div class="loading"><div class="spinner"></div>Yükleniyor...</div>';

    const data = await fetchFilms(page, currentSearch, currentCategory);
    renderFilms(data.films);
    renderPagination(data.totalPages, page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function filterFilms() {
    const category = document.getElementById('categoryFilter').value;
    const year = document.getElementById('yearFilter').value;
    currentCategory = category;
    currentPage = 1;

    const grid = document.getElementById('filmsGrid');
    grid.innerHTML = '<div class="loading"><div class="spinner"></div>Yükleniyor...</div>';

    const data = await fetchFilms(1, currentSearch, category);
    renderFilms(data.films);
    renderPagination(data.totalPages, 1);
}

function filterByCategory(category) {
    document.getElementById('categoryFilter').value = category;
    filterFilms();
}

function searchFilms() {
    const search = document.getElementById('searchInput').value.trim();
    currentSearch = search;
    currentPage = 1;

    const grid = document.getElementById('filmsGrid');
    grid.innerHTML = '<div class="loading"><div class="spinner"></div>Film aranıyor...</div>';

    fetchFilms(1, search, currentCategory).then(data => {
        renderFilms(data.films);
        renderPagination(data.totalPages, 1);
    });
}

async function loadCategories() {
    try {
        const res = await fetch(`${API_URL}/api/films?limit=1000`);
        const data = await res.json();
        const categories = [...new Set(data.films.map(f => f.category).filter(Boolean))];
        const select = document.getElementById('categoryFilter');
        categories.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            select.appendChild(opt);
        });

        const years = [...new Set(data.films.map(f => f.year).filter(y => y))].sort((a, b) => b - a);
        const yearSelect = document.getElementById('yearFilter');
        years.forEach(y => {
            const opt = document.createElement('option');
            opt.value = y;
            opt.textContent = y;
            yearSelect.appendChild(opt);
        });
    } catch (e) {}
}

loadCategories();

fetchFilms(1, '', '').then(data => {
    renderFilms(data.films);
    renderPagination(data.totalPages, 1);
});
