function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Cambiar icono del botón si existe
    const btn = document.getElementById('themeBtn');
    if(btn) btn.innerText = newTheme === 'light' ? '🌙' : '☀️';
}

// Cargar preferencia al iniciar
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
});

//Developer: Jhonn Pether