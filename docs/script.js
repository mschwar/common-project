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
 * Entry data (loaded from docs/entries.json)
 *
 * @type {Entry[]}
 */
let entries = [];

/**
 * Load entry data from entries.json.
 *
 * @returns {Promise<void>}
 */
async function loadEntries() {
    const response = await fetch('entries.json', { cache: 'no-store' });
    if (!response.ok) {
        throw new Error(`Failed to load entries.json (${response.status})`);
    }
    entries = await response.json();
}

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

    const progressText = document.getElementById('progressText');

    if (!progressText) {
        console.error('Progress bar elements not found');
        return;
    }

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

    const fragment = document.createDocumentFragment();

    sortedEntries.forEach((entry) => {
        const item = createEntryItem(entry);
        fragment.appendChild(item);
    });

    entriesList.appendChild(fragment);
}

/**
 * Create an entry card DOM element.
 *
 * @param {Entry} entry - Entry data object
 * @returns {HTMLAnchorElement} Configured anchor element
 */
function createEntryItem(entry) {
    const item = document.createElement('li');
    item.className = 'entry-item';

    const day = entry.day.toString().padStart(3, '0');

    item.innerHTML = `
        <div class="entry-meta">Day ${day} • ${escapeHtml(entry.theme)}</div>
        <div class="entry-title"><a href="entries/${entry.file}">${escapeHtml(entry.title)}</a></div>
        <div class="entry-excerpt">${escapeHtml(entry.excerpt)}</div>
    `;

    return item;
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
async function initialize() {
    try {
        await loadEntries();
        updateProgress();
        renderEntries();
    } catch (error) {
        console.error('Failed to initialize entries:', error);
        const progressText = document.getElementById('progressText');
        if (progressText) {
            progressText.textContent = 'Unable to load entries.';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initialize);
