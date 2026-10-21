import math
import random
import sys
import array
import pygame

# -----------------------------------------------------------------------------
# CONFIGURAÇÕES E CONSTANTES
# -----------------------------------------------------------------------------
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 680
FPS = 60

# Cores
COLOR_BG = (18, 18, 28)
COLOR_PANEL = (28, 30, 48)
COLOR_BORDER = (212, 175, 55)  # Dourado
COLOR_TEXT = (240, 240, 245)
COLOR_MUTED = (140, 145, 165)
COLOR_GREEN = (46, 204, 113)
COLOR_RED = (231, 76, 60)
COLOR_LINE_WIN = (255, 215, 0)

# Definição dos Símbolos
SYMBOLS = [
    {"id": "CHERRY", "label": "🍒", "color": (231, 76, 60),  "mult_3": 5,   "weight": 35},
    {"id": "LEMON",  "label": "🍋", "color": (241, 196, 15), "mult_3": 10,  "weight": 25},
    {"id": "GRAPE",  "label": "🍇", "color": (155, 89, 182), "mult_3": 20,  "weight": 20},
    {"id": "DIAMOND","label": "💎", "color": (52, 152, 219), "mult_3": 50,  "weight": 12},
    {"id": "SEVEN",  "label": "7️⃣", "color": (230, 126, 34), "mult_3": 100, "weight": 8},
]

SYMBOL_DICT = {s["id"]: s for s in SYMBOLS}
POPULATION = [s["id"] for s in SYMBOLS]
WEIGHTS = [s["weight"] for s in SYMBOLS]

# Linhas de pagamento (Linha, Coluna): 3 horizontais + 2 diagonais
PAYLINES = [
    [ (0,0), (0,1), (0,2) ],  # Horizontal Superior
    [ (1,0), (1,1), (1,2) ],  # Horizontal Central
    [ (2,0), (2,1), (2,2) ],  # Horizontal Inferior
    [ (0,0), (1,1), (2,2) ],  # Diagonal Principal
    [ (2,0), (1,1), (0,2) ]   # Diagonal Secundária
]

# -----------------------------------------------------------------------------
# SINTETIZADOR DE ÁUDIO NATIVO
# -----------------------------------------------------------------------------
def init_audio():
    """Inicializa o mixer e gera sons sintetizados sem arquivos externos."""
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    except pygame.error:
        return None

    def make_sound(freq, duration, wave_type="sine"):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = array.array('h')
        for i in range(n_samples):
            t = i / sample_rate
            if wave_type == "sine":
                val = math.sin(2 * math.pi * freq * t)
            elif wave_type == "square":
                val = 0.6 if math.sin(2 * math.pi * freq * t) > 0 else -0.6
            elif wave_type == "noise":
                val = random.uniform(-0.8, 0.8)
            else:
                val = 0
            
            # Decay simples para suavizar o som
            decay = (n_samples - i) / n_samples
            sample = int(val * decay * 16383)
            buf.append(sample)
        return pygame.mixer.Sound(buffer=buf)

    try:
        sounds = {
            "spin": make_sound(120, 0.08, "square"),
            "stop": make_sound(220, 0.1, "sine"),
            "win":  make_sound(587.33, 0.4, "sine"),
            "click": make_sound(440, 0.04, "sine")
        }
        return sounds
    except Exception:
        return None


# -----------------------------------------------------------------------------
# CLASSE DE COMPONENTES INTERATIVOS (BOTÕES)
# -----------------------------------------------------------------------------
class Button:
    def __init__(self, rect, text, bg_color, text_color, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font
        self.callback = callback
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.callback:
                self.callback()

    def draw(self, surface):
        color = [min(c + 30, 255) for c in self.bg_color] if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=2, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


# -----------------------------------------------------------------------------
# CLASSE DA MÁQUINA DE SLOTS (LÓGICA E RENDERIZAÇÃO)
# -----------------------------------------------------------------------------
class SlotMachine3x3:
    def __init__(self, x, y, width, height, font_symbol):
        self.rect = pygame.Rect(x, y, width, height)
        self.font_symbol = font_symbol
        self.cols = 3
        self.rows = 3

        # Dimensões de cada célula
        self.cell_w = width // self.cols
        self.cell_h = height // self.rows

        # Estado da matriz (3x3 com IDs dos símbolos)
        self.grid = [
            [random.choice(POPULATION) for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

        # Estado da animação por coluna
        self.spinning = False
        self.col_offsets = [0.0, 0.0, 0.0]
        self.col_speeds = [0.0, 0.0, 0.0]
        self.col_states = ["idle", "idle", "idle"] # idle, spinning, stopping
        self.col_timers = [0, 0, 0]

        # Símbolos que deslizam durante o giro
        self.spin_strips = [[], [], []]
        self.winning_lines = []

    def start_spin(self, target_grid):
        """Inicia a animação de rotação com destino pré-calculado."""
        self.spinning = True
        self.target_grid = target_grid
        self.winning_lines = []

        for c in range(self.cols):
            self.col_states[c] = "spinning"
            self.col_speeds[c] = random.uniform(35, 45)
            self.col_offsets[c] = 0.0
            # Tempo adicional para parada em cascata por coluna
            self.col_timers[c] = 45 + (c * 25)
            # Gera tira de símbolos aleatórios para o giro
            self.spin_strips[c] = [random.choice(POPULATION) for _ in range(15)]

    def update(self, sounds=None):
        if not self.spinning:
            return False

        all_stopped = True

        for c in range(self.cols):
            if self.col_states[c] == "spinning":
                all_stopped = False
                self.col_offsets[c] += self.col_speeds[c]
                self.col_timers[c] -= 1

                # Toca som de giro periodicamente
                if sounds and "spin" in sounds and random.random() < 0.15:
                    sounds["spin"].play()

                if self.col_timers[c] <= 0:
                    self.col_states[c] = "stopping"

            elif self.col_states[c] == "stopping":
                all_stopped = False
                # Efeito de desaceleração (frenagem)
                self.col_speeds[c] *= 0.82
                self.col_offsets[c] += self.col_speeds[c]

                if self.col_speeds[c] < 2.0:
                    self.col_states[c] = "idle"
                    self.col_offsets[c] = 0.0
                    self.col_speeds[c] = 0.0
                    
                    # Atualiza os símbolos da coluna finalizada
                    for r in range(self.rows):
                        self.grid[r][c] = self.target_grid[r][c]

                    if sounds and "stop" in sounds:
                        sounds["stop"].play()

        if all_stopped:
            self.spinning = False
            return True # Giro concluído

        return False

    def draw(self, surface):
        # Fundo do painel 3x3
        pygame.draw.rect(surface, (12, 12, 20), self.rect, border_radius=12)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=3, border_radius=12)

        # Recorte de área para que os símbolos não vazem o painel
        surface.set_clip(self.rect)

        for c in range(self.cols):
            col_x = self.rect.x + c * self.cell_w

            # Divisórias verticais
            if c > 0:
                pygame.draw.line(
                    surface, COLOR_PANEL, 
                    (col_x, self.rect.y), 
                    (col_x, self.rect.bottom), 
                    width=3
                )

            offset = self.col_offsets[c] % self.cell_h

            # Se estiver girando, desenha os símbolos em movimento
            if self.col_states[c] != "idle":
                strip = self.spin_strips[c]
                for idx, sym_id in enumerate(strip):
                    sym_y = self.rect.y + (idx * self.cell_h) - offset
                    if self.rect.y - self.cell_h <= sym_y <= self.rect.bottom:
                        self._draw_symbol(surface, sym_id, col_x, sym_y)
            else:
                # Desenha os símbolos estáticos da matriz
                for r in range(self.rows):
                    sym_y = self.rect.y + r * self.cell_h
                    sym_id = self.grid[r][c]
                    self._draw_symbol(surface, sym_id, col_x, sym_y)

        # Divisórias horizontais
        for r in range(1, self.rows):
            line_y = self.rect.y + r * self.cell_h
            pygame.draw.line(
                surface, COLOR_PANEL, 
                (self.rect.x, line_y), 
                (self.rect.right, line_y), 
                width=2
            )

        # Desenhar linhas vitoriosas
        if not self.spinning and self.winning_lines:
            for line in self.winning_lines:
                points = []
                for r, c in line:
                    px = self.rect.x + (c + 0.5) * self.cell_w
                    py = self.rect.y + (r + 0.5) * self.cell_h
                    points.append((px, py))
                
                pygame.draw.lines(surface, COLOR_LINE_WIN, False, points, width=6)
                for pt in points:
                    pygame.draw.circle(surface, (255, 255, 255), pt, 8)

        # Restaura a área de clipe padrão
        surface.set_clip(None)

    def _draw_symbol(self, surface, sym_id, x, y):
        sym_info = SYMBOL_DICT[sym_id]
        
        # Fundo do card do símbolo
        card_rect = pygame.Rect(x + 6, y + 6, self.cell_w - 12, self.cell_h - 12)
        pygame.draw.rect(surface, COLOR_PANEL, card_rect, border_radius=8)

        # Render do Emoji / Texto do Símbolo
        txt = self.font_symbol.render(sym_info["label"], True, sym_info["color"])
        txt_rect = txt.get_rect(center=card_rect.center)
        surface.blit(txt, txt_rect)


# -----------------------------------------------------------------------------
# CLASSE PRINCIPAL DO JOGO
# -----------------------------------------------------------------------------
class CasinoGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cassino 3x3 — Slots Universitário")
        self.clock = pygame.time.Clock()

        # Fontes
        self.font_title = pygame.font.SysFont("arial", 28, bold=True)
        self.font_main = pygame.font.SysFont("arial", 18, bold=True)
        self.font_small = pygame.font.SysFont("arial", 14)
        self.font_symbol = pygame.font.SysFont("segoe ui emoji", 42)

        # Som
        self.sounds = init_audio()
        self.sound_enabled = True

        # Economia / Estado do Jogo
        self.balance = 1000.0
        self.bet = 10.0
        self.last_win = 0.0
        self.history = []

        # Instância da máquina
        self.slot = SlotMachine3x3(280, 120, 400, 380, self.font_symbol)

        # Botões
        self.buttons = [
            Button((340, 520, 280, 50), "GIRAR (ESPAÇO)", (230, 126, 34), (255, 255, 255), self.font_main, self.action_spin),
            Button((280, 580, 60, 40), "-10", (52, 73, 94), COLOR_TEXT, self.font_main, lambda: self.adjust_bet(-10)),
            Button((350, 580, 60, 40), "+10", (52, 73, 94), COLOR_TEXT, self.font_main, lambda: self.adjust_bet(10)),
            Button((420, 580, 70, 40), "MÁX", (41, 128, 185), COLOR_TEXT, self.font_main, self.set_max_bet),
            Button((500, 580, 80, 40), "+100 R$", (39, 174, 96), COLOR_TEXT, self.font_main, self.add_fake_money),
            Button((590, 580, 90, 40), "SOM: ON", (127, 140, 141), COLOR_TEXT, self.font_small, self.toggle_sound),
        ]

    def adjust_bet(self, amount):
        if not self.slot.spinning:
            self.bet = max(5.0, min(self.balance, self.bet + amount))
            self.play_sound("click")

    def set_max_bet(self):
        if not self.slot.spinning and self.balance > 0:
            self.bet = float(self.balance)
            self.play_sound("click")

    def add_fake_money(self):
        self.balance += 100.0
        self.play_sound("click")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        btn = self.buttons[-1]
        btn.text = f"SOM: {'ON' if self.sound_enabled else 'OFF'}"

    def play_sound(self, sound_key):
        if self.sound_enabled and self.sounds and sound_key in self.sounds:
            self.sounds[sound_key].play()

    def generate_spin_result(self):
        """Sorteia uma matriz 3x3 de acordo com os pesos configurados."""
        return [
            random.choices(POPULATION, weights=WEIGHTS, k=3)
            for _ in range(3)
        ]

    def evaluate_result(self, grid):
        """Avalia as 5 linhas de pagamento e calcula o total ganho."""
        total_payout = 0.0
        winning_lines = []

        for line in PAYLINES:
            symbols_in_line = [grid[r][c] for r, c in line]
            
            # Verifica se os 3 símbolos da linha são idênticos
            if symbols_in_line[0] == symbols_in_line[1] == symbols_in_line[2]:
                sym_id = symbols_in_line[0]
                mult = SYMBOL_DICT[sym_id]["mult_3"]
                total_payout += self.bet * mult
                winning_lines.append(line)

        return total_payout, winning_lines

    def action_spin(self):
        if self.slot.spinning:
            return

        if self.balance < self.bet:
            return

        # Desconta a aposta
        self.balance -= self.bet
        self.last_win = 0.0

        # Gera o resultado final
        self.pending_grid = self.generate_spin_result()
        self.slot.start_spin(self.pending_grid)
        self.play_sound("click")

    def on_spin_complete(self):
        """Chamado quando a animação de giro termina."""
        payout, winning_lines = self.evaluate_result(self.slot.grid)
        self.last_win = payout
        self.balance += payout
        self.slot.winning_lines = winning_lines

        # Atualiza o Histórico
        net = payout - self.bet
        self.history.insert(0, {"bet": self.bet, "payout": payout, "net": net})
        if len(self.history) > 6:
            self.history.pop()

        if payout > 0:
            self.play_sound("win")

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            # --- PROCESSAMENTO DE EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.action_spin()

                for btn in self.buttons:
                    btn.handle_event(event)

            # --- ATUALIZAÇÃO ---
            if self.slot.update(self.sounds if self.sound_enabled else None):
                self.on_spin_complete()

            # --- RENDERIZAÇÃO ---
            self.screen.fill(COLOR_BG)
            self._draw_header()
            self._draw_sidebar_paytable()
            self._draw_sidebar_history()
            
            self.slot.draw(self.screen)

            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # --- ELEMENTOS DE INTERFACE ---
    def _draw_header(self):
        # Título do jogo
        title_surf = self.font_title.render("CASINO SLOTS 3x3", True, COLOR_BORDER)
        self.screen.blit(title_surf, (280, 20))

        # Card de Saldo
        bal_rect = pygame.Rect(280, 65, 180, 45)
        pygame.draw.rect(self.screen, COLOR_PANEL, bal_rect, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_BORDER, bal_rect, width=1, border_radius=6)
        
        lbl_bal = self.font_small.render("SALDO DISPONÍVEL", True, COLOR_MUTED)
        val_bal = self.font_main.render(f"R$ {self.balance:.2f}", True, COLOR_GREEN)
        self.screen.blit(lbl_bal, (290, 70))
        self.screen.blit(val_bal, (290, 87))

        # Card de Aposta Atual
        bet_rect = pygame.Rect(470, 65, 100, 45)
        pygame.draw.rect(self.screen, COLOR_PANEL, bet_rect, border_radius=6)
        lbl_bet = self.font_small.render("APOSTA", True, COLOR_MUTED)
        val_bet = self.font_main.render(f"R$ {self.bet:.2f}", True, COLOR_TEXT)
        self.screen.blit(lbl_bet, (480, 70))
        self.screen.blit(val_bet, (480, 87))

        # Card do Último Ganho
        win_rect = pygame.Rect(580, 65, 100, 45)
        pygame.draw.rect(self.screen, COLOR_PANEL, win_rect, border_radius=6)
        lbl_win = self.font_small.render("ÚLT. GANHO", True, COLOR_MUTED)
        color_win = COLOR_GREEN if self.last_win > 0 else COLOR_MUTED
        val_win = self.font_main.render(f"R$ {self.last_win:.2f}", True, color_win)
        self.screen.blit(lbl_win, (590, 70))
        self.screen.blit(val_win, (590, 87))

    def _draw_sidebar_paytable(self):
        panel = pygame.Rect(20, 20, 240, 640)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BORDER, panel, width=1, border_radius=10)

        title = self.font_main.render("TABELA DE PAGAMENTOS", True, COLOR_BORDER)
        self.screen.blit(title, (30, 35))

        subtitle = self.font_small.render("Combine 3 ícones nas 5 linhas:", True, COLOR_MUTED)
        self.screen.blit(subtitle, (30, 60))

        y = 90
        for sym in SYMBOLS:
            # Emoji/Símbolo
            s_surf = self.font_symbol.render(sym["label"], True, sym["color"])
            self.screen.blit(s_surf, (35, y))

            # Nome e Multiplicador
            name_surf = self.font_small.render(sym["id"], True, COLOR_TEXT)
            mult_surf = self.font_main.render(f"{sym['mult_3']}x", True, COLOR_GREEN)
            
            self.screen.blit(name_surf, (90, y + 5))
            self.screen.blit(mult_surf, (90, y + 22))

            y += 55

        # Dica de Linhas de Pagamento
        pygame.draw.line(self.screen, COLOR_MUTED, (30, y + 10), (240, y + 10), width=1)
        lines_info = [
            "Linhas Valendo:",
            "• 3 Horizontais",
            "• 2 Diagonais"
        ]
        y_info = y + 25
        for info in lines_info:
            txt = self.font_small.render(info, True, COLOR_MUTED)
            self.screen.blit(txt, (35, y_info))
            y_info += 20

    def _draw_sidebar_history(self):
        panel = pygame.Rect(700, 20, 240, 640)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BORDER, panel, width=1, border_radius=10)

        title = self.font_main.render("HISTÓRICO RECENTE", True, COLOR_BORDER)
        self.screen.blit(title, (715, 35))

        y = 70
        if not self.history:
            empty_txt = self.font_small.render("Nenhuma aposta ainda.", True, COLOR_MUTED)
            self.screen.blit(empty_txt, (715, y))
            return

        for idx, item in enumerate(self.history):
            item_rect = pygame.Rect(710, y, 220, 80)
            pygame.draw.rect(self.screen, COLOR_BG, item_rect, border_radius=6)

            txt_bet = self.font_small.render(f"Aposta: R$ {item['bet']:.2f}", True, COLOR_TEXT)
            txt_pay = self.font_small.render(f"Retorno: R$ {item['payout']:.2f}", True, COLOR_TEXT)
            
            net_color = COLOR_GREEN if item['net'] >= 0 else COLOR_RED
            sign = "+" if item['net'] > 0 else ""
            txt_net = self.font_main.render(f"Lucro: {sign}R$ {item['net']:.2f}", True, net_color)

            self.screen.blit(txt_bet, (720, y + 8))
            self.screen.blit(txt_pay, (720, y + 28))
            self.screen.blit(txt_net, (720, y + 50))

            y += 90


# -----------------------------------------------------------------------------
# PONTO DE ENTRADA DO PROGRAMA
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    game = CasinoGame()
    game.run()