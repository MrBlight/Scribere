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

# --- Configuration & Data ---

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".scribere")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SCORES_FILE = os.path.join(CONFIG_DIR, "scores.json")

# Fixed & Expanded Common Words Bank
COMMON_WORDS = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "dog",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "dig",
    "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "wish",
    "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "send", "folk", "musician", "music", "rock", "pop", "jazz", "electronic",
    "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "man",
    "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "cost",
    "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "talking", "shop",
    "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "fly", "european", "african", "asian", "balkan",
    "new", "want", "because", "any", "these", "give", "day", "most", "us", "is", "meme", "liquid",
    "house", "school", "fight", "although", "through", "water", "money", "world", "place", "group", "tiny", "large",
    "hand", "high", "part", "child", "eye", "woman", "life", "down", "head", "stand", "kid", "silly", "wise",
    "own", "page", "should", "country", "found", "answer", "study", "still", "learn", "parent",
    "face", "friend", "mother", "father", "city", "line", "near", "far", "door", "room", "floor", "lost",
    "book", "letter", "word", "sentence", "paper", "idea", "question", "change", "order", "number", "half",
    "start", "end", "road", "map", "car", "bus", "train", "plane", "boat", "bike", "however", "black", "white",
    "dog", "cat", "bird", "fish", "tree", "flower", "grass", "sun", "moon", "star", "his", "her",
    "sky", "cloud", "rain", "snow", "wind", "fire", "earth", "stone", "sand", "hill", "cat", "frog",
    "river", "lake", "sea", "ocean", "bridge", "tower", "wall", "gate", "fence", "path", "sour", "bitter", "sweet",
    "food", "bread", "milk", "egg", "meat", "fruit", "apple", "orange", "banana", "grape", "computer",
    "cake", "sugar", "salt", "pepper", "coffee", "tea", "juice", "beer", "wine", "water", "eat", "chocolate",
    "hot", "cold", "warm", "cool", "dry", "wet", "hard", "soft", "heavy", "light", "great", "awesome",
    "fast", "slow", "old", "young", "big", "small", "long", "short", "wide", "narrow", "taste", "wrong", "right",
    "thick", "thin", "deep", "shallow", "high", "low", "loud", "quiet", "bright", "dark", "true", "truth", "false", "fake",
    "clean", "dirty", "full", "empty", "open", "closed", "safe", "dangerous", "easy", "hard", "ice",
    "happy", "sad", "angry", "afraid", "tired", "hungry", "thirsty", "sick", "healthy", "strong",
    "weak", "rich", "poor", "kind", "mean", "nice", "rude", "smart", "stupid", "funny", "miller", "care", "game",
    "serious", "busy", "free", "early", "late", "soon", "never", "always", "often", "sometimes", "sound",
    "here", "there", "everywhere", "nowhere", "somewhere", "inside", "outside", "above", "below", "between",
    "before", "behind", "next", "last", "first", "second", "third", "fourth", "fifth", "tenth"
]

# Complex Words Bank
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

# Smart Sentence Templates (Subject + Verb + Object/Adj)
# Uses weights to ensure common words appear more often
TEMPLATES = [
    "{adj} {noun} {verb} {prep} the {noun}.",
    "the {noun} {verb} {adj}.",
    "{pronoun} {verb} the {noun} {adv}.",
    "is the {noun} {adj}?",
    "why {pronoun} {verb} {adj}?",
    "{noun} and {noun} are {adj}.",
    "the {adj} {noun} {verb}.",
    "{pronoun} can {verb} {adv}.",
    "do not {verb} the {noun}.",
    "it is {adj} to {verb}.",
    "{noun} {verb} {prep} the {adj} {noun}.",
    "very {adj} {noun}.",
    "the {noun} is {adj}.",
    "{pronoun} {verb} {noun}."
]

WORD_TYPES = {
    "noun": ["dog", "cat", "bird", "fish", "tree", "flower", "grass", "sun", "moon", "star", "sky", "cloud", "rain", "snow", "wind", "fire", "earth", "stone", "sand", "hill", "river", "lake", "sea", "ocean", "bridge", "tower", "wall", "gate", "fence", "path", "food", "bread", "milk", "egg", "meat", "fruit", "apple", "orange", "banana", "grape", "computer", "cake", "sugar", "salt", "pepper", "coffee", "tea", "juice", "beer", "wine", "water", "chocolate", "house", "school", "money", "world", "place", "group", "hand", "head", "eye", "woman", "life", "child", "friend", "mother", "father", "city", "line", "door", "room", "floor", "book", "letter", "word", "sentence", "paper", "idea", "question", "change", "order", "number", "road", "map", "car", "bus", "train", "plane", "boat", "bike", "man", "people", "time", "day", "year", "way", "thing", "game", "sound", "ice"],
    "verb": ["be", "have", "do", "say", "go", "get", "make", "know", "think", "take", "see", "come", "want", "use", "find", "give", "tell", "work", "call", "try", "ask", "need", "feel", "become", "leave", "put", "mean", "keep", "let", "begin", "seem", "help", "talk", "turn", "start", "show", "hear", "play", "run", "move", "like", "live", "believe", "hold", "bring", "happen", "write", "provide", "sit", "stand", "lose", "pay", "meet", "include", "continue", "set", "learn", "change", "lead", "understand", "watch", "follow", "stop", "create", "speak", "read", "allow", "add", "spend", "grow", "open", "walk", "win", "offer", "remember", "love", "consider", "appear", "buy", "wait", "serve", "die", "send", "expect", "build", "stay", "fall", "cut", "reach", "kill", "remain", "suggest", "raise", "pass", "sell", "require", "report", "decide", "pull"],
    "adj": ["good", "new", "first", "last", "long", "great", "little", "own", "other", "old", "right", "big", "high", "different", "small", "large", "next", "early", "young", "important", "few", "public", "bad", "same", "able", "true", "wrong", "false", "fake", "hot", "cold", "warm", "cool", "dry", "wet", "hard", "soft", "heavy", "light", "loud", "quiet", "bright", "dark", "clean", "dirty", "full", "empty", "safe", "dangerous", "easy", "happy", "sad", "angry", "afraid", "tired", "hungry", "thirsty", "sick", "healthy", "strong", "weak", "rich", "poor", "kind", "mean", "nice", "rude", "smart", "stupid", "funny", "serious", "busy", "free", "late", "soon", "tiny", "large", "silly", "wise", "lost", "sour", "bitter", "sweet", "awesome", "european", "african", "asian", "balkan"],
    "pronoun": ["i", "you", "he", "she", "it", "we", "they", "one", "someone", "everyone"],
    "prep": ["in", "on", "at", "to", "for", "with", "by", "from", "up", "about", "into", "over", "after", "under", "before"],
    "adv": ["quickly", "slowly", "carefully", "badly", "well", "very", "really", "always", "never", "often", "sometimes", "here", "there", "now", "then", "today", "tomorrow", "yes", "no"]
}

def get_weighted_word(word_list):
    # Simple weighting: first 20% of list appears 50% of the time
    if random.random() < 0.5:
        return random.choice(word_list[:max(1, len(word_list)//5)])
    return random.choice(word_list)

def generate_smart_sentence():
    template = random.choice(TEMPLATES)
    result = template
    
    for key in WORD_TYPES:
        # Replace all occurrences of {key}
        while "{" + key + "}" in result:
            word = get_weighted_word(WORD_TYPES[key])
            result = result.replace("{" + key + "}", word, 1)
    
    return result

def get_random_words(count, word_bank="common", smart=False):
    if smart:
        sentences = []
        current_len = 0
        while current_len < count:
            s = generate_smart_sentence()
            sentences.append(s)
            current_len += len(s.split())
        return " ".join(sentences)[:len(" ".join(sentences).split()[:count])] # Rough cut
    
    if word_bank == "complex":
        return " ".join(random.choice(COMPLEX_WORDS) for _ in range(count))
    else:
        # Weighted random for common words too
        words = []
        for _ in range(count):
            if random.random() < 0.6: # 60% chance of top 20% words
                words.append(random.choice(COMMON_WORDS[:50]))
            else:
                words.append(random.choice(COMMON_WORDS))
        return " ".join(words)

def get_quote_by_length(length_cat):
    # Placeholder for quote logic (same as before)
    # Re-using the QUOTES_DB from previous version would go here
    # For brevity in this snippet, assuming it exists or returning fallback
    fallback = "The quick brown fox jumps over the lazy dog."
    return fallback 

def get_random_quote():
    return "Practice makes perfect."

# --- Application Logic ---

class TypingApp:
    def __init__(self, stdscr, mode, target_count=None, length_cat=None, word_bank="common", smart=False):
        self.stdscr = stdscr
        self.mode = mode
        self.target_count = target_count
        self.length_cat = length_cat
        self.word_bank = word_bank
        self.smart_mode = smart
        self.text = ""
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.cursor_pos = 0
        self.errors = 0
        self.total_chars_typed = 0
        self.config = load_config()
        
        # Setup Curses for minimal flicker
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_WHITE, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
        
        # Critical for flicker reduction
        curses.curs_set(0) # Hide physical cursor
        self.stdscr.nodelay(True) # Non-blocking
        self.stdscr.keypad(True)
        curses.noecho()
        
        self.setup_text()
        self.running = True
        self.last_draw_time = 0

    def setup_text(self):
        if self.mode == 'rand':
            count = self.target_count if self.target_count else 25
            self.text = get_random_words(count, self.word_bank, self.smart_mode)
        elif self.mode == 'quote':
            self.text = get_quote_by_length(self.length_cat) if self.length_cat else get_random_quote()
        elif self.mode == 'zen':
            self.text = get_quote_by_length(self.length_cat) if self.length_cat else get_random_quote()
        elif self.mode == 'custom':
            self.text = "Type your own custom text here."
        
        if not self.text:
            self.text = "Error loading text."

    def draw_screen(self):
        # Double buffering: Draw to offscreen, then refresh once
        self.stdscr.erase() # Faster than clear() sometimes
        height, width = self.stdscr.getmaxyx()
        
        # Draw Border
        try:
            self.stdscr.attron(curses.color_pair(5))
            self.stdscr.box()
            self.stdscr.attroff(curses.color_pair(5))
        except curses.error:
            pass

        # Title
        title = " SCRIBERE "
        start_x = max(0, (width - len(title)) // 2)
        try:
            self.stdscr.addstr(0, start_x, title, curses.color_pair(5) | curses.A_BOLD)
        except curses.error:
            pass

        # Status Bar
        status = f" Mode: {self.mode.upper()} | Bank: {self.word_bank} "
        if self.smart_mode: status += "(Smart) "
        if self.finished: status = " TEST COMPLETE "
        try:
            self.stdscr.addstr(2, 2, status, curses.color_pair(5))
        except curses.error:
            pass

        # Text Display Area
        start_row = 4
        max_rows = height - 8
        max_cols = width - 4
        
        # Wrap text
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
        
        # Scroll logic
        flat_cursor = min(self.cursor_pos, len(self.text))
        current_flat = 0
        cursor_line_idx = 0
        cursor_col_idx = 0
        
        for l_idx, line in enumerate(wrapped_lines):
            if current_flat + len(line) >= flat_cursor:
                cursor_line_idx = l_idx
                cursor_col_idx = flat_cursor - current_flat
                break
            current_flat += len(line)
        
        scroll_offset = 0
        if cursor_line_idx >= max_rows:
            scroll_offset = cursor_line_idx - max_rows + 1
        
        visible_lines = wrapped_lines[scroll_offset : scroll_offset + max_rows]
        global_flat_idx = sum(len(l) for l in wrapped_lines[:scroll_offset])
        
        # Render lines
        for r_idx, line in enumerate(visible_lines):
            screen_r = start_row + r_idx
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
                except curses.error:
                    pass
            global_flat_idx += len(line)

        # Stats
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
            except curses.error:
                pass
        
        self.stdscr.refresh() # Single refresh per frame eliminates flicker

    def get_accuracy(self):
        if len(self.user_input) == 0: return 100.0
        correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.text) and c == self.text[i])
        return (correct / len(self.user_input)) * 100

    def draw_results(self, row, width):
        elapsed = (self.end_time - self.start_time) if (self.end_time and self.start_time) else 0
        wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0)) if elapsed > 0 else 0
        acc = self.get_accuracy()
        
        res_title = " RESULTS "
        try:
            self.stdscr.addstr(row, max(0, (width - len(res_title)) // 2), res_title, curses.color_pair(5) | curses.A_BOLD)
        except curses.error: pass

        minimal = self.config.get("minimal_stats", False)
        stats = f" WPM: {wpm} | Accuracy: {acc:.1f}% " if minimal else f" WPM: {wpm} | Accuracy: {acc:.1f}% | Errors: {self.errors} | Time: {elapsed:.1f}s "
        
        try:
            self.stdscr.addstr(row + 2, 2, stats, curses.color_pair(1) | curses.A_BOLD)
            self.stdscr.addstr(row + 4, 2, " Press Enter to continue | 'M' for Scores | 'D' toggle stats ", curses.color_pair(5) | curses.A_DIM)
        except curses.error: pass

    def handle_input(self, key):
        if self.finished:
            if key in (10, curses.KEY_ENTER, 13):
                self.running = False
            elif key in (ord('m'), ord('M')):
                self.show_highscores()
            elif key in (ord('d'), ord('D')):
                self.config["minimal_stats"] = not self.config.get("minimal_stats", False)
                save_config(self.config)
            return

        if key == 27: # ESC
            self.running = False
            return

        if self.mode == 'zen' and key in (10, curses.KEY_ENTER, 13, 343):
             self.finish_test()
             return

        if key in (curses.KEY_BACKSPACE, 127, 8, 263): # 263 is often backspace in some terms
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                if len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]
        elif key == curses.KEY_LEFT:
            if self.cursor_pos > 0: self.cursor_pos -= 1
        elif key == curses.KEY_RIGHT:
            if self.cursor_pos < len(self.text): self.cursor_pos += 1
        elif 32 <= key <= 126:
            if self.cursor_pos < len(self.text):
                char = chr(key)
                if self.cursor_pos == len(self.user_input):
                    self.user_input += char
                elif self.cursor_pos < len(self.user_input):
                    self.user_input = self.user_input[:self.cursor_pos] + char + self.user_input[self.cursor_pos+1:]
                
                if self.cursor_pos < len(self.text) and self.user_input[self.cursor_pos] != self.text[self.cursor_pos]:
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
        elapsed = (self.end_time - self.start_time) if (self.end_time and self.start_time) else 0
        wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0)) if elapsed > 0 else 0
        score_entry = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "mode": self.mode,
            "wpm": wpm,
            "accuracy": self.get_accuracy(),
            "errors": self.errors
        }
        scores = load_scores()
        scores.append(score_entry)
        scores.sort(key=lambda x: x['wpm'], reverse=True)
        save_scores(scores[:100])

    def show_highscores(self):
        scores = load_scores()
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(2, max(0, (w-12)//2), " HIGH SCORES ", curses.color_pair(5) | curses.A_BOLD)
        if not scores:
            self.stdscr.addstr(5, 5, "No scores recorded yet.", curses.color_pair(4))
        else:
            self.stdscr.addstr(4, 5, "Date       Mode   WPM  Acc%", curses.color_pair(5))
            for i, s in enumerate(scores[:15]):
                line = f"{s['date']} {s['mode']:<6} {s['wpm']:>3} {s['accuracy']:>5.1f}"
                try: self.stdscr.addstr(6 + i, 5, line, curses.color_pair(1 if i==0 else 4))
                except curses.error: pass
        self.stdscr.addstr(h-2, 2, " Press Enter to close ", curses.color_pair(5) | curses.A_DIM)
        self.stdscr.refresh()
        while True:
            k = self.stdscr.getch()
            if k in (10, curses.KEY_ENTER, 13): break

    def run(self):
        while self.running:
            self.draw_screen()
            try:
                key = self.stdscr.getch()
                if key != -1: self.handle_input(key)
            except KeyboardInterrupt:
                break
        curses.curs_set(1)

def ensure_config():
    if not os.path.exists(CONFIG_DIR): os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f: json.dump({"minimal_stats": False}, f)
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f: json.dump([], f)

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f: return json.load(f)
    except: return {"minimal_stats": False}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f: json.dump(config, f)

def load_scores():
    try:
        with open(SCORES_FILE, 'r') as f: return json.load(f)
    except: return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f: json.dump(scores, f)

def main_cli(stdscr, args):
    ensure_config()
    mode = args.mode
    # Pass smart flag if needed, defaulting to False for now unless arg added
    app = TypingApp(stdscr, mode, target_count=args.count, length_cat=args.length, word_bank=args.bank, smart=False)
    app.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scribere Typing Tutor")
    subparsers = parser.add_subparsers(dest='command')
    start_parser = subparsers.add_parser('start')
    start_parser.add_argument('mode', choices=['rand', 'quote', 'zen', 'custom'])
    start_parser.add_argument('--count', '-c', type=int, default=25)
    start_parser.add_argument('--length', '-l', choices=['short', 'medium', 'long', 'longest'])
    start_parser.add_argument('--bank', '-b', choices=['common', 'complex'], default='common')
    # Add --smart flag
    start_parser.add_argument('--smart', action='store_true', help='Use smart sentence generation')
    
    subparsers.add_parser('config')
    
    args = parser.parse_args()
    if args.command == 'config':
        print(f"Config: {CONFIG_FILE}")
        sys.exit(0)
    elif not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        curses.wrapper(lambda stdscr: main_cli(stdscr, args))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
