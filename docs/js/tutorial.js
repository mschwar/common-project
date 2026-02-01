// Interactive 9x9 Lab Sandboxes
// Ant Lab: Langton's Ant step-by-step
// Life Lab: Game of Life step-by-step

(function() {
  const SIZE = 9;

  // ========== ANT LAB ==========
  const antLabEl = document.getElementById('ant-lab');
  const antStepBtn = document.getElementById('ant-step');
  const antClearBtn = document.getElementById('ant-clear');

  let antGrid = new Uint8Array(SIZE * SIZE);
  let antX = Math.floor(SIZE / 2);
  let antY = Math.floor(SIZE / 2);
  let antDir = 0; // 0=up, 1=right, 2=down, 3=left

  function buildAntGrid() {
    antLabEl.innerHTML = '';
    for (let i = 0; i < SIZE * SIZE; i++) {
      const cell = document.createElement('div');
      cell.className = 'lab-cell';
      cell.dataset.index = i;
      cell.addEventListener('click', () => toggleAntCell(i));
      antLabEl.appendChild(cell);
    }
    renderAnt();
  }

  function toggleAntCell(idx) {
    antGrid[idx] = antGrid[idx] ? 0 : 1;
    renderAnt();
  }

  function renderAnt() {
    const cells = antLabEl.querySelectorAll('.lab-cell');
    cells.forEach((cell, i) => {
      cell.classList.remove('active', 'ant');
      if (antGrid[i] === 1) cell.classList.add('active');
      if (i === antY * SIZE + antX) cell.classList.add('ant');
    });
  }

  function stepAnt() {
    const idx = antY * SIZE + antX;
    if (antGrid[idx] === 0) {
      antDir = (antDir + 1) % 4; // Turn right on white
      antGrid[idx] = 1;
    } else {
      antDir = (antDir + 3) % 4; // Turn left on black
      antGrid[idx] = 0;
    }
    // Move forward with wrapping
    if (antDir === 0) antY = (antY - 1 + SIZE) % SIZE;
    else if (antDir === 1) antX = (antX + 1) % SIZE;
    else if (antDir === 2) antY = (antY + 1) % SIZE;
    else antX = (antX - 1 + SIZE) % SIZE;
    renderAnt();
  }

  function resetAnt() {
    antGrid = new Uint8Array(SIZE * SIZE);
    antX = Math.floor(SIZE / 2);
    antY = Math.floor(SIZE / 2);
    antDir = 0;
    renderAnt();
  }

  antStepBtn.addEventListener('click', stepAnt);
  antClearBtn.addEventListener('click', resetAnt);

  // ========== LIFE LAB ==========
  const lifeLabEl = document.getElementById('life-lab');
  const lifeStepBtn = document.getElementById('life-step');
  const lifeClearBtn = document.getElementById('life-clear');

  let lifeGrid = new Uint8Array(SIZE * SIZE);

  function buildLifeGrid() {
    lifeLabEl.innerHTML = '';
    for (let i = 0; i < SIZE * SIZE; i++) {
      const cell = document.createElement('div');
      cell.className = 'lab-cell';
      cell.dataset.index = i;
      cell.addEventListener('click', () => toggleLifeCell(i));
      lifeLabEl.appendChild(cell);
    }
    renderLife();
  }

  function toggleLifeCell(idx) {
    lifeGrid[idx] = lifeGrid[idx] ? 0 : 1;
    renderLife();
  }

  function renderLife() {
    const cells = lifeLabEl.querySelectorAll('.lab-cell');
    cells.forEach((cell, i) => {
      cell.classList.remove('alive');
      if (lifeGrid[i] === 1) cell.classList.add('alive');
    });
  }

  function countLifeNeighbors(x, y) {
    let count = 0;
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        if (dx === 0 && dy === 0) continue;
        const nx = (x + dx + SIZE) % SIZE;
        const ny = (y + dy + SIZE) % SIZE;
        count += lifeGrid[ny * SIZE + nx];
      }
    }
    return count;
  }

  function stepLife() {
    const next = new Uint8Array(SIZE * SIZE);
    for (let y = 0; y < SIZE; y++) {
      for (let x = 0; x < SIZE; x++) {
        const idx = y * SIZE + x;
        const neighbors = countLifeNeighbors(x, y);
        if (lifeGrid[idx] === 1) {
          next[idx] = (neighbors === 2 || neighbors === 3) ? 1 : 0;
        } else {
          next[idx] = (neighbors === 3) ? 1 : 0;
        }
      }
    }
    lifeGrid = next;
    renderLife();
  }

  function clearLife() {
    lifeGrid = new Uint8Array(SIZE * SIZE);
    renderLife();
  }

  lifeStepBtn.addEventListener('click', stepLife);
  lifeClearBtn.addEventListener('click', clearLife);

  // Initialize both grids on load
  window.addEventListener('DOMContentLoaded', () => {
    buildAntGrid();
    buildLifeGrid();
  });
})();
