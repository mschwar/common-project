/**
 * Common Projects - Dynamic Entry Management
 *
 * This script handles dynamic loading and display of concept entries
 * on the homepage. It updates the progress bar and renders entry cards
 * with staggered animations.
 *
 * @module script
 * @version 1.0.0
 */

// Configuration constants
const TOTAL_CONCEPTS = 50;
const PROGRESS_ANIMATION_DELAY = 500; // milliseconds
const CARD_ANIMATION_STAGGER = 100;  // milliseconds between card animations

/**
 * Entry data structure
 * TODO: Replace with dynamic JSON loading from entries.json
 *
 * @typedef {Object} Entry
 * @property {number} day - Day number (1-50)
 * @property {string} title - Concept title
 * @property {string} theme - Thematic category
 * @property {string} file - HTML filename
 * @property {string} excerpt - Brief description
 */

/**
 * Sample entry data
 * In production, this should be loaded from a JSON file
 * generated during the build process.
 *
 * @type {Entry[]}
 */
const entries = [
    {
        day: 1,
        title: "Probability Basics",
        theme: "Statistics",
        file: "day-001-probability-basics.html",
        excerpt: "Imagine flipping a coin: it can land heads or tails, each with a 50% chance. Probability is just guessing how likely something is..."
    },
    {
        day: 2,
        title: "Bayesian Statistics",
        theme: "Statistics",
        file: "day-002-bayesian-statistics.html",
        excerpt: "It's about updating your guesses when you get new information. Like a detective gathering clues..."
    },
    {
        day: 3,
        title: "Power Laws",
        theme: "Systems",
        file: "day-003-power-laws.html",
        excerpt: "Most things are small, but a few are HUGE. This pattern appears everywhere from wealth to earthquakes..."
    },
    {
        day: 4,
        title: "Emergent Complexity",
        theme: "Systems",
        file: "day-004-emergent-complexity.html",
        excerpt: "Simple rules from individual parts create complex behavior for the whole. Like ants building colonies..."
    },
    {
        day: 5,
        title: "State Changes",
        theme: "Systems",
        file: "day-005-state-changes.html",
        excerpt: "Slow, incremental changes suddenly tip into dramatic shifts. Like ice melting or traffic jams forming..."
    }
];

/**
 * Update the progress bar to show completion percentage.
 *
 * Animates the progress bar width and updates the text display
 * with current completion statistics.
 *
 * @returns {void}
 */
function updateProgress() {
    const completed = entries.length;
    const percentage = (completed / TOTAL_CONCEPTS) * 100;

    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');

    if (!progressBar || !progressText) {
        console.error('Progress bar elements not found');
        return;
    }

    // Animate progress bar with delay for visual effect
    setTimeout(() => {
        progressBar.style.width = `${percentage}%`;
    }, PROGRESS_ANIMATION_DELAY);

    progressText.textContent = `${completed} of ${TOTAL_CONCEPTS} concepts completed (${percentage.toFixed(1)}%)`;
}

/**
 * Render entry cards to the DOM with staggered animations.
 *
 * Creates card elements for each entry, sorts them by day (newest first),
 * and adds them to the page with staggered fade-in animations.
 *
 * @returns {void}
 */
function renderEntries() {
    const entriesList = document.getElementById('entriesList');

    if (!entriesList) {
        console.error('Entries list element not found');
        return;
    }

    // Sort by day (newest first)
    const sortedEntries = [...entries].sort((a, b) => b.day - a.day);

    // Use DocumentFragment for better performance
    const fragment = document.createDocumentFragment();

    sortedEntries.forEach((entry, index) => {
        const card = createEntryCard(entry);

        // Initial state for animation
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        fragment.appendChild(card);

        // Stagger animations
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, CARD_ANIMATION_STAGGER * index);
    });

    // Single DOM update
    entriesList.appendChild(fragment);
}

/**
 * Create an entry card DOM element.
 *
 * @param {Entry} entry - Entry data object
 * @returns {HTMLAnchorElement} Configured anchor element
 */
function createEntryCard(entry) {
    const card = document.createElement('a');
    card.href = `entries/${entry.file}`;
    card.className = 'entry-card';

    card.innerHTML = `
        <div class="day">Day ${entry.day.toString().padStart(3, '0')}</div>
        <h3>${escapeHtml(entry.title)}</h3>
        <span class="theme">${escapeHtml(entry.theme)}</span>
        <p class="excerpt">${escapeHtml(entry.excerpt)}</p>
    `;

    return card;
}

/**
 * Escape HTML to prevent XSS.
 *
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Initialize the page when DOM is ready.
 *
 * Sets up progress bar and renders all entry cards.
 *
 * @returns {void}
 */
function initialize() {
    updateProgress();
    renderEntries();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initialize);
