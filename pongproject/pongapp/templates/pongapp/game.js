const socket = new WebSocket('ws://localhost:8000/ws/pong/');
let paddle1 = null;
let paddle2 = null;
let ball = null;
let player1Score = null;
let player2Score = null;

const debugInfo = document.createElement('div');
debugInfo.id = "debug-info";

const startScreen = document.createElement('div');
startScreen.id = "start-screen";
const startButton = document.createElement('button');
startButton.id = "start-button";
startButton.innerText = "Start Game";

const winScreen = document.createElement('div');
winScreen.id = "win-screen";
const winMessage = document.createElement('h2');
winMessage.id = "win-message";
const restartButton = document.createElement('button');
restartButton.id = "restart-button";
restartButton.innerText = "Restart Game";
restartButton.onclick = function() {
    location.reload();  // ページを再読み込みしてゲームをリセット
};

document.addEventListener('DOMContentLoaded', function() {
    // ゲームボードの要素
    paddle1 = document.getElementById('player1-paddle');
    paddle2 = document.getElementById('player2-paddle');
    ball = document.getElementById('ball');
    player1Score = document.getElementById('player1-score');
    player2Score = document.getElementById('player2-score');

    // スタート画面とボタンをセットアップ
    startScreen.appendChild(startButton);
    document.body.appendChild(startScreen);
    document.body.appendChild(debugInfo);

    // 勝敗画面とボタンをセットアップ
    winScreen.appendChild(winMessage);
    winScreen.appendChild(restartButton);
    document.body.appendChild(winScreen);

    // スタートボタンをクリックしたときの処理
    startButton.addEventListener('click', function() {
        socket.send(JSON.stringify({'action': 'start'}));
        document.getElementById('game-board').style.display = "block";
        startScreen.style.display = "none";
    });
});

function updateDebugInfo(message) {
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    debugInfo.appendChild(messageElement);
    debugInfo.scrollTop = debugInfo.scrollHeight;
}

socket.onopen = function(e) {
    console.log("WebSocket connection opened.");
    updateDebugInfo("WebSocket connection opened.");
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    let message = '';

    // プレイヤー1のパドル位置とスコアを更新
    if (data.player_1_y !== undefined) {
        paddle1.style.top = `${data.player_1_y}px`;
        message += `Player 1 paddle position: ${data.player_1_y}\n`;
    }
    if (data.score_1 !== undefined) {
        player1Score.textContent = `Player 1: ${data.score_1}`;
        message += `Player 1 score: ${data.score_1}\n`;
    }

    // プレイヤー2のパドル位置とスコアを更新
    if (data.player_2_y !== undefined) {
        paddle2.style.top = `${data.player_2_y}px`;
        message += `Player 2 paddle position: ${data.player_2_y}\n`;
    }
    if (data.score_2 !== undefined) {
        player2Score.textContent = `Player 2: ${data.score_2}`;
        message += `Player 2 score: ${data.score_2}\n`;
    }

    // ボールの位置を更新
    if (data.ball_x !== undefined && data.ball_y !== undefined) {
        ball.style.left = `${data.ball_x}px`;
        ball.style.top = `${data.ball_y}px`;
        message += `Ball position: (${data.ball_x}, ${data.ball_y})\n`;
    }

    // 勝敗が決定した場合
    if (data.winner !== undefined) {
        winMessage.textContent = `Player ${data.winner} wins!`;
        document.getElementById('game-board').style.display = "none";
        winScreen.style.display = "flex";
    }

    updateDebugInfo(message);
};

// キーボード入力に応じてアクションをサーバーに送信
document.addEventListener('keydown', function(event) {
    let action = null;
    if (event.key === 'ArrowUp') {
        action = 'up';
    } else if (event.key === 'ArrowDown') {
        action = 'down';
    }

    if (action) {
        socket.send(JSON.stringify({'action': action}));
    }
});

