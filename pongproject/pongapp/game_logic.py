class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player_y = 250
        self.ball_x = 400
        self.ball_y = 300
        self.ball_dx = 3
        self.ball_dy = 3
        self.player_score = 0
        self.game_started = False

    def start_game(self):
        self.game_started = True

    def move_player_up(self):
        self.player_y = max(self.player_y - 20, 0)

    def move_player_down(self):
        self.player_y = min(self.player_y + 20, 500)
    
    def move_ball(self):
        if not self.game_started:
            return

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x <= 0:
            self.player_score += 1
            self.reset_ball()
        elif self.ball_x >= 780:
            self.ball_dx = -self.ball_dx

        if self.ball_y <= 0 or self.ball_y >= 580:
            self.ball_dy = -self.ball_dy

        # パドルとの衝突判定
        if self.ball_x <= 21 and self.player_y <= self.ball_y <= self.player_y + 100:
            self.ball_dx = -self.ball_dx

    def reset_ball(self):
        self.ball_x = 400
        self.ball_y = 300
        self.ball_dx = 3
        self.ball_dy = 3
    
    def is_game_over(self):
        return self.player_score >= 10