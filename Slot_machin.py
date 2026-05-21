import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
import os
import sys

# Tentativo di import per i suoni
try:
    import winsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

class SlotMachineGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 SLOT MACHINE DELUXE 🎰")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Colori e stili
        self.colors = {
            'bg': '#1a1a2e',
            'slot_bg': '#16213e',
            'gold': '#ffd700',
            'silver': '#c0c0c0',
            'red': '#e94560',
            'green': '#0f3460'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Variabili di gioco
        self.balance = 1000
        self.min_bet = 10
        self.max_bet = 500
        self.current_bet = 10
        self.spinning = False
        
        # Simboli della slot (emoji più leggibili)
        self.symbols = {
            "🍒": {"value": 5, "name": "Ciliegia", "color": "#ff4444"},
            "🍊": {"value": 10, "name": "Arancia", "color": "#ff8800"},
            "🍋": {"value": 15, "name": "Limone", "color": "#ffff44"},
            "💎": {"value": 50, "name": "Diamante", "color": "#00ffff"},
            "7️⃣": {"value": 100, "name": "Sette", "color": "#ff00ff"},
            "🎰": {"value": 200, "name": "JACKPOT", "color": "#ffd700"}
        }
        
        # Lista pesata per probabilità realistiche
        self.symbol_list = []
        for symbol in self.symbols:
            if symbol == "🍒":
                self.symbol_list.extend([symbol] * 40)
            elif symbol == "🍊":
                self.symbol_list.extend([symbol] * 30)
            elif symbol == "🍋":
                self.symbol_list.extend([symbol] * 15)
            elif symbol == "💎":
                self.symbol_list.extend([symbol] * 10)
            elif symbol == "7️⃣":
                self.symbol_list.extend([symbol] * 4)
            elif symbol == "🎰":
                self.symbol_list.extend([symbol] * 1)
        
        self.setup_ui()
        self.update_balance_display()
        
    def setup_ui(self):
        # Frame principale
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titolo
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title = tk.Label(title_frame, text="🎰 SLOT MACHINE DELUXE 🎰", 
                        font=('Arial', 24, 'bold'), 
                        fg=self.colors['gold'], bg=self.colors['bg'])
        title.pack()
        
        # Frame del credito
        credit_frame = tk.Frame(main_frame, bg=self.colors['slot_bg'], relief='ridge', bd=3)
        credit_frame.pack(fill='x', pady=10)
        
        self.credit_label = tk.Label(credit_frame, text="CREDITO: $1000", 
                                     font=('Arial', 18, 'bold'),
                                     fg=self.colors['gold'], bg=self.colors['slot_bg'])
        self.credit_label.pack(pady=10)
        
        # Frame della slot machine
        slot_frame = tk.Frame(main_frame, bg=self.colors['slot_bg'], relief='ridge', bd=5)
        slot_frame.pack(pady=20, padx=20)
        
        # Display dei rulli
        self.reel_labels = []
        reel_frame = tk.Frame(slot_frame, bg=self.colors['slot_bg'])
        reel_frame.pack(pady=20, padx=20)
        
        for i in range(3):
            reel = tk.Label(reel_frame, text="🎰", font=('Arial', 80), 
                           width=3, height=1, relief='sunken', bd=3,
                           bg='white', fg=self.colors['gold'])
            reel.pack(side='left', padx=10, pady=10)
            self.reel_labels.append(reel)
        
        # Frame di controllo
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(pady=20)
        
        # Bet controls
        bet_controls = tk.Frame(control_frame, bg=self.colors['bg'])
        bet_controls.pack(pady=10)
        
        tk.Label(bet_controls, text="PUNTATA:", font=('Arial', 12, 'bold'),
                fg='white', bg=self.colors['bg']).pack(side='left', padx=5)
        
        tk.Button(bet_controls, text="-", font=('Arial', 14, 'bold'),
                 command=self.decrease_bet, width=3, bg=self.colors['red'],
                 fg='white').pack(side='left', padx=5)
        
        self.bet_label = tk.Label(bet_controls, text="$10", font=('Arial', 14, 'bold'),
                                 fg=self.colors['gold'], bg=self.colors['bg'], width=8)
        self.bet_label.pack(side='left', padx=5)
        
        tk.Button(bet_controls, text="+", font=('Arial', 14, 'bold'),
                 command=self.increase_bet, width=3, bg=self.colors['green'],
                 fg='white').pack(side='left', padx=5)
        
        # Pulsante SPIN
        self.spin_button = tk.Button(control_frame, text="🎲 SPIN 🎲", 
                                     font=('Arial', 16, 'bold'),
                                     command=self.spin, bg=self.colors['gold'],
                                     fg='black', width=15, height=2)
        self.spin_button.pack(pady=10)
        
        # Pulsanti funzione
        func_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        func_frame.pack(pady=10)
        
        tk.Button(func_frame, text="📋 TABELLA", font=('Arial', 10, 'bold'),
                 command=self.show_paytable, bg=self.colors['silver'],
                 width=12).pack(side='left', padx=5)
        
        tk.Button(func_frame, text="🔄 RESET", font=('Arial', 10, 'bold'),
                 command=self.reset_game, bg=self.colors['silver'],
                 width=12).pack(side='left', padx=5)
        
        tk.Button(func_frame, text="🚪 ESCI", font=('Arial', 10, 'bold'),
                 command=self.exit_game, bg=self.colors['red'],
                 fg='white', width=12).pack(side='left', padx=5)
        
        # Messaggio di stato
        self.status_label = tk.Label(main_frame, text="Pronto per giocare! 🎰", 
                                     font=('Arial', 10, 'italic'),
                                     fg=self.colors['silver'], bg=self.colors['bg'])
        self.status_label.pack(pady=10)
        
        # Ultima vincita
        self.last_win_label = tk.Label(main_frame, text="", font=('Arial', 12, 'bold'),
                                       fg=self.colors['gold'], bg=self.colors['bg'])
        self.last_win_label.pack()
    
    def update_balance_display(self):
        self.credit_label.config(text=f"CREDITO: ${self.balance}")
        if self.balance < self.min_bet:
            self.spin_button.config(state='disabled', bg='gray')
            self.status_label.config(text="💔 Credito insufficiente! Premi RESET per continuare 💔")
        else:
            self.spin_button.config(state='normal', bg=self.colors['gold'])
    
    def decrease_bet(self):
        if self.current_bet > self.min_bet:
            self.current_bet -= 10
            self.bet_label.config(text=f"${self.current_bet}")
            self.play_sound(800, 50)
    
    def increase_bet(self):
        if self.current_bet < self.max_bet and self.current_bet + 10 <= self.balance:
            self.current_bet += 10
            self.bet_label.config(text=f"${self.current_bet}")
            self.play_sound(1000, 50)
        elif self.current_bet + 10 > self.balance:
            self.status_label.config(text="⚠️ Puntata troppo alta per il tuo credito! ⚠️")
    
    def play_sound(self, frequency, duration):
        if SOUND_ENABLED:
            try:
                threading.Thread(target=lambda: winsound.Beep(frequency, duration), daemon=True).start()
            except:
                pass
    
    def animate_spin(self):
        """Anima i rulli durante lo spin"""
        for _ in range(15):  # 15 fotogrammi di animazione
            for i in range(3):
                random_symbol = random.choice(self.symbol_list)
                self.reel_labels[i].config(text=random_symbol)
            self.root.update()
            time.sleep(0.05)
    
    def spin(self):
        if self.spinning:
            return
        
        if self.current_bet > self.balance:
            messagebox.showerror("Errore", "Credito insufficiente!")
            return
        
        self.spinning = True
        self.spin_button.config(state='disabled', bg='gray')
        self.status_label.config(text="🎲 SPIN IN CORSO... 🎲")
        
        # Sottrai la puntata
        self.balance -= self.current_bet
        self.update_balance_display()
        
        # Animazione
        self.animate_spin()
        
        # Spin finale
        self.play_sound(800, 100)
        reels = [random.choice(self.symbol_list) for _ in range(3)]
        
        # Mostra risultato finale
        for i, symbol in enumerate(reels):
            self.reel_labels[i].config(text=symbol)
        
        # Calcola vincita
        win_amount = self.calculate_winnings(reels, self.current_bet)
        
        if win_amount > 0:
            self.balance += win_amount
            self.update_balance_display()
            
            # Effetto visivo vincita
            for label in self.reel_labels:
                original_bg = label.cget('bg')
                label.config(bg=self.colors['gold'])
                self.root.update()
                time.sleep(0.2)
                label.config(bg=original_bg)
            
            self.last_win_label.config(text=f"🎉 VINCITA: ${win_amount}! 🎉")
            self.status_label.config(text=f"🎉 Complimenti! Hai vinto ${win_amount}! 🎉")
            self.play_sound(1500, 300)
            self.play_sound(2000, 500)
            
            # Suono extra per jackpot
            if reels[0] == reels[1] == reels[2] == "🎰":
                for _ in range(3):
                    self.play_sound(2500, 200)
                    time.sleep(0.1)
                messagebox.showinfo("🎉 JACKPOT! 🎉", 
                                   f"🎰 HAI VINTO IL JACKPOT DI ${win_amount}! 🎰")
        else:
            self.last_win_label.config(text=f"😢 Perso: ${self.current_bet}")
            self.status_label.config(text="😢 Peccato! Ritenta, sarai più fortunato!")
            self.play_sound(400, 500)
        
        self.spinning = False
        
        # Aggiorna stato pulsante
        if self.balance < self.min_bet:
            self.status_label.config(text="💔 Game Over! Premi RESET per continuare")
            self.spin_button.config(state='disabled', bg='gray')
        else:
            self.spin_button.config(state='normal', bg=self.colors['gold'])
    
    def calculate_winnings(self, reels, bet):
        s1, s2, s3 = reels
        
        # Jackpot
        if s1 == s2 == s3 == "🎰":
            return bet * self.symbols["🎰"]["value"]
        
        # Tre simboli uguali
        if s1 == s2 == s3:
            return bet * self.symbols[s1]["value"]
        
        # Due simboli uguali
        if s1 == s2 or s2 == s3:
            symbol = s1 if s1 == s2 else s2
            return bet * self.symbols[symbol]["value"] // 2
        
        # Bonus speciali
        bonus = 0
        if "💎" in reels:
            bonus += bet * 2
        if "7️⃣" in reels:
            bonus += bet * 5
        if "🎰" in reels:
            bonus += bet * 10
            
        return bonus
    
    def show_paytable(self):
        paytable_window = tk.Toplevel(self.root)
        paytable_window.title("Tabella Pagamenti")
        paytable_window.geometry("400x500")
        paytable_window.configure(bg=self.colors['bg'])
        
        tk.Label(paytable_window, text="📋 TABELLA PAGAMENTI", 
                font=('Arial', 16, 'bold'),
                fg=self.colors['gold'], bg=self.colors['bg']).pack(pady=10)
        
        # Frame scrollabile
        canvas = tk.Canvas(paytable_window, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(paytable_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Simboli - CORREZIONE QUI!
        for symbol, data in self.symbols.items():
            frame = tk.Frame(scrollable_frame, bg=self.colors['slot_bg'], relief='ridge', bd=2)
            frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(frame, text=symbol, font=('Arial', 40), 
                    bg=self.colors['slot_bg']).pack(side='left', padx=10)
            
            # CORREZIONE: rimosso 'x' errato nella f-string
            info = f"{data['name']}\n{data['value']}x la puntata"
            tk.Label(frame, text=info, font=('Arial', 10),
                    fg='white', bg=self.colors['slot_bg'], justify='left').pack(side='left', padx=10)
        
        # Regole
        rules = """
Regole Speciali:
• 3 simboli uguali = valore x puntata
• 2 simboli uguali = 50% del valore
• Bonus combinati:
  - 💎 = +2x puntata
  - 7️⃣ = +5x puntata  
  - 🎰 = +10x puntata
        """
        
        tk.Label(scrollable_frame, text=rules, font=('Arial', 10),
                fg=self.colors['silver'], bg=self.colors['bg'], justify='left').pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Button(paytable_window, text="CHIUDI", command=paytable_window.destroy,
                 bg=self.colors['gold'], font=('Arial', 10, 'bold')).pack(pady=10)
    
    def reset_game(self):
        self.balance = 1000
        self.current_bet = 10
        self.bet_label.config(text="$10")
        self.update_balance_display()
        self.last_win_label.config(text="")
        self.status_label.config(text="Gioco resettato! Buona fortuna! 🍀")
        
        # Reset rulli
        for label in self.reel_labels:
            label.config(text="🎰")
        
        self.play_sound(1000, 200)
        messagebox.showinfo("Reset", "Gioco resettato! Credito: $1000")
    
    def exit_game(self):
        if messagebox.askyesno("Esci", f"Vuoi uscire con ${self.balance} di credito?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = SlotMachineGame(root)
    root.mainloop()