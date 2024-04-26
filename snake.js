const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const blockSize = 20;
let snake = [{ x: 10, y: 10 }];
let food = { x: 15, y: 10 };
let dx = 1;
let dy = 0;
let score = 0;
let isGameOver = false;
let gameLoop; 

function drawBlock(x, y) {
  ctx.fillStyle = "green";
  ctx.fillRect(x * blockSize, y * blockSize, blockSize, blockSize);
  ctx.strokeStyle = "black";
  ctx.strokeRect(x * blockSize, y * blockSize, blockSize, blockSize);
}

function drawSnake() {
  snake.forEach(segment => drawBlock(segment.x, segment.y));
}

function drawFood() {
  drawBlock(food.x, food.y);
}

function moveSnake() {
  const head = { x: snake[0].x + dx, y: snake[0].y + dy };
  snake.unshift(head);
  if (head.x === food.x && head.y === food.y) {
    score += 10;
    document.getElementById("score").innerText = score;
    generateFood();
  } else {
    snake.pop();
  }
}

function generateFood() {
  food.x = Math.floor(Math.random() * (canvas.width / blockSize));
  food.y = Math.floor(Math.random() * (canvas.height / blockSize));
  snake.forEach(segment => {
    if (food.x === segment.x && food.y === segment.y) {
      generateFood();
    }
  });
}


function loadAndDisplayScore() {
  var savedScore = localStorage.getItem('savedScore');
  if (!savedScore || score > parseInt(savedScore)) {
    // Aggiorniamo lo score salvato
    localStorage.setItem('savedScore', score);
  }
  // Recuperiamo lo score salvato dal localStorage
  var savedScore = localStorage.getItem('savedScore');
  // Verifichiamo se lo score è stato salvato precedentemente
  if (savedScore) {
    // Aggiorniamo l'elemento h1 sulla pagina di gioco con lo score salvato
    document.getElementById("bscore").innerText =savedScore;
  }
}



function loadAndDisplayBestScores() {
  // Recuperiamo i migliori punteggi salvati dal localStorage (supponiamo che sia una lista di oggetti {player: "Nome", score: valore})

  var table = document.getElementById("table");

  // Array per contenere i valori della seconda colonna
  var values = [];

  // Iteriamo sulle righe della tabella (escludendo l'intestazione)
  for (var i = 1; i < table.rows.length; i++) {
    // Accediamo alle celle nella prima e nella seconda colonna di ciascuna riga
    var playerNameCell = table.rows[i].cells[0];
    var scoreCell = table.rows[i].cells[1];
    
    // Aggiungiamo il nome del giocatore e il punteggio all'array
    var playerName = playerNameCell.textContent || playerNameCell.innerText;
    var score = parseInt(scoreCell.textContent || scoreCell.innerText);
    values.push({ player: playerName, score: score });
  }

  var newPlayerName = document.getElementById("NamePlayer").textContent;
  var newScore = parseInt(document.getElementById("bscore").textContent);
  new_table={ player: newPlayerName, score: newScore };
  tmp=containsValueInArrayOfObjects(values, 'player', newPlayerName)
  if(tmp==false){
    values.push(new_table)
    console.log("fds".values);
  }else{
    if(values[tmp][score]<newScore){
      values[tmp][score]=newScore
      sortByKey(values, 'score');
      console.log("das".values);
    }else{
      console.log("ok".values);
      return;
      
    }
  } 
   
  console.log(values);
  updateLeaderboardHTML(values);
}

function updateLeaderboardHTML(values) {
  var tbody = document.querySelector('#table tbody');
  tbody.innerHTML = ''; // Pulisce il contenuto attuale della tabella

  // Itera attraverso l'array di punteggi e crea una nuova riga per ogni elemento
  values.forEach(function(entry) {
      var row = document.createElement('tr');
      var playerNameCell = document.createElement('td');
      playerNameCell.textContent = entry.player;
      var scoreCell = document.createElement('td');
      scoreCell.textContent = entry.score;

      row.appendChild(playerNameCell);
      row.appendChild(scoreCell);
      tbody.appendChild(row);
  });
}


function sortByKey(arr, key) {
  arr.sort(function(a, b) {
      var valueA = a[key];
      var valueB = b[key];
      if (valueA < valueB) {
          return -1;
      }
      if (valueA > valueB) {
          return 1;
      }
      return 0;
  });
}

function containsValueInArrayOfObjects(arr, key, value) {
  for (var i = 0; i < arr.length; i++) {
      if (arr[i][key] === value) {
          return i;
      }
  }
  return false;
}














function saveScoreAndPlayerToBestScores(player, score) {
  // Recuperiamo i migliori punteggi salvati dal localStorage
  var bestScores = JSON.parse(localStorage.getItem('bestScores')) || [];
  // Aggiungiamo il nuovo punteggio e il giocatore alla lista dei migliori punteggi
  bestScores.push({ player: player, score: score });
  // Salviamo la lista aggiornata dei migliori punteggi nel localStorage
  localStorage.setItem('bestScores', JSON.stringify(bestScores));
}


function checkCollision() {
  const head = snake[0];
  if (head.x < 0 || head.x >= canvas.width / blockSize || head.y < 0 || head.y >= canvas.height / blockSize) {
    gameOver();
  }
  for (let i = 1; i < snake.length; i++) {
    if (head.x === snake[i].x && head.y === snake[i].y) {
      gameOver();
    }
  }
}

function gameOver() {
  isGameOver = true;
  clearInterval(gameLoop);
  document.getElementById("gameOverText").innerText = "Game Over! Your score: " + score;
  document.getElementById("score").innerText = "0";

  loadAndDisplayScore();
  loadAndDisplayBestScores();

}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function updateGame() {
  if (isGameOver) return;
  clearCanvas();
  drawSnake();
  drawFood();
  moveSnake();
  checkCollision();
  
}

function keyDownHandler(event) {
  const keyPressed = event.key;
  if (keyPressed === "ArrowUp" && dy === 0) {
    dx = 0;
    dy = -1;
  } else if (keyPressed === "ArrowDown" && dy === 0) {
    dx = 0;
    dy = 1;
  } else if (keyPressed === "ArrowLeft" && dx === 0) {
    dx = -1;
    dy = 0;
  } else if (keyPressed === "ArrowRight" && dx === 0) {
    dx = 1;
    dy = 0;
  }
}
// Funzione per gestire gli eventi touch su un elemento
function handleTouch(elementId, callback) {
  const element = document.getElementById(elementId);
  element.addEventListener('touchstart', function(event) {
    event.preventDefault(); // Evita il comportamento predefinito del touch (es. lo zoom)
    callback();
  });
}

// Gestione degli eventi touch per i controlli del serpente
handleTouch('up-touch', function() {
  if (dy !== 1) { // Assicura che non stia andando verso il basso
    dx = 0;
    dy = -1;
  }
});

handleTouch('left-touch', function() {
  if (dx !== 1) { // Assicura che non stia andando verso destra
    dx = -1;
    dy = 0;
  }
});

handleTouch('right-touch', function() {
  if (dx !== -1) { // Assicura che non stia andando verso sinistra
    dx = 1;
    dy = 0;
  }
});

handleTouch('down-touch', function() {
  if (dy !== -1) { // Assicura che non stia andando verso l'alto
    dx = 0;
    dy = 1;
  }
});


function startGame() {
  snake = [{ x: 10, y: 10 }];
  dx = 1;
  dy = 0;
  score = 0;
  isGameOver = false;
  document.getElementById("gameOverText").innerText = "";
  document.getElementById("score").innerText = score;
  generateFood();
  clearInterval(gameLoop);
  gameLoop = setInterval(updateGame, 100);
  
}

document.addEventListener("keydown", keyDownHandler);

