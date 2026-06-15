#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scribere - A Hyper-Minimalist Terminal Typing Tutor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import curses
import random
import sys
import os
import json
import time
import platform
from pathlib import Path
from datetime import datetime

# --- CONFIGURATION & CONSTANTS ---
VERSION = "1.0.0"
CONFIG_DIR = Path.home() / ".scribere"
CONFIG_FILE = CONFIG_DIR / "config.json"
SCORES_FILE = CONFIG_DIR / "scores.json"

# Color Pairs
C_NORMAL = 1
C_CURSOR = 2
C_TYPED_CORRECT = 3
C_TYPED_ERROR = 4
C_SUBTLE = 5
C_BORDER = 6
C_HIGHLIGHT = 7

# Quote Database: Diverse sources (Literature, Science, Art, Philosophy, Tech)
# Format: {"text": "...", "author": "...", "topic": "...", "length_cat": "short|medium|long|longest"}
RAW_QUOTES = [
    # SHORT (5-15 words)
    {"text": "Simplicity is the ultimate sophistication.", "author": "Leonardo da Vinci", "topic": "Art"},
    {"text": "Know thyself.", "author": "Socrates", "topic": "Philosophy"},
    {"text": "Nature does not hurry, yet everything is accomplished.", "author": "Lao Tzu", "topic": "Philosophy"},
    {"text": "The unexamined life is not worth living.", "author": "Socrates", "topic": "Philosophy"},
    {"text": "Less is more.", "author": "Mies van der Rohe", "topic": "Design"},
    {"text": "Art is never finished, only abandoned.", "author": "Paul Valéry", "topic": "Art"},
    {"text": "Code is like humor. When you have to explain it, it is bad.", "author": "Cory House", "topic": "Tech"},
    {"text": "Fix the cause, not the symptom.", "author": "Steve Maguire", "topic": "Tech"},
    {"text": "Truth is ever to be found in simplicity.", "author": "Isaac Newton", "topic": "Science"},
    {"text": "Life is short, art is long.", "author": "Hippocrates", "topic": "Medicine"},
    {"text": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs", "topic": "Business"},
    {"text": "Stay hungry, stay foolish.", "author": "Steve Jobs", "topic": "Life"},
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "topic": "Work"},
    {"text": "Simplicity is the soul of efficiency.", "author": "Austin Freeman", "topic": "Tech"},
    {"text": "Make it work, make it right, make it fast.", "author": "Kent Beck", "topic": "Tech"},
    
    # MEDIUM (16-30 words)
    {"text": "The best way to predict the future is to invent it.", "author": "Alan Kay", "topic": "Tech"},
    {"text": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler", "topic": "Tech"},
    {"text": "It is not that I am so smart, it is just that I stay with problems longer.", "author": "Albert Einstein", "topic": "Science"},
    {"text": "Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.", "author": "Albert Einstein", "topic": "Science"},
    {"text": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu", "topic": "Philosophy"},
    {"text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "author": "Ralph Waldo Emerson", "topic": "Life"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "topic": "History"},
    {"text": "Believe you can and you are halfway there.", "author": "Theodore Roosevelt", "topic": "Life"},
    {"text": "Act as if what you do makes a difference. It does.", "author": "William James", "topic": "Psychology"},
    {"text": "Never bend your head. Always hold it high. Look the world straight in the eye.", "author": "Helen Keller", "topic": "Life"},
    {"text": "What we think, we become.", "author": "Buddha", "topic": "Philosophy"},
    {"text": "Hardships often prepare ordinary people for an extraordinary destiny.", "author": "C.S. Lewis", "topic": "Literature"},
    {"text": "Do not go where the path may lead, go instead where there is no path and leave a trail.", "author": "Ralph Waldo Emerson", "topic": "Life"},
    {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins", "topic": "Motivation"},
    {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "topic": "Science"},
    
    # LONG (31-50 words)
    {"text": "Programming is not about what you know; it is about what you can figure out when you don't know. The process of learning to program is a process of learning how to learn.", "author": "Chris Pine", "topic": "Tech"},
    {"text": "The function of good software is to make the complex appear to be simple. Simplicity is the ultimate sophistication and the hallmark of genius.", "author": "Grady Booch", "topic": "Tech"},
    {"text": "We are what we repeatedly do. Excellence, then, is not an act, but a habit. We must all suffer from one of two pains: the pain of discipline or the pain of regret.", "author": "Aristotle", "topic": "Philosophy"},
    {"text": "It does not matter how slowly you go as long as you do not stop. Our greatest glory is not in never falling, but in rising every time we fall.", "author": "Confucius", "topic": "Philosophy"},
    {"text": "The measure of intelligence is the ability to change. Everybody is a genius. But if you judge a fish by its ability to climb a tree, it will live its whole life believing that it is stupid.", "author": "Albert Einstein", "topic": "Science"},
    {"text": "Creativity is intelligence having fun. The true sign of intelligence is not knowledge but imagination. Logic will get you from A to B. Imagination will take you everywhere.", "author": "Albert Einstein", "topic": "Science"},
    {"text": "First, solve the problem. Then, write the code. Experience is the name everyone gives to their mistakes. The only real mistake is the one from which we learn nothing.", "author": "John Johnson", "topic": "Tech"},
    {"text": "Talk is cheap. Show me the code. Programs must be written for people to read, and only incidentally for machines to execute.", "author": "Linus Torvalds", "topic": "Tech"},
    {"text": "The saddest aspect of life right now is that science gathers knowledge faster than society gathers wisdom. Science without religion is lame, religion without science is blind.", "author": "Isaac Asimov", "topic": "Science"},
    {"text": "I have not failed. I have just found ten thousand ways that won't work. Genius is one percent inspiration and ninety-nine percent perspiration.", "author": "Thomas Edison", "topic": "History"},
    
    # LONGEST (50+ words)
    {"text": "Two things are infinite: the universe and human stupidity; and I am not sure about the universe. The important thing is not to stop questioning. Curiosity has its own reason for existing.", "author": "Albert Einstein", "topic": "Science"},
    {"text": "Be yourself; everyone else is already taken. To live is the rarest thing in the world. Most people exist, that is all. Be who you are and say what you feel, because those who mind don't matter and those who matter don't mind.", "author": "Oscar Wilde", "topic": "Literature"},
    {"text": "In three words I can sum up everything I have learned about life: it goes on. Life is what happens to us while we are making other plans. The purpose of our lives is to be happy.", "author": "Robert Frost", "topic": "Literature"},
    {"text": "Clean code always looks like it was written by someone who cares. There is nothing quite so permanent as a quick fix. Getting good at programming is largely a matter of adopting good habits.", "author": "Robert C. Martin", "topic": "Tech"},
    {"text": "The computer was born to solve problems that did not exist before. Software is eating the world. Technology is best when it brings people together. It has become appallingly obvious that our technology has exceeded our humanity.", "author": "Bill Gates", "topic": "Tech"},
    {"text": "Education is the most powerful weapon which you can use to change the world. It always seems impossible until it is done. Freedom cannot be achieved unless women have been emancipated from all forms of oppression.", "author": "Nelson Mandela", "topic": "History"},
    {"text": "If you want to lift yourself up, lift up someone else. I have learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.", "author": "Booker T. Washington", "topic": "History"},
    {"text": "The greatest glory in living lies not in never falling, but in rising every time we fall. The future belongs to those who believe in the beauty of their dreams. Tell me and I forget. Teach me and I remember. Involve me and I learn.", "author": "Eleanor Roosevelt", "topic": "History"},
]

def categorize_quotes():
    """Categorize quotes by word count."""
    categorized = {"short": [], "medium": [], "long": [], "longest": []}
    for q in RAW_QUOTES:
        words = len(q["text"].split())
        if words <= 15:
            q["length_cat"] = "short"
            categorized["short"].append(q)
        elif words <= 30:
            q["length_cat"] = "medium"
            categorized["medium"].append(q)
        elif words <= 50:
            q["length_cat"] = "long"
            categorized["long"].append(q)
        else:
            q["length_cat"] = "longest"
            categorized["longest"].append(q)
    return categorized

QUOTE_DB = categorize_quotes()

# --- UTILS ---

def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        default_config = {
            "theme": "default",
            "minimal_stats": False,
            "color_correct": 3, # Blue
            "color_error": 4,   # Red
            "cursor_color": 2   # Green
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)
    
    if not SCORES_FILE.exists():
        with open(SCORES_FILE, 'w') as f:
            json.dump([], f)

def load_scores():
    try:
        with open(SCORE_FILE := CONFIG_DIR / "scores.json", 'r') as f:
            return json.load(f)
    except:
        return []

def save_score(score_entry):
    scores = load_scores()
    scores.append(score_entry)
    # Sort by WPM descending
    scores.sort(key=lambda x: x.get('wpm', 0), reverse=True)
    with open(CONFIG_DIR / "scores.json", 'w') as f:
        json.dump(scores, f, indent=2)

# --- UI HELPERS ---

def draw_box(stdscr, y, x, h, w, title=""):
    try:
        stdscr.attron(curses.color_pair(C_BORDER))
        stdscr.addch(y, x, curses.ACS_ULCORNER)
        stdscr.addch(y, x + w - 1, curses.ACS_URCORNER)
        stdscr.addch(y + h - 1, x, curses.ACS_LLCORNER)
        stdscr.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)
        
        for i in range(1, w - 1):
            stdscr.addch(y, x + i, curses.ACS_HLINE)
            stdscr.addch(y + h - 1, x + i, curses.ACS_HLINE)
        for i in range(1, h - 1):
            stdscr.addch(y + i, x, curses.ACS_VLINE)
            stdscr.addch(y + i, x + w - 1, curses.ACS_VLINE)
            
        if title:
            start_pos = x + (w // 2) - (len(title) // 2)
            stdscr.addstr(y, start_pos, f" {title} ", curses.A_REVERSE | curses.color_pair(C_BORDER))
        stdscr.attroff(curses.color_pair(C_BORDER))
    except curses.error:
        pass

def center_text(text, width):
    padding = (width - len(text)) // 2
    if padding < 0: padding = 0
    return " " * padding + text

# --- GAME LOGIC ---

class TypingSession:
    def __init__(self, stdscr, mode, target_length=None, length_cat=None):
        self.stdscr = stdscr
        self.mode = mode
        self.target_length = target_length
        self.length_cat = length_cat
        self.text = ""
        self.author = ""
        self.topic = ""
        self.user_input = ""
        self.start_time = 0
        self.end_time = 0
        self.finished = False
        self.errors = 0
        self.correct_chars = 0
        self.total_typed = 0
        self.cursor_pos = 0
        self.zen_mode = (mode == "zen")
        self.minimal_stats = False
        
        self.prepare_text()
        self.setup_colors()

    def setup_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(C_NORMAL, curses.COLOR_WHITE, -1)
        curses.init_pair(C_CURSOR, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(C_TYPED_CORRECT, curses.COLOR_BLUE, -1)
        curses.init_pair(C_TYPED_ERROR, curses.COLOR_RED, -1)
        curses.init_pair(C_SUBTLE, curses.COLOR_CYAN, -1)
        curses.init_pair(C_BORDER, curses.COLOR_WHITE, -1)
        curses.init_pair(C_HIGHLIGHT, curses.COLOR_YELLOW, -1)

    def prepare_text(self):
        if self.mode == "custom":
            # Handled in main loop before init usually, but fallback here
            self.text = "Custom text loading..." 
            return
            
        pool = []
        if self.mode == "rand":
            # Filter by approximate length if target_length provided
            if self.target_length:
                tolerance = 10
                min_w = max(5, self.target_length - tolerance)
                max_w = self.target_length + tolerance
                for q in RAW_QUOTES:
                    w_count = len(q["text"].split())
                    if min_w <= w_count <= max_w:
                        pool.append(q)
            if not pool: # Fallback to any random if specific length fails
                pool = RAW_QUOTES
                
        elif self.mode == "quote":
            pool = RAW_QUOTES
        elif self.mode in ["short", "medium", "long", "longest"]:
            pool = QUOTE_DB.get(self.mode, RAW_QUOTES)
        elif self.mode == "zen":
             pool = RAW_QUOTES # Zen uses random quotes usually
        else:
            pool = RAW_QUOTES

        selected = random.choice(pool)
        self.text = selected["text"]
        self.author = selected.get("author", "Unknown")
        self.topic = selected.get("topic", "General")

    def calculate_stats(self):
        duration = max(1, self.end_time - self.start_time)
        minutes = duration / 60.0
        wpm = round((self.correct_chars / 5) / minutes, 1) if minutes > 0 else 0
        accuracy = round((self.correct_chars / max(1, self.total_typed)) * 100, 1)
        return {
            "wpm": wpm,
            "accuracy": accuracy,
            "errors": self.errors,
            "correct": self.correct_chars,
            "total": len(self.text),
            "duration": round(duration, 2),
            "mode": self.mode,
            "length_cat": self.length_cat or self.mode,
            "timestamp": datetime.now().isoformat()
        }

    def render(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        # Draw Border
        box_h, box_w = h - 4, w - 4
        start_y, start_x = 2, 2
        draw_box(self.stdscr, start_y, start_x, box_h, box_w, f"Scribere [{self.mode.upper()}]")
        
        # Render Text
        display_text = self.text
        input_len = len(self.user_input)
        
        # Wrap text logic simplified for terminal (assume fits or simple scroll)
        # For true multiline wrap, we'd need complex logic. 
        # Minimalist approach: Center the block.
        
        lines = []
        current_line = ""
        for char in display_text:
            if len(current_line) + 1 > w - 8: # Break before border
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        if current_line:
            lines.append(current_line)
            
        # Calculate start Y to center vertically
        total_lines = len(lines)
        text_start_y = start_y + (box_h // 2) - (total_lines // 2)
        
        char_idx = 0
        for l_idx, line in enumerate(lines):
            y_pos = text_start_y + l_idx
            if y_pos >= start_y + box_h - 1: break
            
            line_start_x = start_x + 2 # Padding inside box
            
            for c_idx, char in enumerate(line):
                x_pos = line_start_x + c_idx
                if x_pos >= start_x + box_w - 2: continue
                
                if char_idx >= input_len:
                    # Not typed yet
                    if char_idx == input_len and not self.finished:
                        # Cursor position
                        try:
                            self.stdscr.addch(y_pos, x_pos, char, curses.color_pair(C_CURSOR) | curses.A_BOLD)
                        except: pass
                    else:
                        try:
                            self.stdscr.addch(y_pos, x_pos, char, curses.color_pair(C_NORMAL))
                        except: pass
                else:
                    # Typed
                    user_char = self.user_input[char_idx]
                    if user_char == char:
                        try:
                            self.stdscr.addch(y_pos, x_pos, char, curses.color_pair(C_TYPED_CORRECT) | curses.A_BOLD)
                        except: pass
                    else:
                        try:
                            self.stdscr.addch(y_pos, x_pos, char, curses.color_pair(C_TYPED_ERROR) | curses.A_UNDERLINE)
                        except: pass
                char_idx += 1

        # Status Bar
        status_y = h - 2
        if self.zen_mode and not self.finished:
            status_msg = "ZEN MODE: Type freely. Press SHIFT+ENTER to finish."
        elif self.finished:
            status_msg = "Test Complete. Press ENTER to see results, 'M' for High Scores."
        else:
            stats = self.calculate_stats() # Live calc
            if self.minimal_stats:
                status_msg = f"WPM: {stats['wpm']} | Acc: {stats['accuracy']}%"
            else:
                status_msg = f"Time: {int(time.time() - self.start_time)}s | Errors: {self.errors} | WPM: {stats['wpm']}"
        
        try:
            self.stdscr.addstr(status_y, 2, status_msg[:w-4], curses.color_pair(C_SUBTLE) | curses.A_BOLD)
        except: pass
        
        self.stdscr.refresh()

    def run(self):
        self.start_time = time.time()
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)
        curses.curs_set(0) # Hide system cursor

        while True:
            self.render()
            key = self.stdscr.getch()
            
            if key == 27: # ESC
                return None # Quit
            
            if self.finished:
                if key == 10 or key == 13: # Enter
                    return self.calculate_stats()
                if key == ord('m') or key == ord('M'):
                    show_highscores(self.stdscr, self.calculate_stats())
                    self.render() # Redraw after menu
                if key == ord('d') or key == ord('D'):
                    self.minimal_stats = not self.minimal_stats
                continue

            # Typing Logic
            if key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                if len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]
            elif key == 10 or key == 13: # Enter
                if self.zen_mode:
                    # Check if Shift was held? Curses doesn't easily detect shift+enter combo cleanly across all terminals without raw mode complexity.
                    # Heuristic: In Zen mode, Enter finishes.
                    self.finished = True
                    self.end_time = time.time()
            elif 32 <= key <= 126: # Printable
                char = chr(key)
                self.user_input += char
                self.total_typed += 1
                
                if len(self.user_input) <= len(self.text):
                    idx = len(self.user_input) - 1
                    if self.user_input[idx] == self.text[idx]:
                        self.correct_chars += 1
                    else:
                        self.errors += 1
                
                # Auto finish if text completed
                if len(self.user_input) == len(self.text):
                    self.finished = True
                    self.end_time = time.time()

def show_highscores(stdscr, current_score=None):
    scores = load_scores()
    if current_score:
        save_score(current_score)
        scores = load_scores() # Reload
    
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    # Simple Menu
    title = "HIGH SCORES (M to Close, Arrows to Scroll)"
    draw_box(stdscr, 1, 1, h-2, w-2, title)
    
    start_y = 4
    max_entries = h - 8
    
    # Display top scores
    for i, score in enumerate(scores[:max_entries]):
        y = start_y + i
        if y >= h - 3: break
        msg = f"#{i+1} {score['wpm']} WPM | {score['accuracy']}% | {score['mode']} | {score['timestamp'][:10]}"
        try:
            stdscr.addstr(y, 4, msg, curses.color_pair(C_NORMAL))
        except: pass
    
    if current_score:
        msg = f"YOUR RESULT: {current_score['wpm']} WPM"
        try:
            stdscr.addstr(h-4, 4, msg, curses.color_pair(C_HIGHLIGHT) | curses.A_BOLD)
        except: pass
        
    stdscr.refresh()
    while True:
        k = stdscr.getch()
        if k == ord('m') or k == ord('M') or k == 27:
            break

def custom_input_loop(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    draw_box(stdscr, 2, 2, h-4, w-4, "CUSTOM TEXT INPUT")
    stdscr.addstr(4, 4, "Type or paste your text below. Press ESC when done.")
    stdscr.addstr(5, 4, "> ")
    stdscr.refresh()
    
    curses.echo()
    stdscr.nodelay(False)
    input_text = ""
    
    # Simple single line input for minimalism, or multi-line? 
    # Let's do multi-line until ESC
    temp_win = curses.newwin(h-8, w-8, 7, 4)
    temp_win.keypad(True)
    temp_win.refresh()
    
    lines = []
    while True:
        key = temp_win.getch()
        if key == 27: # ESC
            break
        if key == 10: # Enter
            lines.append("")
        elif key == curses.KEY_BACKSPACE:
            if lines and len(lines[-1]) == 0:
                if len(lines) > 0: lines.pop()
            elif lines:
                lines[-1] = lines[-1][:-1]
        elif 32 <= key <= 126:
            if not lines: lines.append("")
            lines[-1] += chr(key)
        
        temp_win.clear()
        for i, line in enumerate(lines):
            try: temp_win.addstr(i, 0, line)
            except: pass
        temp_win.refresh()
    
    curses.noecho()
    return " ".join(lines)

def main_curses(stdscr, args):
    ensure_config()
    mode = args[0] if args else "rand"
    target_len = None
    
    # Parse arguments like "rand-25"
    if mode.startswith("rand-"):
        try:
            target_len = int(mode.split("-")[1])
            mode = "rand"
        except:
            mode = "rand"
    
    session = None
    
    if mode == "custom":
        text = custom_input_loop(stdscr)
        if not text.strip():
            return
        # Create a dummy session then override text
        session = TypingSession(stdscr, "custom")
        session.text = text
        session.author = "Custom"
        session.topic = "User"
    else:
        # Determine length category if mode is specific
        cat = None
        if mode in ["short", "medium", "long", "longest"]:
            cat = mode
        session = TypingSession(stdscr, mode, target_length=target_len, length_cat=cat)
    
    result = session.run()
    
    if result:
        # Results Screen
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_box(stdscr, 2, 2, h-4, w-4, "RESULTS")
        
        mid_y = h // 2
        stats = [
            f"WPM: {result['wpm']}",
            f"Accuracy: {result['accuracy']}%",
            f"Errors: {result['errors']}",
            f"Chars: {result['correct']}/{result['total']}",
            f"Time: {result['duration']}s"
        ]
        
        for i, line in enumerate(stats):
            try:
                stdscr.addstr(mid_y - 2 + i, w//2 - 10, line, curses.A_BOLD | curses.color_pair(C_TYPED_CORRECT))
            except: pass
            
        stdscr.addstr(h-4, 4, "Press ENTER to continue, M for High Scores, D to toggle stats detail", curses.color_pair(C_SUBTLE))
        stdscr.refresh()
        
        # Loop for post-game actions handled in session.run() usually, 
        # but here we just exit to let the wrapper handle restart or quit
        stdscr.getch()

def run_app(args):
    try:
        curses.wrapper(lambda stdscr: main_curses(stdscr, args))
    except Exception as e:
        print(f"Scribere Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # CLI Entry Point
    if len(sys.argv) > 1:
        run_app(sys.argv[1:])
    else:
        print("Scribere v" + VERSION)
        print("Usage: scribere start [mode]")
        print("Modes: rand-25, short, medium, long, longest, zen, custom, quote")
        print("Example: scribere start rand-25")