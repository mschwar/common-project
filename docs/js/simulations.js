// Emergent Complexity Simulations
// Conway's Game of Life (canvas-based demo)

(function() {
  const FPS = 30;
  const FRAME_TIME = 1000 / FPS;

  // ========== GAME OF LIFE ==========
  const lifeCanvas = document.getElementById('life-canvas');
  const lifeCtx = lifeCanvas.getContext('2d');
  const lifeStartBtn = document.getElementById('life-start');
  const lifeResetBtn = document.getElementById('life-reset');

  const LIFE_GRID_SIZE = 80;
  let lifeGrid, lifeNext, lifeRunning, lifeAnimId, lifeLastTime;

  function initLife() {
    lifeCanvas.width = lifeCanvas.offsetWidth;
    lifeCanvas.height = lifeCanvas.offsetHeight;
    lifeGrid = new Uint8Array(LIFE_GRID_SIZE * LIFE_GRID_SIZE);
    lifeNext = new Uint8Array(LIFE_GRID_SIZE * LIFE_GRID_SIZE);
    // Random seed
    for (let i = 0; i < lifeGrid.length; i++) {
      lifeGrid[i] = Math.random() < 0.3 ? 1 : 0;
    }
    lifeRunning = false;
    lifeLastTime = 0;
    drawLife();
  }

  function countNeighbors(x, y) {
    let count = 0;
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        if (dx === 0 && dy === 0) continue;
        const nx = (x + dx + LIFE_GRID_SIZE) % LIFE_GRID_SIZE;
        const ny = (y + dy + LIFE_GRID_SIZE) % LIFE_GRID_SIZE;
        count += lifeGrid[ny * LIFE_GRID_SIZE + nx];
      }
    }
    return count;
  }

  function stepLife() {
    for (let y = 0; y < LIFE_GRID_SIZE; y++) {
      for (let x = 0; x < LIFE_GRID_SIZE; x++) {
        const idx = y * LIFE_GRID_SIZE + x;
        const neighbors = countNeighbors(x, y);
        if (lifeGrid[idx] === 1) {
          // Alive: survive with 2-3 neighbors
          lifeNext[idx] = (neighbors === 2 || neighbors === 3) ? 1 : 0;
        } else {
          // Dead: birth with exactly 3 neighbors
          lifeNext[idx] = (neighbors === 3) ? 1 : 0;
        }
      }
    }
    [lifeGrid, lifeNext] = [lifeNext, lifeGrid];
  }

  function drawLife() {
    const cellW = lifeCanvas.width / LIFE_GRID_SIZE;
    const cellH = lifeCanvas.height / LIFE_GRID_SIZE;
    lifeCtx.fillStyle = '#fff';
    lifeCtx.fillRect(0, 0, lifeCanvas.width, lifeCanvas.height);
    lifeCtx.fillStyle = '#2f5f5a';
    for (let y = 0; y < LIFE_GRID_SIZE; y++) {
      for (let x = 0; x < LIFE_GRID_SIZE; x++) {
        if (lifeGrid[y * LIFE_GRID_SIZE + x] === 1) {
          lifeCtx.fillRect(x * cellW, y * cellH, cellW + 0.5, cellH + 0.5);
        }
      }
    }
  }

  function loopLife(timestamp) {
    if (!lifeRunning) return;
    if (timestamp - lifeLastTime >= FRAME_TIME) {
      stepLife();
      drawLife();
      lifeLastTime = timestamp;
    }
    lifeAnimId = requestAnimationFrame(loopLife);
  }

  lifeStartBtn.addEventListener('click', () => {
    if (lifeRunning) {
      lifeRunning = false;
      lifeStartBtn.textContent = 'Start';
    } else {
      lifeRunning = true;
      lifeStartBtn.textContent = 'Pause';
      lifeAnimId = requestAnimationFrame(loopLife);
    }
  });

  lifeResetBtn.addEventListener('click', () => {
    lifeRunning = false;
    lifeStartBtn.textContent = 'Start';
    cancelAnimationFrame(lifeAnimId);
    initLife();
  });

  // Initialize on load
  window.addEventListener('load', () => {
    initLife();
  });

  // Handle resize
  window.addEventListener('resize', () => {
    initLife();
  });
})();
