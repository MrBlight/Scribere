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
import argparse
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
    # Extra flavor words
    "dig", "wish", "send", "folk", "musician", "music", "rock", "pop", "jazz", "electronic",
    "man", "cost", "talking", "shop", "fly", "european", "african", "asian", "balkan",
    "meme", "liquid", "tiny", "large", "kid", "silly", "wise", "lost", "half",
    "however", "black", "white", "frog", "sour", "bitter", "sweet", "computer", "eat", "chocolate",
    "great", "awesome", "taste", "wrong", "right", "true", "truth", "false", "fake", "ice",
    "miller", "care", "game", "sound"
]

# Weighted list: Common words appear multiple times to increase frequency
COMMON_WORDS = []
for word in BASE_WORDS:
    if word in ["the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "on", "with", "he", "as", "you", "do", "at"]:
        COMMON_WORDS.extend([word] * 8)  # Very high frequency
    elif word in ["this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all"]:
        COMMON_WORDS.extend([word] * 5)  # High frequency
    else:
        COMMON_WORDS.append(word)        # Normal frequency

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

# Smart Sentence Templates
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
            "smart_sentences": False
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
        return {"word_bank": "common", "smart_sentences": False, "minimal_stats": False}

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

# --- Easter Egg Logic (Fixed) ---

def fetch_and_convert_image(url):
    if not PIL_AVAILABLE:
        return ["Pillow library not installed.", "Run: pip install Pillow"]
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        img_data = response.read()
        
        img = Image.open(io.BytesIO(img_data))
        
        # Get terminal size
        # We will calculate this dynamically in the display function, 
        # but here we prepare a high-res version to be scaled later if needed.
        # For now, we just return the image object to be processed per-frame or once.
        return img
        
    except Exception as e:
        return None

def render_ascii_frame(stdscr, img):
    h_term, w_term = stdscr.getmaxyx()
    
    # Calculate max available area (leave some padding)
    max_h = h_term - 4
    max_w = w_term - 4
    
    if max_h <= 0 or max_w <= 0:
        return

    # Terminal characters are roughly twice as tall as they are wide.
    # To prevent stretching, we scale height by 0.5 relative to width.
    aspect_ratio = img.width / img.height
    new_w = max_w
    new_h = int(max_w / aspect_ratio * 0.55) # 0.55 compensates for char aspect ratio
    
    if new_h > max_h:
        new_h = max_h
        new_w = int(max_h * aspect_ratio / 0.55)

    # Resize image to fit terminal
    img_resized = img.convert('L').resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    pixels = list(img_resized.getdata())
    
    # Binary threshold for sharp contrast (Smiling picture style)
    threshold = 128 
    
    lines = []
    for i in range(new_h):
        line = ""
        for j in range(new_w):
            pixel = pixels[i * new_w + j]
            if pixel < threshold:
                line += "█" # Dark pixel
            else:
                line += " " # Light pixel
        lines.append(line)
    
    # Center and draw
    start_y = (h_term - len(lines)) // 2
    start_x = (w_term - len(lines[0])) // 2 if lines else 0
    
    for i, line in enumerate(lines):
        y = start_y + i
        x = start_x
        if 0 <= y < h_term:
            try:
                # Draw the line. Since it's mixed chars, we just addstr.
                # We truncate if line is too long for window
                safe_line = line[:w_term-1]
                stdscr.addstr(y, max(0, x), safe_line, curses.A_BOLD)
            except curses.error:
                pass

def show_secret_screen(stdscr):
    stdscr.clear()
    stdscr.nodelay(False)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    
    h, w = stdscr.getmaxyx()
    
    title = " "
    try:
        stdscr.addstr(0, (w - len(title)) // 2, title, curses.color_pair(2) | curses.A_BOLD)
    except: pass
    
    stdscr.addstr(h-2, 2, " Loading image... ", curses.color_pair(1))
    stdscr.refresh()
    
    img = fetch_and_convert_image("https://f4.bcbits.com/img/a1664460568_10.jpg")
    
    if img is None:
        stdscr.clear()
        stdscr.addstr(h//2, (w-40)//2, "Failed to load image. Check internet/Pillow.", curses.color_pair(2))
        stdscr.getch()
        return

    # Render loop to handle resize or just static display
    while True:
        stdscr.erase()
        try:
            stdscr.addstr(0, (w - len(title)) // 2, title, curses.color_pair(2) | curses.A_BOLD)
        except: pass
        
        render_ascii_frame(stdscr, img)
        
        msg = " Press any key to exit "
        try:
            stdscr.addstr(h-2, (w - len(msg)) // 2, msg, curses.color_pair(1) | curses.A_DIM)
        except: pass
        
        stdscr.refresh()
        
        # Non-blocking check for key, but allow a moment to render
        stdscr.timeout(100)
        key = stdscr.getch()
        if key != -1:
            break
        # Update terminal size in case of resize
        h, w = stdscr.getmaxyx()

# --- Application Logic ---

class TypingApp:
    def __init__(self, stdscr, mode, target_count=25, word_bank="common"):
        self.stdscr = stdscr
        self.mode = mode 
        self.target_count = target_count
        self.word_bank = word_bank
        self.config = load_config()
        
        if self.config.get("smart_sentences", False):
            self.smart_mode = True
        else:
            self.smart_mode = False
            
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
        if self.mode in ['rand', 'zen']:
            self.text = get_random_words(self.target_count, self.word_bank, self.smart_mode)
        else:
            self.text = "Type something."
        if not self.text:
            self.text = "Error loading text."

    def draw_screen(self):
        if self.show_menu:
            self.draw_menu()
            return

        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        try:
            self.stdscr.box()
            self.stdscr.attron(curses.color_pair(5))
            self.stdscr.box()
            self.stdscr.attroff(curses.color_pair(5))
        except: pass

        title = " SCRIBERE "
        start_x = (width - len(title)) // 2
        try:
            self.stdscr.addstr(0, start_x, title, curses.color_pair(5) | curses.A_BOLD)
        except: pass

        status = f" Mode: {self.mode.upper()} | Words: {self.target_count} | Bank: {self.word_bank} "
        if self.finished:
            status = " TEST COMPLETE "
        try:
            self.stdscr.addstr(2, 2, status, curses.color_pair(5))
        except: pass

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
        if current_line:
            wrapped_lines.append(current_line)
        
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
                t_char = char
                char_idx_global = global_flat_idx + c_idx
                
                attr = curses.color_pair(4)
                
                if char_idx_global < len(self.user_input):
                    u_char = self.user_input[char_idx_global]
                    if u_char == t_char:
                        attr = curses.color_pair(1)
                    else:
                        attr = curses.color_pair(2)
                
                if char_idx_global == flat_cursor and not self.finished:
                    attr = curses.color_pair(3) | curses.A_REVERSE
                
                try:
                    self.stdscr.addch(screen_r, 2 + c_idx, t_char, attr)
                except: pass
            
            global_flat_idx += len(line)

        if self.finished:
            self.draw_results(start_row + max_rows + 1, width)
        else:
            wpm = 0
            if self.start_time:
                elapsed = (time.time() - self.start_time) / 60.0
                if elapsed > 0:
                    wpm = int((len(self.user_input) / 5.0) / elapsed)
            
            stats_str = f" WPM: {wpm} | Acc: {self.get_accuracy():.1f}% | Err: {self.errors} "
            try:
                self.stdscr.addstr(height - 2, 2, stats_str, curses.color_pair(5) | curses.A_DIM)
            except: pass
        
        self.stdscr.refresh()

    def draw_menu(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()
        
        menu_h, menu_w = 12, 50
        start_y, start_x = (h - menu_h) // 2, (w - menu_w) // 2
        
        win = curses.newwin(menu_h, menu_w, start_y, start_x)
        win.box()
        win.keypad(True)
        
        title = " MENU "
        win.addstr(0, (menu_w - len(title)) // 2, title, curses.color_pair(5) | curses.A_BOLD)
        
        options = [
            "1. Toggle Smart Sentences",
            "2. Change Word Bank (Common/Complex)",
            "3. Toggle Minimal Stats",
            "4. Resume Test",
            "5. Quit App"
        ]
        
        for i, opt in enumerate(options):
            win.addstr(2 + i, 2, opt, curses.color_pair(6))
        
        win.addstr(menu_h - 2, 2, " Select (1-5) or Esc to close ", curses.color_pair(5) | curses.A_DIM)
        win.refresh()
        
        while True:
            key = win.getch()
            if key == 27 or key == ord('q'):
                self.show_menu = False
                break
            elif key == ord('1'):
                self.config["smart_sentences"] = not self.config.get("smart_sentences", False)
                save_config(self.config)
                self.smart_mode = self.config["smart_sentences"]
                self.reset_test()
                break
            elif key == ord('2'):
                self.config["word_bank"] = "complex" if self.config.get("word_bank") == "common" else "common"
                save_config(self.config)
                self.word_bank = self.config["word_bank"]
                self.reset_test()
                break
            elif key == ord('3'):
                self.config["minimal_stats"] = not self.config.get("minimal_stats", False)
                save_config(self.config)
                break
            elif key == ord('4'):
                self.show_menu = False
                break
            elif key == ord('5'):
                self.running = False
                break

    def reset_test(self):
        self.text = get_random_words(self.target_count, self.word_bank, self.smart_mode)
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.cursor_pos = 0
        self.errors = 0
        self.total_chars_typed = 0

    def get_accuracy(self):
        if len(self.user_input) == 0:
            return 100.0
        correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.text) and c == self.text[i])
        return (correct / len(self.user_input)) * 100

    def draw_results(self, row, width):
        elapsed = 0
        if self.start_time and self.end_time:
            elapsed = self.end_time - self.start_time
        
        wpm = 0
        if elapsed > 0:
            wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0))
        
        acc = self.get_accuracy()
        
        res_title = " RESULTS "
        start_x = (width - len(res_title)) // 2
        try:
            self.stdscr.addstr(row, start_x, res_title, curses.color_pair(5) | curses.A_BOLD)
        except: pass

        minimal = self.config.get("minimal_stats", False)
        
        if minimal:
            stats = f" WPM: {wpm} | Accuracy: {acc:.1f}% "
        else:
            stats = f" WPM: {wpm} | Accuracy: {acc:.1f}% | Errors: {self.errors} | Chars: {len(self.user_input)} | Time: {elapsed:.1f}s "
        
        try:
            self.stdscr.addstr(row + 2, 2, stats, curses.color_pair(1) | curses.A_BOLD)
        except: pass
            
        hint = " Enter: New Test | M: Scores | D: Toggle Stats | Esc: Menu "
        try:
            self.stdscr.addstr(row + 4, 2, hint, curses.color_pair(5) | curses.A_DIM)
        except: pass

    def handle_input(self, key):
        if self.show_menu:
            self.show_menu = False
            return

        if self.finished:
            if key == 10 or key == curses.KEY_ENTER:
                self.reset_test()
            elif key == ord('m') or key == ord('M'):
                self.show_highscores()
            elif key == ord('d') or key == ord('D'):
                self.config["minimal_stats"] = not self.config.get("minimal_stats", False)
                save_config(self.config)
            elif key == 27:
                self.show_menu = True
            return

        if key == 27:
            self.show_menu = True
            return

        if self.mode == 'zen' and (key == 10 or key == curses.KEY_ENTER or key == 343): 
             self.finish_test()
             return

        if key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                if len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]
        elif key == curses.KEY_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif key == curses.KEY_RIGHT:
            if self.cursor_pos < len(self.text):
                self.cursor_pos += 1
        elif 32 <= key <= 126:
            if self.cursor_pos < len(self.text):
                char = chr(key)
                if self.cursor_pos == len(self.user_input):
                    self.user_input += char
                else:
                    if self.cursor_pos < len(self.user_input):
                         self.user_input = self.user_input[:self.cursor_pos] + char + self.user_input[self.cursor_pos+1:]
                    else:
                         self.user_input += char
                
                if self.cursor_pos < len(self.text):
                    if self.user_input[self.cursor_pos] != self.text[self.cursor_pos]:
                         self.errors += 1
                    
                self.cursor_pos += 1
                self.total_chars_typed += 1
                
                if self.cursor_pos == len(self.text):
                    self.finish_test()
        
        if not self.finished and self.start_time is None and len(self.user_input) > 0:
            self.start_time = time.time()

    def finish_test(self):
        if not self.finished:
            self.finished = True
            self.end_time = time.time()
            self.save_score()

    def save_score(self):
        elapsed = self.end_time - self.start_time if self.end_time and self.start_time else 0
        wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0)) if elapsed > 0 else 0
        acc = self.get_accuracy()
        
        score_entry = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "mode": self.mode,
            "word_bank": self.word_bank,
            "smart": self.smart_mode,
            "wpm": wpm,
            "accuracy": acc,
            "errors": self.errors,
            "chars": len(self.user_input)
        }
        
        scores = load_scores()
        scores.append(score_entry)
        scores.sort(key=lambda x: x['wpm'], reverse=True)
        save_scores(scores[:100])

    def show_highscores(self):
        scores = load_scores()
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        title = " HIGH SCORES "
        self.stdscr.addstr(2, (w-len(title))//2, title, curses.color_pair(5) | curses.A_BOLD)
        
        if not scores:
            self.stdscr.addstr(5, 5, "No scores recorded yet.", curses.color_pair(4))
        else:
            self.stdscr.addstr(4, 5, "Date       Mode    WPM  Acc%   Bank", curses.color_pair(5))
            for i, s in enumerate(scores[:15]):
                bank = s.get('word_bank', 'N/A')
                if s.get('smart'): bank += " (Smart)"
                line = f"{s['date']} {s['mode']:<6} {s['wpm']:>3} {s['accuracy']:>5.1f}   {bank}"
                try:
                    self.stdscr.addstr(6 + i, 5, line, curses.color_pair(1 if i == 0 else 4))
                except: pass
        
        self.stdscr.addstr(h-2, 2, " Press Enter to close ", curses.color_pair(5) | curses.A_DIM)
        self.stdscr.refresh()
        
        while True:
            k = self.stdscr.getch()
            if k == 10 or k == curses.KEY_ENTER:
                break

    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        
        while self.running:
            self.draw_screen()
            try:
                key = self.stdscr.getch()
                if key != -1:
                    self.handle_input(key)
            except KeyboardInterrupt:
                break
        
        curses.curs_set(1)

def main_cli(stdscr, args):
    ensure_config()
    
    if args.command == 'secret':
        show_secret_screen(stdscr)
        return

    mode = args.mode
    word_bank = args.bank
    target = args.count
    
    app = TypingApp(stdscr, mode, target_count=target, word_bank=word_bank)
    app.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scribere Typing Tutor")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    start_parser = subparsers.add_parser('start', help='Start a typing test')
    start_parser.add_argument('mode', choices=['rand', 'zen'], help='Test mode')
    start_parser.add_argument('--count', '-c', type=int, default=25, help='Number of words')
    start_parser.add_argument('--bank', '-b', choices=['common', 'complex'], default='common', help='Word bank')
    
    subparsers.add_parser('secret', help='Secret Easter Egg')
    subparsers.add_parser('config', help='Show config path')
    
    args = parser.parse_args()
    
    if args.command == 'config':
        print(f"Config: {CONFIG_FILE}")
        sys.exit(0)
    elif args.command == 'secret':
        curses.wrapper(lambda stdscr: main_cli(stdscr, args))
        sys.exit(0)
    elif args.command == 'start':
        pass
    else:
        class DefaultArgs:
            command = 'start'
            mode = 'rand'
            count = 25
            bank = 'common'
        args = DefaultArgs()

    try:
        curses.wrapper(lambda stdscr: main_cli(stdscr, args))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
