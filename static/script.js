document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generate-form');
    const loading = document.getElementById('loading');

    form.addEventListener('submit', function() {
        loading.style.display = 'flex';
    });
});
