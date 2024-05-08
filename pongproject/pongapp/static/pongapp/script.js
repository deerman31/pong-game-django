// pongapp/static/pongapp/script.js

document.addEventListener("DOMContentLoaded", function() {
    const startButton = document.getElementById("start-game");
    const paddle1 = document.getElementById("player-1");
    const paddle2 = document.getElementById("player-2");
    const ball = document.getElementById("ball");
    const score1Element = document.getElementById("score-1");
    const score2Element = document.getElementById("score-2");

    let score1 = 0;
    let score2 = 0;

    function updateScores() {
        score1Element.textContent = score1;
        score2Element.textContent = score2;
    }

    // WebSocketの接続
    const socket = new WebSocket("ws://" + window.location.host + "/ws/pong/");

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        ball.style.left = data.ball_x + "px";
        ball.style.top = data.ball_y + "px";
        paddle1.style.top = data.player_1_y + "px";
        paddle2.style.top = data.player_2_y + "px";
        score1 = data.score_1;
        score2 = data.score_2;
        updateScores();
    };

    startButton.addEventListener("click", function() {
        socket.send(JSON.stringify({ action: "start" }));
    });

    // キー入力でパドルを動かす
    document.addEventListener("keydown", function(event) {
        const key = event.key;
        let action = null;

        if (key === "ArrowUp") {
            action = "up";
        } else if (key === "ArrowDown") {
            action = "down";
        }

        if (action) {
            socket.send(JSON.stringify({ action: action }));
        }
    });
});
