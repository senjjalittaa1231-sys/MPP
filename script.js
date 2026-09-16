const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const loginScreen = document.getElementById("loginScreen");
const gameScreen = document.getElementById("gameScreen");
const nameInput = document.getElementById("nameInput");
const startButton = document.getElementById("startButton");
const restartButton = document.getElementById("restartButton");
const gameOverBox = document.getElementById("gameOver");
const finalScore = document.getElementById("finalScore");
const niceText = document.getElementById("niceText");

const playerText = document.getElementById("playerText");
const scoreText = document.getElementById("scoreText");
const lengthText = document.getElementById("lengthText");
const speedText = document.getElementById("speedText");

const GRID = 20;
const BOARD_LEFT = 20;
const BOARD_TOP = 0;
const BOARD_RIGHT = 780;
const BOARD_BOTTOM = 600;

let snake = [];
let snakeColors = [];
let foods = [];
let score = 0;
let speed = 10;
let direction = "RIGHT";
let nextDirection = "RIGHT";
let playerName = "";
let gameRunning = false;
let niceTimer = 0;
let lastMove = 0;
let moveInterval = 1000 / 10;

const foodColors = [
    "#781478",
    "#c81e2e",
    "#1446b4",
    "#14783c",
    "#282828",
    "#dc8c0a"
];

let colorIndex = 0;

function resetGame() {
    snake = [
        { x: 400, y: 300 },
        { x: 380, y: 300 },
        { x: 360, y: 300 },
        { x: 340, y: 300 }
    ];

    snakeColors = snake.map(() => "#781478");
    score = 0;
    speed = 10;
    direction = "RIGHT";
    nextDirection = "RIGHT";
    colorIndex = 0;
    niceTimer = 0;
    moveInterval = 1000 / speed;
    gameOverBox.classList.add("hidden");
    createFoods();
    updateInfo();
}

function randomFoodPosition() {
    let position;

    do {
        const x = Math.floor(Math.random() * 37 + 2) * GRID;
        const y = Math.floor(Math.random() * 28 + 2) * GRID;
        position = { x, y };
    } while (
        snake.some(part => part.x === position.x && part.y === position.y) ||
        foods.some(food => food.x === position.x && food.y === position.y)
    );

    return position;
}

function createFoods() {
    foods = [];

    for (let i = 0; i < 20; i++) {
        foods.push(randomFoodPosition());
    }
}

function moveSnake() {
    direction = nextDirection;

    let head = { ...snake[0] };

    if (direction === "RIGHT") head.x += GRID;
    if (direction === "LEFT") head.x -= GRID;
    if (direction === "UP") head.y -= GRID;
    if (direction === "DOWN") head.y += GRID;

    snake.unshift(head);
    snakeColors.unshift(snakeColors[0]);

    const foodIndex = foods.findIndex(
        food => food.x === head.x && food.y === head.y
    );

    if (foodIndex !== -1) {
        score++;

        foods.splice(foodIndex, 1);
        foods.push(randomFoodPosition());

        const newColor = foodColors[colorIndex];
        snakeColors = snake.map(() => newColor);

        colorIndex++;
        if (colorIndex >= foodColors.length) {
            colorIndex = 0;
        }

        niceTimer = 35;

        if (score % 5 === 0) {
            speed += 2;
            if (speed > 25) speed = 25;
            moveInterval = 1000 / speed;
        }
    } else {
        snake.pop();
        snakeColors.pop();
    }

    updateInfo();

    if (checkGameOver()) {
        endGame();
    }
}

function checkGameOver() {
    const head = snake[0];

    if (head.x < BOARD_LEFT + GRID / 2) return true;
    if (head.x > BOARD_RIGHT - GRID / 2) return true;
    if (head.y < BOARD_TOP + GRID / 2) return true;
    if (head.y > BOARD_BOTTOM - GRID / 2) return true;

    for (let i = 1; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            return true;
        }
    }

    return false;
}

function drawBackground() {
    ctx.fillStyle = "#d7f0d7";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#bedcbe";
    ctx.lineWidth = 1;

    for (let x = BOARD_LEFT; x < BOARD_RIGHT; x += GRID) {
        ctx.beginPath();
        ctx.moveTo(x, BOARD_TOP);
        ctx.lineTo(x, BOARD_BOTTOM);
        ctx.stroke();
    }

    for (let y = BOARD_TOP; y < BOARD_BOTTOM; y += GRID) {
        ctx.beginPath();
        ctx.moveTo(BOARD_LEFT, y);
        ctx.lineTo(BOARD_RIGHT, y);
        ctx.stroke();
    }

    ctx.strokeStyle = "#286428";
    ctx.lineWidth = 3;
    ctx.strokeRect(
        BOARD_LEFT,
        BOARD_TOP,
        BOARD_RIGHT - BOARD_LEFT,
        BOARD_BOTTOM - BOARD_TOP
    );
}

function drawFood() {
    for (const food of foods) {
        ctx.fillStyle = "#dc1e28";
        ctx.fillRect(food.x - 7, food.y - 7, 14, 14);

        ctx.fillStyle = "#ff7878";
        ctx.fillRect(food.x - 4, food.y - 4, 5, 5);

        ctx.fillStyle = "#14641e";
        ctx.fillRect(food.x + 5, food.y - 9, 6, 4);
    }
}

function drawSnake() {
    snake.forEach((part, index) => {
        ctx.fillStyle = snakeColors[index];
        ctx.fillRect(
            part.x - GRID / 2 + 1,
            part.y - GRID / 2 + 1,
            GRID - 2,
            GRID - 2
        );

        ctx.strokeStyle = "#280a28";
        ctx.lineWidth = 1;
        ctx.strokeRect(
            part.x - GRID / 2,
            part.y - GRID / 2,
            GRID,
            GRID
        );
    });

    const head = snake[0];
    let eye1;
    let eye2;

    if (direction === "RIGHT") {
        eye1 = { x: head.x + 5, y: head.y - 5 };
        eye2 = { x: head.x + 5, y: head.y + 5 };
    } else if (direction === "LEFT") {
        eye1 = { x: head.x - 5, y: head.y - 5 };
        eye2 = { x: head.x - 5, y: head.y + 5 };
    } else if (direction === "UP") {
        eye1 = { x: head.x - 5, y: head.y - 5 };
        eye2 = { x: head.x + 5, y: head.y - 5 };
    } else {
        eye1 = { x: head.x - 5, y: head.y + 5 };
        eye2 = { x: head.x + 5, y: head.y + 5 };
    }

    for (const eye of [eye1, eye2]) {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(eye.x - 2, eye.y - 2, 4, 4);

        ctx.fillStyle = "#000000";
        ctx.fillRect(eye.x - 1, eye.y - 1, 2, 2);
    }
}

function draw() {
    drawBackground();

    if (gameRunning) {
        drawFood();
    }

    drawSnake();
}

function updateInfo() {
    playerText.textContent = "Pemain: " + playerName;
    scoreText.textContent = "Skor: " + score;
    lengthText.textContent = "Panjang: " + snake.length;
    speedText.textContent = "Speed: " + speed;
}

function endGame() {
    gameRunning = false;
    finalScore.textContent = "Skor Akhir: " + score;
    gameOverBox.classList.remove("hidden");
}

function setDirection(newDirection) {
    if (!gameRunning) return;

    if (newDirection === "RIGHT" && direction !== "LEFT") {
        nextDirection = "RIGHT";
    }

    if (newDirection === "LEFT" && direction !== "RIGHT") {
        nextDirection = "LEFT";
    }

    if (newDirection === "UP" && direction !== "DOWN") {
        nextDirection = "UP";
    }

    if (newDirection === "DOWN" && direction !== "UP") {
        nextDirection = "DOWN";
    }
}

function startGame() {
    const name = nameInput.value.trim();

    if (name === "") {
        nameInput.focus();
        return;
    }

    playerName = name;
    loginScreen.classList.add("hidden");
    gameScreen.classList.remove("hidden");

    resetGame();
    gameRunning = true;
    lastMove = performance.now();
}

startButton.addEventListener("click", startGame);

nameInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        startGame();
    }
});

restartButton.addEventListener("click", () => {
    resetGame();
    gameRunning = true;
    lastMove = performance.now();
});

document.querySelectorAll("#controls button[data-direction]").forEach(button => {
    const directionName = button.dataset.direction;

    button.addEventListener("pointerdown", event => {
        event.preventDefault();
        setDirection(directionName);
    });
});

window.addEventListener("keydown", event => {
    const keys = {
        ArrowRight: "RIGHT",
        d: "RIGHT",
        D: "RIGHT",
        ArrowLeft: "LEFT",
        a: "LEFT",
        A: "LEFT",
        ArrowUp: "UP",
        w: "UP",
        W: "UP",
        ArrowDown: "DOWN",
        s: "DOWN",
        S: "DOWN"
    };

    if (keys[event.key]) {
        event.preventDefault();
        setDirection(keys[event.key]);
    }

    if (event.key === " " && !gameRunning && !gameOverBox.classList.contains("hidden")) {
        resetGame();
        gameRunning = true;
        lastMove = performance.now();
    }
});

function gameLoop(timestamp) {
    if (gameRunning && timestamp - lastMove >= moveInterval) {
        moveSnake();
        lastMove = timestamp;
    }

    draw();

    if (niceTimer > 0) {
        niceText.classList.remove("hidden");
        niceTimer--;
    } else {
        niceText.classList.add("hidden");
    }

    requestAnimationFrame(gameLoop);
}

resetGame();
requestAnimationFrame(gameLoop);
