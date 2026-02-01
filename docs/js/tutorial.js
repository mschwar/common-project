// Life Rules Interactive Playground
// Click neighbors to see how the target cell responds

(function() {
  const grid = document.querySelector('.grid-3x3');
  if (!grid) return;

  const cells = grid.querySelectorAll('.cell:not(.target)');
  const target = document.getElementById('target-cell');
  const feedback = document.getElementById('feedback-text');

  function updateTarget() {
    const neighbors = Array.from(cells).filter(c => c.classList.contains('active')).length;

    target.classList.remove('alive', 'dead');

    if (neighbors < 2) {
      target.classList.add('dead');
      target.textContent = 'Dies';
      feedback.textContent = 'Under-population: Too lonely to survive.';
    } else if (neighbors === 2) {
      target.textContent = '?';
      feedback.textContent = 'Stable: Survives if already alive, stays dead if dead.';
    } else if (neighbors === 3) {
      target.classList.add('alive');
      target.textContent = 'Lives!';
      feedback.textContent = 'Birth/Survival: Perfect balance—life thrives!';
    } else {
      target.classList.add('dead');
      target.textContent = 'Dies';
      feedback.textContent = 'Over-population: Too crowded to survive.';
    }
  }

  cells.forEach(cell => {
    cell.addEventListener('click', () => {
      cell.classList.toggle('active');
      updateTarget();
    });

    // Keyboard accessibility
    cell.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        cell.classList.toggle('active');
        updateTarget();
      }
    });
  });

  // Initial state
  updateTarget();
})();
