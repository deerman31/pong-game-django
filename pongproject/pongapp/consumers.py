from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .game_logic import GameState

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = GameState()
        self.running = False

    async def connect(self):
        await self.accept()
        self.running = True
        asyncio.create_task(self.move_ball())

    async def disconnect(self, close_code):
        self.running = False

    async def move_ball(self):
        while self.running:
            if not self.game_state.is_game_over():
                self.game_state.move_ball()
            else:
                self.game_state.reset()

            self.game_state.move_ball()

            # クライアントにボールとパドルの位置を送信
            await self.send(text_data=json.dumps({
                'ball_x': self.game_state.ball_x,
                'ball_y': self.game_state.ball_y,
                'player_y': self.game_state.player_y,
                'score': self.game_state.player_score,
                'game_over': self.game_state.is_game_over(),
            }))
            # 更新間隔を設定（例えば0.05秒ごと）
            await asyncio.sleep(0.01)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        print(f"Received action: {action}")

        if action == 'start':
            self.game_state.start_game()
        elif action == 'up':
            self.game_state.move_player_up()
        elif action == 'down':
            self.game_state.move_player_down()
        
        # クライアントに新しい位置を送信
        await self.send(text_data=json.dumps({
            #'player_y': self.player_y
            'player_y': self.game_state.player_y
        }))

