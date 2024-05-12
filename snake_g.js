const playBoard = document.querySelector(".play-board");
const scoreElement = document.querySelector(".score");
const highScoreElement = document.querySelector(".high-score");
const controls = document.querySelectorAll(".controls i");

let gameOver = false;
let foodX, foodY;
let snakeX = 5, snakeY = 5;
let speedX = 0, speedY = 0;
let snakeBody = [];
let setIntervalId;
let score = 0;
let touchSupport = 0;
var initialX = null;
var initialY = null;



// Section of controls to see if the device is touchscreen or not, this is useful to know if the movements should be taken by touch or keyboard arrows

// Check if the device support multiple touch, if it support it, it could be a touchscreen device
function hasTouchSupport(){
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}


// Check if the device supports touch events using a combination of 'ontouchstart' in window and the DocumentTouch interface
function isTouchDevice() {
    return 'ontouchstart' in window || (window.DocumentTouch && document instanceof window.DocumentTouch);
}


// Check based on the width of the device
function isMobile(){
    const minWidth = 768;           // Minimum width for desktop devices
    return window.innerWidth < minWidth || screen.width < minWidth;
}

// Function that groups the checks and their calls
function touchSupportCheck(){

    if(hasTouchSupport()){
        touchSupport+=1;
    }
    if(isTouchDevice()){
        touchSupport+=1;
    }
    if(isMobile()){
        touchSupport+=1;
    }
    return touchSupport;
}


// Getting high score from the local storage
let highScore = localStorage.getItem("high-score") || 0;
highScoreElement.innerText = `High Score: ${highScore}`;

// Assign a random value from 1 to 30 to X and Y to determine a position
const foodPosition = () => {
    foodX = Math.floor(Math.random()*30)+1;
    foodY = Math.floor(Math.random()*30)+1;
}


const handleGameOver = () =>{
    // Resetting the timer and reloading the page on game over
    clearInterval(setIntervalId);
    document.getElementById("gameOverScreen").style.display = "block";
    document.getElementById("scoreDisplay").innerText = "Punteggio ottenuto: " + score;
    // Event listener for the button "Continua
    document.getElementById("continueButton").addEventListener("click", () => {
        document.getElementById("gameOverScreen").style.display = "none";
        foodPosition();
        location.reload();
    });
}


const changeDirectionK = e =>{
    // Changing velocity value based on key press
    if(e.key === "ArrowUp" && speedY != -1){
        speedX = 0;
        speedY = -1;
    }
    else if(e.key === "ArrowDown" && speedY != -1){
        speedX = 0;
        speedY = 1;
    }
    else if(e.key === "ArrowLeft" && speedX != 1){
        speedX = -1;
        speedY = 0;
    }
    else if(e.key === "ArrowRight" && speedX != -1){
        speedX = 1;
        speedY = 0;
    }
}
 
function startTouch(e){
    initialX = e.touches[0].clientX;
    initialY = e.touches[0].clientY;
};


 
function moveTouch(e){
    if(initialX === null){
        return;
    }

    if(initialY === null){
        return;
    }
 
    var currentX = e.touches[0].clientX;
    var currentY = e.touches[0].clientY;
    
    var diffX = initialX - currentX;
    var diffY = initialY - currentY;
    
    if(Math.abs(diffX) > Math.abs(diffY)){

        // Horizontal swipe
        if(diffX > 0){
            // Swiped left
            console.log("left");
            speedX = -1;
            speedY = 0;
        }
        else{
            // Swiped right
            console.log("right");
            speedX = 1;
            speedY = 0;
        }
    }
    else{   // Vertical swipe
        if(diffY > 0){
            // Swiped up
            console.log("up");
            speedX = 0;
            speedY = -1;
        }
        else{
            // Swiped down
            console.log("down");
            speedX = 0;
            speedY = 1;
        }
    }

    initialX = null;
    initialY = null;

    e.preventDefault();
};

function changeDirectionT(e) {
    if (e.type === "touchstart" || e.type === "touchmove") {
        moveTouch(e);
    }
}


// Call to "changeDirectionK" on each key click and passing key dataset value as an object
controls.forEach(button => button.addEventListener("click", () => changeDirectionK({ key: button.dataset.key })));
const initGame = () =>{
    if(gameOver)
        return handleGameOver();
    let html = `<div class="food" style="grid-area: ${foodY}/${foodX}"></div>`;
    
    // Check if the snake hit the food
    if(snakeX == foodX && snakeY == foodY){
        foodPosition();
        snakeBody.push([foodY, foodX]);         // Pushing food position to snake body array
        score++;
        highScore = score >= highScore ? score : highScore;
        localStorage.setItem("high-score", highScore);
        scoreElement.innerText = `Score: ${score}`;
        highScoreElement.innerText = `High Score: ${highScore}`;
    }

    // Updating the snake's head position based on the current speed
    snakeX += speedX;
    snakeY += speedY;
    
    for(let i=snakeBody.length-1; i>0; i--){            // Shifting forward the values of the elements in the snake body by one
        snakeBody[i] = snakeBody[i-1];
    }
    
    snakeBody[0] = [snakeX, snakeY];            // Setting first element of snake body to current snake position
    
    if(snakeX <= 0 || snakeX > 30 || snakeY <= 0 || snakeY > 30){           // Checking if the snake's head is out of wall, if so setting gameOver to true
        return gameOver = true;
    }
    
    for(let i=0; i<snakeBody.length; i++){
        html += `<div class="head" style="grid-area: ${snakeBody[i][1]} / ${snakeBody[i][0]}"></div>`;          // Adding a div for each part of the snake's body
        
        if(i !== 0 && snakeBody[0][1] == snakeBody[i][1] && snakeBody[0][0] == snakeBody[i][0]){            // Check if the snake head hit the body, in this case it set gameOver to true
            gameOver = true;
        }
    }
    playBoard.innerHTML = html;
}

document.getElementById("gameOverScreen").style.display = "none";           // Make sure that the "Game Over" is not displayed
foodPosition();
setIntervalId = setInterval(initGame, 100);

if(touchSupportCheck() >= 2){           // If touchSupport is 2 or 3 means that probably is a touchscreen device so the EventListener is added
    document.addEventListener("touchstart", startTouch, false);
    document.addEventListener("touchmove", changeDirectionT, false);
}
else{
    document.addEventListener("keyup", changeDirectionK);
}