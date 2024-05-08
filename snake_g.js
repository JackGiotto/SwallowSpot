import platform from 'platform';        // library for checking the device support type
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



// Section of controls to see if the device is touchscreen or not, this is useful to know if the movements should be taken by touch or keyboard arrows

// Check if the device support multiple touch, if it support it, it could be a touchscreen device
function hasTouchSupport(){
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// Check based on the width of the device
function isMobile(){
    const minWidth = 768;           // Minimum width for desktop devices
    return window.innerWidth < minWidth || screen.width < minWidth;
}

// Function that groups the checks and their calls
function touchSupportCheck(){

    if(platform.isMobile){          // Check using a library that provides information about the browser, operating system, and device type by parsing the user agent string
        touchSupport+=1;
    }
    if(hasTouchSupport()){          // Method above with it explanation
        touchSupport+=1;
    }
    if(isMobile()){                 // Method above with it explanation
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
    alert("GAME OVER! Press OK to play again");
    location.reload();
}

const changeDirectionK = e =>{
    if(e.key === "ArrowUp" && speedY != 1){
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

// Call to "changeDirectionK" on each key click and passing key dataset value as an object
controls.forEach(button => button.addEventListener("click", () => changeDirection({ key: button.dataset.key })));
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
    
    // Shifting forward the values of the elements in the snake body by one
    for(let i=snakeBody.length-1; i>0; i--){
        snakeBody[i] = snakeBody[i-1];
    }
    if(snakeX <= 0 || snakeX > 30 || snakeY <= 0 || snakeY > 30){
        return gameOver = true;
    }

    for(let i=0; i<snakeBody.length; i++){
        html += `<div class="head" style="grid-area: ${snakeBody[i][1]} / ${snakeBody[i][0]}"></div>`;          // Adding a div for each part of the snake's body
        
        // Check if the snake head hit the body, in this case it set gameOver to true
        if(i !== 0 && snakeBody[0][1] == snakeBody[i][1] && snakeBody[0][0] == snakeBody[i][0]){
            gameOver = true;
        }
    }
    playBoard.innerHTML = html;
}


// T1
foodPosition();
setIntervalId = setInterval(initGame, 100);

if(touchSupportCheck() >= 2){       // If touchSupport is 2 or 3 means that probably is a touchscreen device so the EventListener is added
    document.addEventListener("touchstart", startTouch, false);
    document.addEventListener("touchmove", changeDirectionT, false);
}
else{
    document.addEventListener("keyup", changeDirectionK);
}

// T2
foodPosition();
setIntervalId = setInterval(initGame, 100);
document.addEventListener("keyup", changeDirectionK);


/* ------ */


myElement.addEventListener("touchstart", startTouch, false);
myElement.addEventListener("touchmove", moveTouch, false);
 
// Swipe Up / Down / Left / Right
var initialX = null;
var initialY = null;
 
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



const changeDirectionT = e => {
    if(e.type === "keyup" && !isTouchDevice()){       // Event from the keyboard and the device doesn't support touch
        handleKeyboardMovement(e);
    }
    else if(e.type === "touchstart" || e.type === "touchmove"){      // Event from touch
        handleTouchMovement(e);
    }
}

const handleKeyboardMovement = e => {
    if(e.key === "ArrowUp" && speedY !== 1){
        speedX = 0;
        speedY = -1;
    }
    else if(e.key === "ArrowDown" && speedY != -1){
        speedX = 0;
        speedY = 1;
    }
    else if(e.key === "ArrowLeft" && speedX !== 1){
        speedX = -1;
        speedY = 0;
    }
    else if(e.key === "ArrowRight" && speedX !== -1){
        speedX = 1;
        speedY = 0;
    }
}


const handleTouchMovement = e => {
    const touchX = e.touches[0].clientX;
    const touchY = e.touches[0].clientY;

    const diffX = touchX - initialX;
    const diffY = touchY - initialY;

    if(Math.abs(diffX) > Math.abs(diffY)){
        // Horizontal swipe
        if(diffX > 0){
            if(speedX !== -1){      // Swipe right
                speedX = 1;
                speedY = 0;
            }
        }
        else{
            if(speedX !== 1){       // Swipe left
                speedX = -1;
                speedY = 0;
            }
        }
    }
    // Vertical swipe
    else{
        if(diffY > 0){
            if(speedY !== -1){      // Swipe down
                speedX = 0;
                speedY = 1;
            }
        }
        else{
            if(speedY !== 1){       // Swipe up
                speedX = 0;
                speedY = -1;
            }
        }
    }
}

// Check if the device is touchscreen
const isTouchDevice = () => {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// Based on the type of input it add the event listener
if(isTouchDevice()){
    document.addEventListener("touchstart", startTouch, false);
    document.addEventListener("touchmove", changeDirectionT, false);
}
else{
    document.addEventListener("keyup", changeDirectionK);
}

