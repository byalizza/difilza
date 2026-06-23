const API_URL = 'https://difilza-backend.onrender.com';

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
        console.error('Filmler yüklenirken hata:', error);
        return { films: [], total: 0, totalPages: 0 };
    }
}

async function fetchCategories() {
    try {
        const response = await fetch(`${API_URL}/api/categories`);
        return await response.json();
    } catch (error) {
        return [];
    }
}

function renderFilms(films) {
    const grid = document.getElementById('filmsGrid');

    if (!films || films.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <h2>Film bulunamadı</h2>
                <p>Henüz film eklenmemiş veya aramanız sonucu eşleşen film yok.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = films.map(film => `
        <div class="film-card" onclick="watchFilm('${film.id}')">
            <div class="poster">
                ${film.poster
                    ? `<img src="${film.poster}" alt="${film.title}" onerror="this.parentElement.innerHTML='<div class=\\'no-poster\\'>🎬</div>'">`
                    : '<div class="no-poster">🎬</div>'
                }
                <div class="play-btn"></div>
                <span class="category-badge">${film.category || 'Genel'}</span>
            </div>
            <div class="info">
                <h3>${film.title}</h3>
                <div class="meta">
                    ${film.year ? `<span>${film.year}</span>` : ''}
                    ${film.imdb ? `<span class="imdb">⭐ ${film.imdb}</span>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

function renderPagination(totalPages, currentPage) {
    const pagination = document.getElementById('pagination');

    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = '';
    html += `<button onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>Önceki</button>`;

    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            html += `<button onclick="goToPage(${i})" class="${i === currentPage ? 'active' : ''}">${i}</button>`;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            html += `<button disabled>...</button>`;
        }
    }

    html += `<button onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>Sonraki</button>`;

    pagination.innerHTML = html;
}

async function loadFilms(page = 1) {
    currentPage = page;
    const data = await fetchFilms(page, currentSearch, currentCategory);
    renderFilms(data.films);
    renderPagination(data.totalPages, page);
}

function watchFilm(id) {
    window.location.href = `film.html?id=${id}`;
}

async function searchFilms() {
    const search = document.getElementById('searchInput').value;
    currentSearch = search;
    loadFilms(1);
}

function filterByCategory(category) {
    currentCategory = category;
    document.getElementById('categoryFilter').value = category;
    loadFilms(1);
}

function filterFilms() {
    currentCategory = document.getElementById('categoryFilter').value;
    loadFilms(1);
}

function goToPage(page) {
    loadFilms(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function loadCategories() {
    const categories = await fetchCategories();
    const select = document.getElementById('categoryFilter');
    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        select.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadFilms(1);
    loadCategories();
});
