// Emergent Complexity Simulations
// Langton's Ant and Conway's Game of Life

(function() {
  const FPS = 30;
  const FRAME_TIME = 1000 / FPS;

  // ========== LANGTON'S ANT ==========
  const antCanvas = document.getElementById('ant-canvas');
  const antCtx = antCanvas.getContext('2d');
  const antStartBtn = document.getElementById('ant-start');
  const antResetBtn = document.getElementById('ant-reset');

  const ANT_GRID_SIZE = 100;
  let antGrid, antX, antY, antDir, antRunning, antAnimId, antLastTime;

  function initAnt() {
    antCanvas.width = antCanvas.offsetWidth;
    antCanvas.height = antCanvas.offsetHeight;
    antGrid = new Uint8Array(ANT_GRID_SIZE * ANT_GRID_SIZE);
    antX = Math.floor(ANT_GRID_SIZE / 2);
    antY = Math.floor(ANT_GRID_SIZE / 2);
    antDir = 0; // 0=up, 1=right, 2=down, 3=left
    antRunning = false;
    antLastTime = 0;
    drawAnt();
  }

  function stepAnt() {
    const idx = antY * ANT_GRID_SIZE + antX;
    if (antGrid[idx] === 0) {
      antDir = (antDir + 1) % 4; // Turn right on white
      antGrid[idx] = 1;
    } else {
      antDir = (antDir + 3) % 4; // Turn left on black
      antGrid[idx] = 0;
    }
    // Move forward
    if (antDir === 0) antY = (antY - 1 + ANT_GRID_SIZE) % ANT_GRID_SIZE;
    else if (antDir === 1) antX = (antX + 1) % ANT_GRID_SIZE;
    else if (antDir === 2) antY = (antY + 1) % ANT_GRID_SIZE;
    else antX = (antX - 1 + ANT_GRID_SIZE) % ANT_GRID_SIZE;
  }

  function drawAnt() {
    const cellW = antCanvas.width / ANT_GRID_SIZE;
    const cellH = antCanvas.height / ANT_GRID_SIZE;
    antCtx.fillStyle = '#fff';
    antCtx.fillRect(0, 0, antCanvas.width, antCanvas.height);
    antCtx.fillStyle = '#1c1b1a';
    for (let y = 0; y < ANT_GRID_SIZE; y++) {
      for (let x = 0; x < ANT_GRID_SIZE; x++) {
        if (antGrid[y * ANT_GRID_SIZE + x] === 1) {
          antCtx.fillRect(x * cellW, y * cellH, cellW + 0.5, cellH + 0.5);
        }
      }
    }
    // Draw ant
    antCtx.fillStyle = '#e74c3c';
    antCtx.fillRect(antX * cellW, antY * cellH, cellW + 0.5, cellH + 0.5);
  }

  function loopAnt(timestamp) {
    if (!antRunning) return;
    if (timestamp - antLastTime >= FRAME_TIME) {
      for (let i = 0; i < 10; i++) stepAnt(); // Multiple steps per frame for speed
      drawAnt();
      antLastTime = timestamp;
    }
    antAnimId = requestAnimationFrame(loopAnt);
  }

  antStartBtn.addEventListener('click', () => {
    if (antRunning) {
      antRunning = false;
      antStartBtn.textContent = 'Start';
    } else {
      antRunning = true;
      antStartBtn.textContent = 'Pause';
      antAnimId = requestAnimationFrame(loopAnt);
    }
  });

  antResetBtn.addEventListener('click', () => {
    antRunning = false;
    antStartBtn.textContent = 'Start';
    cancelAnimationFrame(antAnimId);
    initAnt();
  });

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

  // Initialize both on load
  window.addEventListener('load', () => {
    initAnt();
    initLife();
  });

  // Handle resize
  window.addEventListener('resize', () => {
    initAnt();
    initLife();
  });
})();
