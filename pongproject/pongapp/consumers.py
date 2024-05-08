from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .game_logic import Game

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = Game()
        self.running = False
        self.player_id = None

    async def connect(self):
        await self.accept()
        if not self.game.players[1].score:
            self.player_id = 1
        elif not self.game.players[2].score:
            self.player_id = 2
        else:
            await self.close() # すでに二人参加している場合は閉じる

        self.running = True
        asyncio.create_task(self.move_ball())

    async def disconnect(self, close_code):
        self.running = False

    async def move_ball(self):
        while self.running:
            if not self.game.is_game_over():
                self.game.move_ball()
            else:
                winner = 1 if self.game.players[1].score >= self.game.max_score else 2
                await self.send(text_data=json.dumps({
                    'game_over': True,
                    'winner': winner
                }))
                self.game.reset()

            # プレイヤー情報を含むデータを送信
            await self.send_game_state()

            # 更新間隔を設定（例えば0.05秒ごと）
            await asyncio.sleep(0.05)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        print(f"Received action: {action}")

        if action == 'start':
            self.game.start()
            print("Game started")
        elif self.player_id == 1:
            if action == 'up':
                self.game.players[1].paddle.move_up()
            elif action == 'down':
                self.game.players[1].paddle.move_down(600)
        elif self.player_id == 2:
            if action == 'up':
                self.game.players[2].paddle.move_up()
            elif action == 'down':
                self.game.players[2].paddle.move_down(600)

        # クライアントに新しい位置を送信
        await self.send_game_state()

    async def send_game_state(self):
        """現在のゲーム状態をクライアントに送信する"""
        #print("send_game_state")
        await self.send(text_data=json.dumps({
            'ball_x': self.game.ball.x,
            'ball_y': self.game.ball.y,
            'player_1_y': self.game.players[1].paddle.y,
            'player_2_y': self.game.players[2].paddle.y,
            'score_1': self.game.players[1].score,
            'score_2': self.game.players[2].score,
            'game_over': self.game.is_game_over()
        }))