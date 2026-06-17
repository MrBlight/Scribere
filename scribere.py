#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scribere - A hyper-minimalist terminal typing tutor.
License: GNU GPL v3
"""

import curses
import random
import time
import os
import json
import sys
import urllib.request
import io

# Try to import Pillow for the easter egg
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- Configuration & Data ---

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".scribere")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SCORES_FILE = os.path.join(CONFIG_DIR, "scores.json")

# Common Words Bank (Frequency weighted by repetition)
BASE_WORDS = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what", "so",
    "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
    "make", "can", "like", "time", "no", "just", "him", "know", "take", "people",
    "into", "year", "your", "good", "some", "could", "them", "see", "other", "than",
    "then", "now", "look", "only", "come", "its", "over", "think", "also", "back",
    "after", "use", "two", "how", "our", "work", "first", "well", "way", "even",
    "new", "want", "because", "any", "these", "give", "day", "most", "us", "is",
    "house", "school", "fight", "although", "through", "water", "money", "world", "place", "group",
    "hand", "high", "part", "child", "eye", "woman", "life", "down", "head", "stand",
    "own", "page", "should", "country", "found", "answer", "study", "still", "learn", "parent",
    "face", "friend", "mother", "father", "city", "line", "near", "far", "door", "room", "floor",
    "book", "letter", "word", "sentence", "paper", "idea", "question", "change", "order", "number",
    "start", "end", "road", "map", "car", "bus", "train", "plane", "boat", "bike",
    "dog", "cat", "bird", "fish", "tree", "flower", "grass", "sun", "moon", "star",
    "sky", "cloud", "rain", "snow", "wind", "fire", "earth", "stone", "sand", "hill",
    "river", "lake", "sea", "ocean", "bridge", "tower", "wall", "gate", "fence", "path",
    "food", "bread", "milk", "egg", "meat", "fruit", "apple", "orange", "banana", "grape",
    "cake", "sugar", "salt", "pepper", "coffee", "tea", "juice", "beer", "wine", "water",
    "hot", "cold", "warm", "cool", "dry", "wet", "hard", "soft", "heavy", "light",
    "fast", "slow", "old", "young", "big", "small", "long", "short", "wide", "narrow",
    "thick", "thin", "deep", "shallow", "high", "low", "loud", "quiet", "bright", "dark",
    "clean", "dirty", "full", "empty", "open", "closed", "safe", "dangerous", "easy", "hard",
    "happy", "sad", "angry", "afraid", "tired", "hungry", "thirsty", "sick", "healthy", "strong",
    "weak", "rich", "poor", "kind", "mean", "nice", "rude", "smart", "stupid", "funny",
    "serious", "busy", "free", "early", "late", "soon", "never", "always", "often", "sometimes",
    "here", "there", "everywhere", "nowhere", "somewhere", "inside", "outside", "above", "below", "between",
    "before", "behind", "next", "last", "first", "second", "third", "fourth", "fifth", "tenth",
    "dig", "wish", "send", "folk", "musician", "music", "rock", "pop", "jazz", "electronic",
    "man", "cost", "talking", "shop", "fly", "european", "african", "asian", "balkan",
    "meme", "liquid", "tiny", "large", "kid", "silly", "wise", "lost", "half",
    "however", "black", "white", "frog", "sour", "bitter", "sweet", "computer", "eat", "chocolate",
    "great", "awesome", "taste", "wrong", "right", "true", "truth", "false", "fake", "ice",
    "miller", "care", "game", "sound"
]

COMMON_WORDS = []
for word in BASE_WORDS:
    if word in ["the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "on", "with", "he", "as", "you", "do", "at"]:
        COMMON_WORDS.extend([word] * 8)
    elif word in ["this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all"]:
        COMMON_WORDS.extend([word] * 5)
    else:
        COMMON_WORDS.append(word)

COMPLEX_WORDS = [
    "phallus", "beryllium", "doctorate", "ephemeral", "quintessential", "serendipity", "ubiquitous",
    "cacophony", "juxtaposition", "mitochondria", "photosynthesis", "algorithm", "cryptography",
    "philosophy", "metaphysics", "epistemology", "existentialism", "nihilism", "stoicism",
    "renaissance", "enlightenment", "industrialization", "globalization", "sustainability",
    "bureaucracy", "aristocracy", "democracy", "totalitarianism", "authoritarianism",
    "psychology", "psychoanalysis", "behaviorism", "cognitive", "neuroscience", "consciousness",
    "quantum", "relativity", "thermodynamics", "electromagnetism", "gravitation", "cosmology",
    "architecture", "engineering", "mathematics", "calculus", "geometry", "algebra", "statistics",
    "literature", "poetry", "prose", "fiction", "nonfiction", "biography", "autobiography",
    "impressionism", "expressionism", "surrealism", "cubism", "abstract", "realism", "romanticism",
    "constitution", "legislation", "jurisprudence", "litigation", "arbitration", "mediation",
    "economics", "microeconomics", "macroeconomics", "capitalism", "socialism", "communism",
    "anthropology", "sociology", "archaeology", "linguistics", "semantics", "phonetics",
    "biology", "zoology", "botany", "ecology", "genetics", "evolution", "mutation", "adaptation",
    "chemistry", "organic", "inorganic", "biochemistry", "molecular", "atomic", "nuclear",
    "physics", "mechanics", "optics", "acoustics", "magnetism", "electricity", "energy",
    "astronomy", "astrophysics", "planetary", "stellar", "galactic", "universal", "cosmic",
    "geology", "mineralogy", "petrology", "volcanology", "seismology", "meteorology", "climatology",
    "oceanography", "hydrology", "glaciology", "geomorphology", "paleontology", "stratigraphy",
    "medicine", "anatomy", "physiology", "pathology", "pharmacology", "immunology", "oncology",
    "cardiology", "neurology", "psychiatry", "dermatology", "pediatrics", "geriatrics",
    "surgery", "orthopedics", "obstetrics", "gynecology", "urology", "ophthalmology", "otolaryngology",
    "dentistry", "orthodontics", "periodontics", "endodontics", "oral", "maxillofacial",
    "veterinary", "agriculture", "horticulture", "silviculture", "aquaculture", "apiculture",
    "culinary", "gastronomy", "oenology", "viticulture", "brewing", "distilling", "baking",
    "textile", "fabric", "weaving", "knitting", "sewing", "embroidery", "tailoring", "fashion",
    "ceramics", "pottery", "sculpture", "painting", "drawing", "printmaking", "photography",
    "cinema", "theater", "dance", "music", "opera", "ballet", "symphony", "concerto", "sonata",
    "jazz", "blues", "rock", "pop", "folk", "classical", "electronic", "hiphop", "reggae", "country"
]

TEMPLATES = [
    "{noun} {verb} {adj} {noun}.",
    "The {adj} {noun} {verb} {adv}.",
    "{pronoun} {verb} the {adj} {noun}.",
    "Can {pronoun} {verb} {adj} {noun}?",
    "Why is the {noun} so {adj}?",
    "{noun} and {noun} are {adj}.",
    "I see a {adj} {noun}.",
    "Do not {verb} the {noun}.",
    "It is {adj} to {verb} {noun}.",
    "{pronoun} will {verb} {noun} tomorrow.",
    "The {noun} is {verb}ing.",
    "Many {noun}s are {adj}.",
    "She likes {adj} {noun}s.",
    "He went to the {noun}.",
    "We need more {noun}.",
    "Where is the {noun}?",
    "This {noun} looks {adj}.",
    "They are {verb}ing the {noun}.",
    "No {noun} here.",
    "Just {verb} it."
]

TEMPLATE_FILLERS = {
    "noun": BASE_WORDS[:50],
    "verb": ["run", "jump", "eat", "sleep", "walk", "talk", "see", "hear", "feel", "think", "make", "take", "go", "come", "work", "play", "live", "love", "hate", "fight"],
    "adj": ["big", "small", "red", "blue", "green", "fast", "slow", "hot", "cold", "good", "bad", "new", "old", "high", "low", "bright", "dark", "happy", "sad", "wise"],
    "adv": ["quickly", "slowly", "loudly", "quietly", "happily", "sadly", "well", "badly", "very", "too"],
    "pronoun": ["I", "you", "he", "she", "it", "we", "they"]
}

def ensure_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "color_theme": "default",
            "minimal_stats": False,
            "word_bank": "common",
            "smart_sentences": False,
            "word_count": 25,
            "mode": "rand"
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f)
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            json.dump([], f)

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"word_bank": "common", "smart_sentences": False, "minimal_stats": False, "word_count": 25, "mode": "rand"}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_scores():
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def get_random_words(count, word_bank="common", smart=False):
    if word_bank == "complex":
        source = COMPLEX_WORDS
    else:
        source = COMMON_WORDS
    
    if smart:
        sentences = []
        while len(" ".join(sentences).split()) < count:
            template = random.choice(TEMPLATES)
            sentence = template
            for key in TEMPLATE_FILLERS:
                sentence = sentence.replace("{" + key + "}", random.choice(TEMPLATE_FILLERS[key]))
            sentences.append(sentence)
        result = " ".join(sentences)
        words = result.split()[:count]
        return " ".join(words)
    else:
        return " ".join(random.choice(source) for _ in range(count))

def fetch_and_convert_image(url):
    if not PIL_AVAILABLE:
        return ["Pillow library not installed.", "Run: pip install Pillow"]
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        img_data = response.read()
        img = Image.open(io.BytesIO(img_data))
        width = 80
        height = int(width * (img.height / img.width) * 0.5)
        img = img.convert('L').resize((width, height), Image.Resampling.LANCZOS)
        pixels = list(img.getdata())
        chars = "@%#*+=-:. "
        ascii_lines = []
        for i in range(height):
            line = ""
            for j in range(width):
                pixel = pixels[i * width + j]
                char_idx = int(pixel / 255 * (len(chars) - 1))
                line += chars[char_idx]
            ascii_lines.append(line)
        return ascii_lines
    except Exception as e:
        return [f"Error loading image: {str(e)}", "Check internet connection."]

# --- UI Components ---

class MainMenu:
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.config = config
        self.options = [
            {"label": "Start Typing Test", "action": "start"},
            {"label": "Settings", "action": "settings"},
            {"label": "High Scores", "action": "scores"},
            {"label": "Secret Easter Egg", "action": "secret"},
            {"label": "Quit", "action": "quit"}
        ]
        self.selected = 0
        self.running = True
        self.next_action = None

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        title = " SCRIBERE "
        self.stdscr.addstr(2, (w - len(title)) // 2, title, curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE)
        
        subtitle = " Hyper-minimalist typing tutor "
        self.stdscr.addstr(3, (w - len(subtitle)) // 2, subtitle, curses.color_pair(5) | curses.A_DIM)
        
        menu_start = 6
        for i, opt in enumerate(self.options):
            label = opt["label"]
            x = (w - len(label)) // 2
            if i == self.selected:
                self.stdscr.addstr(menu_start + i, x, f"> {label} <", curses.color_pair(6) | curses.A_BOLD)
            else:
                self.stdscr.addstr(menu_start + i, x, f"  {label}  ", curses.color_pair(4))
        
        footer = " Use ↑/↓ to navigate, Enter to select "
        self.stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.color_pair(5) | curses.A_DIM)
        self.stdscr.refresh()

    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(False)
        while self.running:
            self.draw()
            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif key == curses.KEY_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif key == 10 or key == curses.KEY_ENTER:
                self.next_action = self.options[self.selected]["action"]
                self.running = False
            elif key == 27: # ESC
                self.next_action = "quit"
                self.running = False
        return self.next_action

class SettingsMenu:
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.config = config
        self.rows = [
            {"key": "mode", "label": "Mode", "values": ["rand", "zen"]},
            {"key": "word_count", "label": "Word Count", "values": [10, 25, 50, 100, 200]},
            {"key": "word_bank", "label": "Word Bank", "values": ["common", "complex"]},
            {"key": "smart_sentences", "label": "Smart Sentences", "values": [False, True]},
            {"key": "minimal_stats", "label": "Minimal Stats", "values": [False, True]}
        ]
        self.selected_row = 0
        self.running = True

    def get_val(self, key):
        return self.config.get(key)

    def set_val(self, key, val):
        self.config[key] = val
        save_config(self.config)

    def cycle(self, key):
        current = self.get_val(key)
        row_idx = next(i for i, r in enumerate(self.rows) if r["key"] == key)
        values = self.rows[row_idx]["values"]
        idx = values.index(current)
        next_val = values[(idx + 1) % len(values)]
        self.set_val(key, next_val)

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        title = " SETTINGS "
        self.stdscr.addstr(2, (w - len(title)) // 2, title, curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE)
        
        for i, row in enumerate(self.rows):
            key = row["key"]
            label = row["label"]
            val = self.get_val(key)
            val_str = str(val).upper()
            
            line = f"{label}: {val_str}"
            x = (w - len(line)) // 2
            y = 5 + i * 2
            
            if i == self.selected_row:
                self.stdscr.addstr(y, x - 2, f"> {line} <", curses.color_pair(6) | curses.A_BOLD)
            else:
                self.stdscr.addstr(y, x, f"  {line}  ", curses.color_pair(4))
        
        footer = " ↑/↓ to change selection, Enter to toggle, Esc to save "
        self.stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.color_pair(5) | curses.A_DIM)
        self.stdscr.refresh()

    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(False)
        while self.running:
            self.draw()
            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                self.selected_row = (self.selected_row - 1) % len(self.rows)
            elif key == curses.KEY_DOWN:
                self.selected_row = (self.selected_row + 1) % len(self.rows)
            elif key == 10 or key == curses.KEY_ENTER:
                self.cycle(self.rows[self.selected_row]["key"])
            elif key == 27:
                self.running = False
        return self.config

class TypingApp:
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.config = config
        self.mode = config.get("mode", "rand")
        self.target_count = config.get("word_count", 25)
        self.word_bank = config.get("word_bank", "common")
        self.smart_mode = config.get("smart_sentences", False)
        
        self.text = ""
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.cursor_pos = 0
        self.errors = 0
        self.total_chars_typed = 0
        self.show_menu = False
        
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_WHITE, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        
        self.setup_text()
        self.running = True

    def setup_text(self):
        self.text = get_random_words(self.target_count, self.word_bank, self.smart_mode)
        if not self.text: self.text = "Error."

    def draw_screen(self):
        if self.show_menu:
            self.draw_pause_menu()
            return

        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        try:
            self.stdscr.box()
            self.stdscr.attron(curses.color_pair(5))
            self.stdscr.box()
            self.stdscr.attroff(curses.color_pair(5))
        except: pass

        title = f" SCRIBERE ({self.mode.upper()}) "
        self.stdscr.addstr(0, (width - len(title)) // 2, title, curses.color_pair(5) | curses.A_BOLD)

        status = f" Words: {self.target_count} | Bank: {self.word_bank} "
        if self.finished: status = " TEST COMPLETE "
        self.stdscr.addstr(2, 2, status, curses.color_pair(5))

        start_row = 4
        max_rows = height - 8
        max_cols = width - 4
        
        wrapped_lines = []
        current_line = ""
        for char in self.text:
            if len(current_line) + 1 > max_cols:
                wrapped_lines.append(current_line)
                current_line = char
            else:
                current_line += char
        if current_line: wrapped_lines.append(current_line)
        
        flat_cursor = min(self.cursor_pos, len(self.text))
        current_flat = 0
        cursor_line_idx = 0
        for l_idx, line in enumerate(wrapped_lines):
            if current_flat + len(line) >= flat_cursor:
                cursor_line_idx = l_idx
                break
            current_flat += len(line)
        
        scroll_offset = 0
        if cursor_line_idx >= max_rows:
            scroll_offset = cursor_line_idx - max_rows + 1
        
        visible_lines = wrapped_lines[scroll_offset : scroll_offset + max_rows]
        global_flat_idx = sum(len(l) for l in wrapped_lines[:scroll_offset])
        
        for r_idx, line in enumerate(visible_lines):
            screen_r = start_row + r_idx
            if screen_r >= height - 2: break
            
            for c_idx, char in enumerate(line):
                char_idx_global = global_flat_idx + c_idx
                attr = curses.color_pair(4)
                
                if char_idx_global < len(self.user_input):
                    u_char = self.user_input[char_idx_global]
                    if u_char == char: attr = curses.color_pair(1)
                    else: attr = curses.color_pair(2)
                
                if char_idx_global == flat_cursor and not self.finished:
                    attr = curses.color_pair(3) | curses.A_REVERSE
                
                try: self.stdscr.addch(screen_r, 2 + c_idx, char, attr)
                except: pass
            
            global_flat_idx += len(line)

        if self.finished:
            self.draw_results(start_row + max_rows + 1, width)
        else:
            wpm = 0
            if self.start_time:
                elapsed = (time.time() - self.start_time) / 60.0
                if elapsed > 0: wpm = int((len(self.user_input) / 5.0) / elapsed)
            stats_str = f" WPM: {wpm} | Acc: {self.get_accuracy():.1f}% | Err: {self.errors} "
            self.stdscr.addstr(height - 2, 2, stats_str, curses.color_pair(5) | curses.A_DIM)
        
        self.stdscr.refresh()

    def draw_pause_menu(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()
        menu_h, menu_w = 10, 40
        start_y, start_x = (h - menu_h) // 2, (w - menu_w) // 2
        win = curses.newwin(menu_h, menu_w, start_y, start_x)
        win.box()
        win.keypad(True)
        win.addstr(0, (menu_w - 6) // 2, " PAUSED ", curses.color_pair(5) | curses.A_BOLD)
        opts = ["Resume", "Restart", "Settings", "Main Menu", "Quit"]
        for i, o in enumerate(opts):
            win.addstr(2 + i, 2, f"{i+1}. {o}", curses.color_pair(6))
        win.addstr(menu_h - 2, 2, " Select 1-5 or Esc ", curses.color_pair(5) | curses.A_DIM)
        win.refresh()
        
        while True:
            key = win.getch()
            if key == 27 or key == ord('q'): self.show_menu = False; break
            elif key == ord('1'): self.show_menu = False; break
            elif key == ord('2'): self.reset_test(); self.show_menu = False; break
            elif key == ord('3'): 
                # Open settings inline? For now just resume to keep simple
                self.show_menu = False; break
            elif key == ord('4'): self.running = False; self.next_action = "main_menu"; break
            elif key == ord('5'): self.running = False; self.next_action = "quit"; break

    def reset_test(self):
        # Reload config in case changed
        self.config = load_config()
        self.mode = self.config.get("mode", "rand")
        self.target_count = self.config.get("word_count", 25)
        self.word_bank = self.config.get("word_bank", "common")
        self.smart_mode = self.config.get("smart_sentences", False)
        
        self.text = get_random_words(self.target_count, self.word_bank, self.smart_mode)
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.cursor_pos = 0
        self.errors = 0
        self.total_chars_typed = 0

    def get_accuracy(self):
        if len(self.user_input) == 0: return 100.0
        correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.text) and c == self.text[i])
        return (correct / len(self.user_input)) * 100

    def draw_results(self, row, width):
        elapsed = (self.end_time - self.start_time) if (self.start_time and self.end_time) else 0
        wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0)) if elapsed > 0 else 0
        acc = self.get_accuracy()
        
        self.stdscr.addstr(row, (width - 9) // 2, " RESULTS ", curses.color_pair(5) | curses.A_BOLD)
        minimal = self.config.get("minimal_stats", False)
        stats = f" WPM: {wpm} | Acc: {acc:.1f}% " if minimal else f" WPM: {wpm} | Acc: {acc:.1f}% | Err: {self.errors} | Time: {elapsed:.1f}s "
        self.stdscr.addstr(row + 2, 2, stats, curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(row + 4, 2, " Enter: Retry | M: Scores | Esc: Menu ", curses.color_pair(5) | curses.A_DIM)

    def handle_input(self, key):
        if self.show_menu: return # Handled in draw

        if self.finished:
            if key == 10 or key == curses.KEY_ENTER: self.reset_test()
            elif key == ord('m') or key == ord('M'): self.show_highscores()
            elif key == 27: self.show_menu = True
            return

        if key == 27:
            self.show_menu = True
            return

        if self.mode == 'zen' and (key == 10 or key == curses.KEY_ENTER or key == 343): 
             self.finish_test()
             return

        if key in (curses.KEY_BACKSPACE, 127, 8):
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                if len(self.user_input) > 0: self.user_input = self.user_input[:-1]
        elif key == curses.KEY_LEFT:
            if self.cursor_pos > 0: self.cursor_pos -= 1
        elif key == curses.KEY_RIGHT:
            if self.cursor_pos < len(self.text): self.cursor_pos += 1
        elif 32 <= key <= 126:
            if self.cursor_pos < len(self.text):
                char = chr(key)
                if self.cursor_pos == len(self.user_input):
                    self.user_input += char
                else:
                    # Overwrite if moving cursor back and forth
                    if self.cursor_pos < len(self.user_input):
                         self.user_input = self.user_input[:self.cursor_pos] + char + self.user_input[self.cursor_pos+1:]
                    else:
                         self.user_input += char
                
                # Only count error if the char we just typed is wrong
                if self.user_input[self.cursor_pos] != self.text[self.cursor_pos]:
                     self.errors += 1
                    
                self.cursor_pos += 1
                self.total_chars_typed += 1
                if self.cursor_pos == len(self.text): self.finish_test()
        
        if not self.finished and self.start_time is None and len(self.user_input) > 0:
            self.start_time = time.time()

    def finish_test(self):
        if not self.finished:
            self.finished = True
            self.end_time = time.time()
            self.save_score()

    def save_score(self):
        elapsed = (self.end_time - self.start_time) if (self.end_time and self.start_time) else 0
        wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0)) if elapsed > 0 else 0
        acc = self.get_accuracy()
        score_entry = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "mode": self.mode,
            "word_bank": self.word_bank,
            "smart": self.smart_mode,
            "wpm": wpm, "accuracy": acc, "errors": self.errors, "chars": len(self.user_input)
        }
        scores = load_scores()
        scores.append(score_entry)
        scores.sort(key=lambda x: x['wpm'], reverse=True)
        save_scores(scores[:100])

    def show_highscores(self):
        scores = load_scores()
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(2, (w-11)//2, " HIGH SCORES ", curses.color_pair(5) | curses.A_BOLD)
        if not scores:
            self.stdscr.addstr(5, 5, "No scores yet.", curses.color_pair(4))
        else:
            self.stdscr.addstr(4, 5, "Date       Mode    WPM  Acc%   Bank", curses.color_pair(5))
            for i, s in enumerate(scores[:15]):
                bank = s.get('word_bank', 'N/A') + (" (S)" if s.get('smart') else "")
                line = f"{s['date']} {s['mode']:<6} {s['wpm']:>3} {s['accuracy']:>5.1f}   {bank}"
                try: self.stdscr.addstr(6 + i, 5, line, curses.color_pair(1 if i == 0 else 4))
                except: pass
        self.stdscr.addstr(h-2, 2, " Press Enter to close ", curses.color_pair(5) | curses.A_DIM)
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        while True:
            k = self.stdscr.getch()
            if k == 10 or k == curses.KEY_ENTER: break
        self.stdscr.nodelay(True)

    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.next_action = None
        while self.running:
            self.draw_screen()
            try:
                key = self.stdscr.getch()
                if key != -1: self.handle_input(key)
            except KeyboardInterrupt: break
        curses.curs_set(1)
        return self.next_action

def show_secret(stdscr):
    stdscr.clear()
    stdscr.nodelay(False)
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, (w-14)//2, " SECRET FOUND ", curses.color_pair(5) | curses.A_BOLD)
    lines = fetch_and_convert_image("https://f4.bcbits.com/img/a1664460568_10.jpg")
    start_y = 2
    for i, line in enumerate(lines):
        if start_y + i >= h - 2: break
        x_pos = max(0, (w - len(line)) // 2)
        try: stdscr.addstr(start_y + i, x_pos, line, curses.color_pair(1))
        except: pass
    stdscr.addstr(h - 2, (w - 20) // 2, " Press any key...", curses.color_pair(5) | curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()

def main_loop(stdscr):
    ensure_config()
    config = load_config()
    
    while True:
        # 1. Main Menu
        menu = MainMenu(stdscr, config)
        action = menu.run()
        
        if action == "quit": break
        elif action == "settings":
            settings = SettingsMenu(stdscr, config)
            config = settings.run()
        elif action == "scores":
            # Inline scores view
            scores = load_scores()
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            stdscr.addstr(2, (w-11)//2, " HIGH SCORES ", curses.color_pair(5) | curses.A_BOLD)
            if not scores: stdscr.addstr(5, 5, "No scores yet.", curses.color_pair(4))
            else:
                stdscr.addstr(4, 5, "Date       Mode    WPM  Acc%   Bank", curses.color_pair(5))
                for i, s in enumerate(scores[:15]):
                    bank = s.get('word_bank', 'N/A') + (" (S)" if s.get('smart') else "")
                    line = f"{s['date']} {s['mode']:<6} {s['wpm']:>3} {s['accuracy']:>5.1f}   {bank}"
                    try: stdscr.addstr(6 + i, 5, line, curses.color_pair(1 if i == 0 else 4))
                    except: pass
            stdscr.addstr(h-2, 2, " Press Enter to return ", curses.color_pair(5) | curses.A_DIM)
            stdscr.refresh()
            stdscr.nodelay(False)
            stdscr.getch()
            stdscr.nodelay(True)
        elif action == "secret":
            show_secret(stdscr)
        elif action == "start":
            # 2. Start Typing
            app = TypingApp(stdscr, config)
            next_act = app.run()
            if next_act == "main_menu": continue
            elif next_act == "quit": break
            elif next_act == "settings":
                settings = SettingsMenu(stdscr, config)
                config = settings.run()

if __name__ == "__main__":
    try:
        curses.wrapper(main_loop)
    except Exception as e:
        print(f"Error: {e}")
        if not PIL_AVAILABLE and "secret" in str(e):
            print("Note: Install Pillow for the secret image feature.")
        sys.exit(1)
