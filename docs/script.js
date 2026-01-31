document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('concept-container');

    fetch('concepts.json')
        .then(response => {
            if (!response.ok) throw new Error('Failed to load concepts');
            return response.json();
        })
        .then(concepts => {
            const today = new Date();
            const startOfYear = new Date(today.getFullYear(), 0, 0);
            const dayOfYear = Math.floor((today - startOfYear) / 86400000);
            const index = dayOfYear % concepts.length;
            const concept = concepts[index];

            container.innerHTML = `
                <h1 class="concept-title">${escapeHtml(concept.concept_title)}</h1>

                <div class="section">
                    <p class="section-content">${escapeHtml(concept.kindergarten_explanation)}</p>
                </div>

                <div class="section">
                    <p class="section-label">Why It Matters</p>
                    <p class="section-content">${escapeHtml(concept.why_it_matters)}</p>
                </div>

                <div class="section">
                    <p class="section-label">Connections</p>
                    <div class="section-content">
                        <ul>${concept.connections_unlocked.map(c => `<li>${escapeHtml(c)}</li>`).join('')}</ul>
                    </div>
                </div>

                <div class="section">
                    <p class="section-label">Try This</p>
                    <p class="section-content">${escapeHtml(concept.quick_exercise)}</p>
                </div>

                <p class="day-indicator">Day ${concept.day} of ${concepts.length}</p>
            `;
        })
        .catch(() => {
            container.innerHTML = '<p class="loading">Unable to load today\'s concept. Please try again later.</p>';
        });
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
