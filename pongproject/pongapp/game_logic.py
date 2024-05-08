class Paddle:
    def __init__(self, x_position, y_position, height, speed):
        self.x = x_position
        self.y = y_position
        self.height = height
        self.speed = speed
    def move_up(self):
        self.y = max(self.y - self.speed, 0)
        print("A: paddle up", self.y)
    def move_down(self, boundary):
        self.y = min(self.y + self.speed, boundary - self.height)
        print("A: paddle down", self.y)

class Ball:
    def __init__(self, x_position=400, y_position=300, radius=10, speed=10):
        self.x = x_position
        self.y = y_position
        self.dx = speed
        self.dy = speed
        self.radius = radius
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def bounce_vertical(self):
        print("bounce_vertical")
        self.dy = -self.dy

    def bounce_horizontal(self):
        print("bounce_horizontal")
        self.dx = -self.dx

    def reset(self):
        self.x = 400
        self.y = 300
        self.dx = -self.dx
        self.dy = -self.dy

class Player:
    def __init__(self, name, x_position, y_position=250, height=100, speed=20):
        self.name = name
        self.score = 0
        self.paddle = Paddle(x_position, y_position=250, height=100, speed=20)

    def add_score(self):
        print(self.name, ": add_score")
        self.score += 1

class Game:
    def __init__(self):
        self.players = {
            1: Player("ykusano", 10),
            2: Player("nop", 760)
        }
        self.ball = Ball()
        self.max_score = 10
        self.started = False
        self.winner = None
    
    def check_winner(self):
        if self.players[1].score >= self.max_score:
            self.winner = 1
        elif self.players[2].score >= self.max_score:
            self.winner = 2
    
    def start(self):
        print("Game start")
        self.started = True
    def stop(self):
        print("Game stop")
        self.started = False
    def reset(self):
        for player in self.players.values():
            player.score = 0
        self.ball.reset()
        self.started = False
        self.winner = None

    def move_ball(self):
        """ボールの動きと衝突判定"""
        if not self.started:
            #print("Game is not started")  # デバッグ用の出力
            return

        #print("Moving the ball")  # デバッグ用の出力
        self.ball.move()

        # 上下の壁でボールが跳ね返る
        if self.ball.y <= 0 or self.ball.y >= 580:
            self.ball.bounce_vertical()

        # プレイヤーパドルとの衝突判定
        if (self.ball.x <= self.players[1].paddle.x + 0 and
            self.players[1].paddle.y <= self.ball.y <= self.players[1].paddle.y + self.players[1].paddle.height):
            self.ball.bounce_horizontal()
        elif (self.ball.x >= self.players[2].paddle.x - 0 and
              self.players[2].paddle.y <= self.ball.y <= self.players[2].paddle.y + self.players[2].paddle.height):
            self.ball.bounce_horizontal()

        # ボールが左側の壁を通過したら右側のプレイヤーの得点
        elif self.ball.x <= 0:
            self.players[2].add_score()
            self.ball.reset()

        # ボールが右側の壁を通過したら左側のプレイヤーの得点
        elif self.ball.x >= 800:
            self.players[1].add_score()
            self.ball.reset()

    def is_game_over(self):
        """どちらかのプレイヤーが最大スコアに達したらゲームオーバー"""
        return any(player.score >= self.max_score for player in self.players.values())