import platform from 'platform';
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



// Section of controls (3 in total) to see if the device is touchscreen or not, this is useful to know if the movements should be taken by touch or keyboard arrows

// Function that control if the device support multiple touch, if it support it, it could be a touchscreen device
function hasTouchSupport(){
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// Second check based on the width of the device
function isMobile(){
    const minWidth = 768;           // Minimum width for desktop devices
    return window.innerWidth < minWidth || screen.width < minWidth;
}


function touchSupportCheck(){

    if(platform.isMobile){
        touchSupport+=1
    }
    if(hasTouchSupport()){
        touchSupport+=1
    }
    if(isMobile()){         // Third check using a library that provides information about the browser, operating system, and device type by parsing the user agent string
        touchSupport+=1
    }

    // If touchSupport is 2 or 3 means that probably is a touchscreen device
    if(touchSupport >= 2){
        // The device is touchscreen                        ****** TO BE IMPLEMENTED ******
    }
    else{
        // The devise is NOT touchscreen                    ****** TO BE IMPLEMENTED ******
    }
}






// Getting high score from the local storage
let highScore = localStorage.getItem("high-score") || 0;
highScoreElement.innerText = `High Score: ${highScore}`;
const updateFoodPosition = () => {
    // Passing a random 1-30 value as food position
    foodX = Math.floor(Math.random()*30)+1;
    foodY = Math.floor(Math.random()*30)+1;
}

const handleGameOver = () =>{
    // Resetting the timer and reloading the page on game over
    clearInterval(setIntervalId);
    alert("GAME OVER! Press OK to play again");
    location.reload();
}

const changeDirection = e =>{
    if(e.key === "ArrowUp" && speedY != 1){
        speedX = 0;
        speedY = -1;
    } else if(e.key === "ArrowDown" && speedY != -1){
        speedX = 0;
        speedY = 1;
    } else if(e.key === "ArrowLeft" && speedX != 1){
        speedX = -1;
        speedY = 0;
    } else if(e.key === "ArrowRight" && speedX != -1){
        speedX = 1;
        speedY = 0;
    }
}

// Call to "changeDirection" on each key click and passing key dataset value as an object
controls.forEach(button => button.addEventListener("click", () => changeDirection({ key: button.dataset.key })));
const initGame = () =>{
    if(gameOver) return handleGameOver();
    let html = `<div class="food" style="grid-area: ${foodY}/${foodX}"></div>`;
    
    // Checking if the snake hit the food
    if(snakeX == foodX && snakeY == foodY){
        updateFoodPosition();
        snakeBody.push([foodY, foodX]); // Pushing food position to snake body array
        score++;
        highScore = score >= highScore ? score : highScore;
        localStorage.setItem("high-score", highScore);
        scoreElement.innerText = `Score: ${score}`;
        highScoreElement.innerText = `High Score: ${highScore}`;
    }

    // Updating the snake's head position based on the current speed
    snakeX += speedX;
    snakeY += speedY;
    
    // Shifting forward the values of the elements in the snake body by one
    for(let i = snakeBody.length-1; i>0; i--){
        snakeBody[i] = snakeBody[i-1];
    }
    snakeBody[0] = [snakeX, snakeY];            // Setting first element of snake body to current snake position
    
    // Control of the snake head if is out of wall, in this case gameOver it set to true
    if(snakeX <= 0 || snakeX > 30 || snakeY <= 0 || snakeY > 30){
        return gameOver = true;
    }

    for(let i=0; i<snakeBody.length; i++){
        html += `<div class="head" style="grid-area: ${snakeBody[i][1]} / ${snakeBody[i][0]}"></div>`;          // Adding a div for each part of the snake's body
        
        // Control of the snake head hit the body, in this case it set gameOver to true
        if(i !== 0 && snakeBody[0][1] == snakeBody[i][1] && snakeBody[0][0] == snakeBody[i][0]){
            gameOver = true;
        }
    }
    playBoard.innerHTML = html;
}

touchSupportCheck();
updateFoodPosition();
setIntervalId = setInterval(initGame, 100);
document.addEventListener("keyup", changeDirection);