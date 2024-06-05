const playBoard = document.querySelector(".play-board");
const scoreElement = document.querySelector(".score");
const highScoreElement = document.querySelector(".high-score");
const controls = document.querySelectorAll(".controls i");

let gameOver = false;
let foodX, foodY;
let snakeX = 15, snakeY = 15;           // To spawn the snake in the centre of the field
let speedX = 0, speedY = 0;
let snakeBody = [];
let setIntervalId;
let score = 0;
let touchSupport = 0;
var initialX = null, initialY = null;


// Section of controls to see if the device is touchscreen or not, this is useful to know if the movements should be taken by touch or keyboard arrows

// Check if the device support multiple touch, if it support it, it could be a touchscreen device
function hasTouchSupport(){
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}


// Check if the device supports touch events using a combination of 'ontouchstart' in window and the DocumentTouch interface
function isTouchDevice(){
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
highScoreElement.innerText = `Record personale: ${highScore}`;


function foodPosition(){

    let validPosition = false;
    let foodtype = 1

    foodtype = Math.floor(Math.random() * 6) + 1;           // Generate a random number to choose the type of food that will be displayed

    if(foodtype == 1 ){
        html = `<div class="food apple" style="grid-area: ${foodY}/${foodX}"><img src="/AppleEmoji_snake.png"></div>`
    }
    else if(foodtype == 2){
        html = `<div class="food banana" style="grid-area: ${foodY}/${foodX}"><img src="/BananaEmoji_snake.png"></div>`
    }
    else if(foodtype == 3){
        html = `<div class="food cherry" style="grid-area: ${foodY}/${foodX}"><img src="/CherryEmoji_snake.png"></div>`
    }
    else if(foodtype == 4){
        html = `<div class="food peach" style="grid-area: ${foodY}/${foodX}"><img src="/PeachEmoji_snake.png"></div>`
    }
    else if(foodtype == 5){
        html = `<div class="food pear" style="grid-area: ${foodY}/${foodX}"><img src="/PearEmoji_snake.png"></div>`
    }
    else if(foodtype == 6){
        html = `<div class="food strawberry" style="grid-area: ${foodY}/${foodX}"><img src="/StrawberrEmoji_snake.png"></div>`
    }

    while(!validPosition){          // Assign a random value from 1 to 30 to X and Y to determine a position except the cells where there is the snake
        foodX = Math.floor(Math.random() * 30) + 1;
        foodY = Math.floor(Math.random() * 30) + 1;
        
        validPosition = true;
        for(let i = 0; i < snakeBody.length; i++){
            if(snakeBody[i][0] === foodX && snakeBody[i][1] === foodY){
                validPosition = false;
                break;
            }
        }
    }
    playBoard.innerHTML += htmlfood;
}


function handleGameOver(){          // Resetting the timer and reloading the page on game over
    clearInterval(setIntervalId);
    document.getElementById("gameOverScreen").style.display = "block";
    document.getElementById("scoreDisplay").innerText = "Punteggio ottenuto: " + score;

    if(score > highScore){
        highScore = score;
        localStorage.setItem("high-score", highScore);
        highScoreElement.innerText = `Record personale: ${highScore}`;
    }

    function continueGame(){
        document.getElementById("gameOverScreen").style.display = "none";
        foodPosition();
        location.reload();
    }


    document.getElementById("continueButton").addEventListener("click", continueGame);          // Event listener for the button "Continua"   
    document.addEventListener("keyup", function(e){         // Event listener for the "Enter" key of the keyboard
        if(e.key === "Enter"){
            continueGame();
        }
    });
}


function changeDirectionK(e){       // Function to change the direction of the snake based on the keyboard input
    // Check if the key pressed is the "ArrowUp" key, the snake is not currently moving downward,
    // and either the snake's body length is 1 or less, or if it is greater than 1,
    // ensure that the current vertical speed is not moving upward.
    if(e.key === "ArrowUp" && speedY !== 1 && (snakeBody.length <= 1 || speedY !== -1)){
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
 
    var currentX = e.touches[0].clientX;            // Obtain the current X coordinate of the touch relative to the top-left corner of the touched element
    var currentY = e.touches[0].clientY;
    
    var diffX = initialX - currentX;            // Calculate the difference between the initial X and Y coordinate and the current X and Y coordinate of the touch for understanding the direction of the swipe
    var diffY = initialY - currentY;

    if(Math.abs(diffX) > Math.abs(diffY)){

        // Horizontal swipe
        // Ensure that the current horizontal speed is not moving right (speedX !== 1)
        // Allow changing direction if the snake's body length is exactly 1 or if it is greater than 1, ensure that the current horizontal speed is not moving left (speedX !== -1)
        if(diffX > 0 && speedX !== 1 && (snakeBody.length == 1 || speedX !== -1)){
            // Swiped left
            speedX = -1;
            speedY = 0;
        }
        else if(diffX < 0 && speedX !== -1 && (snakeBody.length == 1 || speedX !== 1)){
            // Swiped right
            speedX = 1;
            speedY = 0;
        }
    }
    else{   // Vertical swipe
        if(diffY > 0 && speedY !== 1 && (snakeBody.length == 1 || speedY !== -1)){
            // Swiped up
            speedX = 0;
            speedY = -1;
        }
        else if(diffY < 0 && speedY !== -1 && (snakeBody.length == 1 || speedY !== 1)){
            // Swiped down
            speedX = 0;
            speedY = 1;
        }
    }

    initialX = null;
    initialY = null;

    e.preventDefault();
};


function changeDirectionT(e){
    if (e.type === "touchstart" || e.type === "touchmove") {
        moveTouch(e);
    }
}

// Call to "changeDirectionK" on each key click and passing key dataset value as an object
controls.forEach(function(button) {
    button.addEventListener("click", function() {
        changeDirectionK({ key: button.dataset.key });
    });
});


function launchConfetti()
{
    confetti({
        particleCount: 100,         // Set the number of confetti
        angle: -25,         // Set the angle that confetti will be thrown
        spread: 70,         // Set the spread of the thrown
        origin: {x:0.1, y:0.1}          // Set the point from which the confetti will be thrown
    });

    confetti({
        particleCount: 100,
        angle: 205,
        spread: 70,
        origin: {x:0.9, y:0.1}
    });
}


function initGame()
{
    if(gameOver)
    {
        return handleGameOver();
    }

    snakeBody[0] = [snakeX, snakeY];

    // Check if the snake hit the food
    if(snakeX == foodX && snakeY == foodY){
        foodPosition();
        snakeBody.push([foodY, foodX]);         // Pushing food position to snake body array
        score++;
        highScore = Math.max(score, highScore);
        localStorage.setItem("high-score", highScore);
        scoreElement.innerText = `Punteggio: ${score}`;
        if(score % 50 === 0){
            launchConfetti();
        }
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

    for(let i=0; i<snakeBody.length; i++)
    {
        html += `<div class="head" style="grid-area: ${snakeBody[i][1]} / ${snakeBody[i][0]}"></div>`;          // Adding a div for each part of the snake's body
        
        if(i !== 0 && snakeBody[0][1] == snakeBody[i][1] && snakeBody[0][0] == snakeBody[i][0]){            // Check if the snake head hit the body, in this case it set gameOver to true
            gameOver = true;
        }
    }
    playBoard.innerHTML = html;

}

document.getElementById("gameOverScreen").style.display = "none";           // Hide the "Game Over" screen
foodPosition();
setIntervalId = setInterval(initGame, 100);

if(touchSupportCheck() >= 2){           // If touchSupport is 2 or 3 means that probably is a touchscreen device so the EventListener is added
    document.addEventListener("touchstart", startTouch, false);
    document.addEventListener("touchmove", changeDirectionT, false);
}
else{
    document.addEventListener("keyup", changeDirectionK);
}