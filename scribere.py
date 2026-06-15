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

# Common Words Bank
COMMON_WORDS = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "dog"
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "dig", 
    "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "wish",
    "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "send", "folk", "musicial", "music", "rock", "pop", "jazz", "electronic"
    "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "man",
    "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "cost",
    "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "talking",
    "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "fly", "european", "african" "asian" "balkan",
    "new", "want", "because", "any", "these", "give", "day", "most", "us", "is", "meme", "liquid",
    "house", "school", "fight", "although", "through", "water", "money", "world", "place", "group", "tiny", "large",
    "hand", "high", "part", "child", "eye", "woman", "life", "down", "head", "stand", "kid", "silly", "wise",
    "own", "page", "should", "country", "found", "answer", "study", "still", "learn", "parent",
    "face", "friend", "mother", "father", "city", "line", "near", "far", "door", "room", "floor", "lost", 
    "book", "letter", "word", "sentence", "paper", "idea", "question", "change", "order", "number", "half",
    "start", "end", "road", "map", "car", "bus", "train", "plane", "boat", "bike", "however", "black", "white",
    "dog", "cat", "bird", "fish", "tree", "flower", "grass", "sun", "moon", "star", "his", "her",
    "sky", "cloud", "rain", "snow", "wind", "fire", "earth", "stone", "sand", "hill", "cat", "frog", 
    "river", "lake", "sea", "ocean", "bridge", "tower", "wall", "gate", "fence", "path", "sour", "bitter", "sweet"
    "food", "bread", "milk", "egg", "meat", "fruit", "apple", "orange", "banana", "grape", "computer",
    "cake", "sugar", "salt", "pepper", "coffee", "tea", "juice", "beer", "wine", "water", "eat",
    "hot", "cold", "warm", "cool", "dry", "wet", "hard", "soft", "heavy", "light", "great", "awesome",  
    "fast", "slow", "old", "young", "big", "small", "long", "short", "wide", "narrow", "taste", "wrong", "right", 
    "thick", "thin", "deep", "shallow", "high", "low", "loud", "quiet", "bright", "dark", "true", "truth", "false", "fake",
    "clean", "dirty", "full", "empty", "open", "closed", "safe", "dangerous", "easy", "hard", "ice"
    "happy", "sad", "angry", "afraid", "tired", "hungry", "thirsty", "sick", "healthy", "strong",
    "weak", "rich", "poor", "kind", "mean", "nice", "rude", "smart", "stupid", "funny", "miller", "care", "game",  
    "serious", "busy", "free", "early", "late", "soon", "never", "always", "often", "sometimes", "sound",
    "here", "there", "everywhere", "nowhere", "somewhere", "inside", "outside", "above", "below", "between",
    "before", "behind", "next", "last", "first", "second", "third", "fourth", "fifth", "tenth"
]

# Complex Words Bank (Less common, technical, or longer words)
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

# Curated Quotes Database (Categorized by length and topic)
QUOTES_DB = [
    # Short (5-15 words)
    {"text": "The only way to do great work is to love what you do.", "topic": "Work", "length": "short"},
    {"text": "Life is what happens when you are busy making other plans.", "topic": "Life", "length": "short"},
    {"text": "Get busy living or get busy dying.", "topic": "Life", "length": "short"},
    {"text": "You miss one hundred percent of the shots you never take.", "topic": "Sports", "length": "short"},
    {"text": "Whether you think you can or you think you can not, you are right.", "topic": "Mindset", "length": "short"},
    {"text": "The best time to plant a tree was twenty years ago. The next best time is now.", "topic": "Action", "length": "short"},
    {"text": "An unexamined life is not worth living.", "topic": "Philosophy", "length": "short"},
    {"text": "Eighty percent of success is showing up.", "topic": "Success", "length": "short"},
    {"text": "Your time is limited, so do not waste it living someone else's life.", "topic": "Life", "length": "short"},
    {"text": "Winning isn't everything, but wanting to win is.", "topic": "Sports", "length": "short"},
    {"text": "I am not a product of my circumstances. I am a product of my decisions.", "topic": "Mindset", "length": "short"},
    {"text": "Every child is an artist. The problem is how to remain an artist once he grows up.", "topic": "Art", "length": "short"},
    {"text": "You can never cross the ocean until you have the courage to lose sight of the shore.", "topic": "Courage", "length": "short"},
    {"text": "I've learned that people will forget what you said, but people will never forget how you made them feel.", "topic": "Wisdom", "length": "short"},
    {"text": "Either you run the day, or the day runs you.", "topic": "Productivity", "length": "short"},
    
    # Medium (16-30 words)
    {"text": "It is during our darkest moments that we must focus to see the light.", "topic": "Hope", "length": "medium"},
    {"text": "Do not go where the path may lead, go instead where there is no path and leave a trail.", "topic": "Leadership", "length": "medium"},
    {"text": "In the end, it's not the years in your life that count. It's the life in your years.", "topic": "Life", "length": "medium"},
    {"text": "The greatest glory in living lies not in never falling, but in rising every time we fall.", "topic": "Resilience", "length": "medium"},
    {"text": "Many of life's failures are people who did not realize how close they were to success when they gave up.", "topic": "Persistence", "length": "medium"},
    {"text": "If you want to live a happy life, tie it to a goal, not to people or things.", "topic": "Happiness", "length": "medium"},
    {"text": "Never let the fear of striking out keep you from playing the game.", "topic": "Courage", "length": "medium"},
    {"text": "Money and success don't change people; they merely amplify what is already there.", "topic": "Success", "length": "medium"},
    {"text": "Not how long, but how well you have lived is the main thing.", "topic": "Life", "length": "medium"},
    {"text": "If life were predictable it would cease to be life, and be without flavor.", "topic": "Life", "length": "medium"},
    {"text": "The whole secret of a successful life is to find out what is one's destiny to do, and then do it.", "topic": "Success", "length": "medium"},
    {"text": "In order to write about life first you must live it.", "topic": "Writing", "length": "medium"},
    {"text": "The big lesson in life, baby, is never be scared of anyone or anything.", "topic": "Courage", "length": "medium"},
    {"text": "Sing like no one's listening, love like you've never been hurt, dance like nobody's watching, and live like its heaven on earth.", "topic": "Life", "length": "medium"},
    {"text": "Curiosity about life in all of its aspects, I think, is still the secret of great creative people.", "topic": "Creativity", "length": "medium"},
    
    # Long (31-50 words)
    {"text": "Life is not about waiting for the storm to pass but learning to dance in the rain. Embrace the challenges, for they shape your character and define your journey.", "topic": "Life", "length": "long"},
    {"text": "The purpose of life is not to be happy. It is to be useful, to be honorable, to be compassionate, to have it make some difference that you have lived and lived well.", "topic": "Purpose", "length": "long"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts. Keep moving forward, even when the road seems uncertain and the path is unclear.", "topic": "Success", "length": "long"},
    {"text": "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. Your potential is limitless if you dare to explore it.", "topic": "Belief", "length": "long"},
    {"text": "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment. This is the only time you truly have control over.", "topic": "Mindfulness", "length": "long"},
    {"text": "It does not matter how slowly you go as long as you do not stop. Progress is progress, no matter the pace. Consistency is the key to achieving your dreams.", "topic": "Persistence", "length": "long"},
    {"text": "Everything you've ever wanted is on the other side of fear. Face your fears, embrace the unknown, and watch as your world expands beyond your wildest imagination.", "topic": "Fear", "length": "long"},
    {"text": "Opportunities don't happen. You create them. Stop waiting for the perfect moment and start taking action today. Your future is shaped by the choices you make now.", "topic": "Action", "length": "long"},
    {"text": "Try not to become a person of success, but rather try to become a person of value. Value comes from contribution, kindness, and integrity, not just material wealth.", "topic": "Value", "length": "long"},
    {"text": "Great minds discuss ideas; average minds discuss events; small minds discuss people. Focus your energy on creating, innovating, and building something that lasts.", "topic": "Wisdom", "length": "long"},
    
    # Longest (50+ words)
    {"text": "The man who moves a mountain begins by carrying away small stones. Do not be overwhelmed by the size of your goals. Break them down into manageable tasks and tackle them one by one. Patience and persistence will yield results.", "topic": "Goals", "length": "longest"},
    {"text": "We cannot solve problems with the kind of thinking we employed when we came up with them. We must evolve our mindset, embrace new perspectives, and be willing to unlearn old habits to find innovative solutions.", "topic": "Innovation", "length": "longest"},
    {"text": "Learn from yesterday, live for today, hope for tomorrow. The important thing is not to stop questioning. Curiosity has its own reason for existing. One cannot help but be in awe when he contemplates the mysteries of eternity.", "topic": "Learning", "length": "longest"},
    {"text": "It is better to be hated for what you are than to be loved for what you are not. Authenticity is the foundation of true happiness. Embrace your flaws, celebrate your uniqueness, and live your truth without apology.", "topic": "Authenticity", "length": "longest"},
    {"text": "A ship in harbor is safe, but that is not what ships are built for. Step out of your comfort zone, take risks, and pursue your passions. Life begins at the edge of your comfort zone.", "topic": "Risk", "length": "longest"},
    {"text": "The only limit to our realization of tomorrow will be our doubts of today. Let us move forward with strong and active faith. Doubt kills more dreams than failure ever will. Believe in your ability to achieve greatness.", "topic": "Faith", "length": "longest"},
    {"text": "Yesterday is history, tomorrow is a mystery, but today is a gift of God, which is why we call it the present. Cherish each moment, make the most of your time, and create memories that will last a lifetime.", "topic": "Time", "length": "longest"},
    {"text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. Stay true to your values, follow your heart, and never compromise your integrity for the sake of approval.", "topic": "Individuality", "length": "longest"},
    {"text": "Happiness is not something ready made. It comes from your own actions. Cultivate gratitude, practice kindness, and spread joy wherever you go. Your happiness is your responsibility, and it starts with the choices you make each day.", "topic": "Happiness", "length": "longest"},
    {"text": "The best revenge is massive success. Instead of dwelling on negativity or seeking vengeance, channel your energy into achieving your goals. Let your success speak louder than any words ever could.", "topic": "Success", "length": "longest"}
]

def ensure_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "color_theme": "default", # default, blue_cursor, green_cursor
            "minimal_stats": False,
            "word_bank": "common" # common, complex
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f)
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            json.dump([], f)

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_scores():
    with open(SCORES_FILE, 'r') as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def get_random_words(count, word_bank="common"):
    if word_bank == "complex":
        return " ".join(random.choice(COMPLEX_WORDS) for _ in range(count))
    else:
        return " ".join(random.choice(COMMON_WORDS) for _ in range(count))

def get_quote_by_length(length_cat):
    valid_quotes = [q for q in QUOTES_DB if q["length"] == length_cat]
    if not valid_quotes:
        # Fallback to any quote if category empty
        return random.choice(QUOTES_DB)["text"]
    return random.choice(valid_quotes)["text"]

def get_random_quote():
    return random.choice(QUOTES_DB)["text"]

# --- Application Logic ---

class TypingApp:
    def __init__(self, stdscr, mode, target_count=None, length_cat=None, word_bank="common"):
        self.stdscr = stdscr
        self.mode = mode # 'rand', 'quote', 'zen', 'custom'
        self.target_count = target_count
        self.length_cat = length_cat
        self.word_bank = word_bank
        self.text = ""
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.cursor_pos = 0
        self.errors = 0
        self.total_chars_typed = 0
        self.config = load_config()
        
        # Initialize colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)   # Correct
        curses.init_pair(2, curses.COLOR_RED, -1)    # Error
        curses.init_pair(3, curses.COLOR_GREEN, -1)  # Cursor highlight
        curses.init_pair(4, curses.COLOR_WHITE, -1)  # Untyped
        curses.init_pair(5, curses.COLOR_YELLOW, -1) # UI Borders
        
        self.setup_text()
        self.running = True

    def setup_text(self):
        if self.mode == 'rand':
            count = self.target_count if self.target_count else 25
            self.text = get_random_words(count, self.word_bank)
        elif self.mode == 'quote':
            if self.length_cat:
                self.text = get_quote_by_length(self.length_cat)
            else:
                self.text = get_random_quote()
        elif self.mode == 'zen':
            # Zen uses a random quote or random words depending on preference, defaulting to quote
            if self.length_cat:
                self.text = get_quote_by_length(self.length_cat)
            else:
                self.text = get_random_quote()
        elif self.mode == 'custom':
            # Handled outside usually, but fallback
            self.text = "Type your own custom text here."
        
        # Ensure text is not empty
        if not self.text:
            self.text = "Error loading text."

    def draw_screen(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        
        # Draw Border
        border_win = curses.newwin(height, width, 0, 0)
        border_win.attron(curses.color_pair(5))
        border_win.box()
        border_win.attroff(curses.color_pair(5))
        border_win.refresh()

        # Title
        title = " SCRIBERE "
        start_x = (width - len(title)) // 2
        try:
            self.stdscr.addstr(0, start_x, title, curses.color_pair(5) | curses.A_BOLD)
        except curses.error:
            pass

        # Status Bar
        status = f" Mode: {self.mode.upper()} | Bank: {self.word_bank} "
        if self.finished:
            status = " TEST COMPLETE "
        try:
            self.stdscr.addstr(2, 2, status, curses.color_pair(5))
        except curses.error:
            pass

        # Text Display Area
        # Calculate visible area
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
        
        # Determine scroll offset based on cursor
        # Flatten index to line/col
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
        
        # Scroll logic
        scroll_offset = 0
        if cursor_line_idx >= max_rows:
            scroll_offset = cursor_line_idx - max_rows + 1
        
        visible_lines = wrapped_lines[scroll_offset : scroll_offset + max_rows]
        
        # Render lines
        global_flat_idx = sum(len(l) for l in wrapped_lines[:scroll_offset])
        
        for r_idx, line in enumerate(visible_lines):
            screen_r = start_row + r_idx
            line_str = ""
            
            for c_idx, char in enumerate(line):
                t_char = char
                char_idx_global = global_flat_idx + c_idx
                
                attr = curses.color_pair(4) # Default untyped
                
                if char_idx_global < len(self.user_input):
                    u_char = self.user_input[char_idx_global]
                    if u_char == t_char:
                        attr = curses.color_pair(1) # Correct (Blue)
                    else:
                        attr = curses.color_pair(2) # Error (Red)
                
                # Cursor Highlight
                if char_idx_global == flat_cursor and not self.finished:
                    attr = curses.color_pair(3) | curses.A_REVERSE # Green/Reverse
                
                # Safe addch/addstr logic to avoid tuple error
                # We build the string segment and apply attribute via addstr with specific range or char by char
                # To be safe and simple:
                try:
                    self.stdscr.addch(screen_r, 2 + c_idx, t_char, attr)
                except curses.error:
                    pass
            
            global_flat_idx += len(line)

        # Stats or Finish Screen
        if self.finished:
            self.draw_results(start_row + max_rows + 1, width)
        else:
            # Live Stats
            wpm = 0
            if self.start_time:
                elapsed = (time.time() - self.start_time) / 60.0
                if elapsed > 0:
                    chars_typed = len(self.user_input)
                    wpm = int((chars_typed / 5.0) / elapsed)
            
            stats_str = f" WPM: {wpm} | Acc: {self.get_accuracy():.1f}% | Err: {self.errors} "
            try:
                self.stdscr.addstr(height - 2, 2, stats_str, curses.color_pair(5) | curses.A_DIM)
            except curses.error:
                pass
        
        self.stdscr.refresh()

    def get_accuracy(self):
        if self.total_chars_typed == 0:
            return 100.0
        correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.text) and c == self.text[i])
        return (correct / len(self.user_input)) * 100 if len(self.user_input) > 0 else 100.0

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
        except curses.error:
            pass

        minimal = self.config.get("minimal_stats", False)
        
        if minimal:
            stats = f" WPM: {wpm} | Accuracy: {acc:.1f}% "
        else:
            stats = f" WPM: {wpm} | Accuracy: {acc:.1f}% | Errors: {self.errors} | Chars: {len(self.user_input)} | Time: {elapsed:.1f}s "
        
        try:
            self.stdscr.addstr(row + 2, 2, stats, curses.color_pair(1) | curses.A_BOLD)
        except curses.error:
            pass
            
        hint = " Press Enter to continue | 'M' for Scores | 'D' toggle stats "
        try:
            self.stdscr.addstr(row + 4, 2, hint, curses.color_pair(5) | curses.A_DIM)
        except curses.error:
            pass

    def handle_input(self, key):
        if self.finished:
            if key == 10 or key == curses.KEY_ENTER: # Enter
                self.running = False
            elif key == ord('m') or key == ord('M'):
                self.show_highscores()
            elif key == ord('d') or key == ord('D'):
                self.config["minimal_stats"] = not self.config.get("minimal_stats", False)
                save_config(self.config)
            return

        if key == 27: # ESC
            self.running = False
            return

        if self.mode == 'zen' and (key == 10 or key == curses.KEY_ENTER or key == 343): # Enter variants
             # In Zen, Enter finishes ONLY if we decide so, or we can make it finish anytime?
             # Prompt said: "in zen mode to finish the test you can press shift enter"
             # Curses often doesn't distinguish Shift+Enter easily across terminals. 
             # We'll treat Enter as finish for Zen to be user-friendly, or check specifically if possible.
             # For now, let's assume Enter finishes in Zen.
             self.finish_test()
             return

        # Typing logic
        if key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                # Remove char from user_input logically? 
                # Actually user_input should mirror typed chars.
                # Simplified: user_input is the string of typed chars.
                if len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]
        elif key == curses.KEY_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif key == curses.KEY_RIGHT:
            if self.cursor_pos < len(self.text):
                self.cursor_pos += 1
        elif 32 <= key <= 126: # Printable
            if self.cursor_pos < len(self.text):
                char = chr(key)
                # Insert/Overwrite logic: Monkeytype overwrites/advances
                if self.cursor_pos == len(self.user_input):
                    self.user_input += char
                else:
                    # If editing in middle, truncate and add? 
                    # Standard typing test: linear progression. 
                    # Let's enforce linear for simplicity unless backspace used.
                    # But if cursor moved, we overwrite?
                    # Let's stick to linear: cursor always at end of user_input effectively
                    # Wait, if I move cursor left, I can correct.
                    # Simple approach: user_input matches text up to cursor_pos?
                    # No, user_input stores exactly what was typed.
                    
                    # Correction: Just append if at end. If moved back, overwrite at pos.
                    if self.cursor_pos < len(self.user_input):
                         self.user_input = self.user_input[:self.cursor_pos] + char + self.user_input[self.cursor_pos+1:]
                    else:
                         self.user_input += char
                
                if self.cursor_pos == len(self.user_input) - 1 or self.cursor_pos < len(self.user_input):
                     # Check correctness
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
            "length_cat": self.length_cat if self.mode == 'quote' else 'N/A',
            "word_bank": self.word_bank if self.mode == 'rand' else 'N/A',
            "wpm": wpm,
            "accuracy": acc,
            "errors": self.errors,
            "chars": len(self.user_input)
        }
        
        scores = load_scores()
        scores.append(score_entry)
        # Keep top 100
        scores.sort(key=lambda x: x['wpm'], reverse=True)
        save_scores(scores[:100])

    def show_highscores(self):
        # Simple modal overlay
        scores = load_scores()
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        title = " HIGH SCORES "
        self.stdscr.addstr(2, (w-len(title))//2, title, curses.color_pair(5) | curses.A_BOLD)
        
        if not scores:
            self.stdscr.addstr(5, 5, "No scores recorded yet.", curses.color_pair(4))
        else:
            self.stdscr.addstr(4, 5, "Date       Mode    WPM  Acc%   Topic/Bank", curses.color_pair(5))
            for i, s in enumerate(scores[:15]): # Show top 15
                line = f"{s['date']} {s['mode']:<6} {s['wpm']:>3} {s['accuracy']:>5.1f}   {s.get('length_cat', s.get('word_bank', 'N/A'))}"
                try:
                    self.stdscr.addstr(6 + i, 5, line, curses.color_pair(1 if i == 0 else 4))
                except curses.error:
                    pass
        
        self.stdscr.addstr(h-2, 2, " Press Enter to close ", curses.color_pair(5) | curses.A_DIM)
        self.stdscr.refresh()
        
        # Wait for enter
        while True:
            k = self.stdscr.getch()
            if k == 10 or k == curses.KEY_ENTER:
                break
        # Redraw main screen logic handled by main loop

    def run(self):
        curses.curs_set(0) # Hide system cursor
        self.stdscr.nodelay(True) # Non-blocking input
        
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
    
    mode = args.mode
    length_cat = args.length
    word_bank = args.bank
    target = args.count
    
    # Override bank if mode is quote
    if mode == 'quote' or mode == 'zen':
        word_bank = "N/A"
    
    app = TypingApp(stdscr, mode, target_count=target, length_cat=length_cat, word_bank=word_bank)
    app.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scribere Typing Tutor")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start a typing test')
    start_parser.add_argument('mode', choices=['rand', 'quote', 'zen', 'custom'], help='Test mode')
    start_parser.add_argument('--count', '-c', type=int, default=25, help='Number of words (for rand)')
    start_parser.add_argument('--length', '-l', choices=['short', 'medium', 'long', 'longest'], help='Quote length')
    start_parser.add_argument('--bank', '-b', choices=['common', 'complex'], default='common', help='Word bank for random')
    
    # Config command
    subparsers.add_parser('config', help='Show config path')
    
    args = parser.parse_args()
    
    if args.command == 'start':
        # Map positional argument from user input like "rand-25" if passed differently?
        # The launcher handles parsing "rand-25" into mode=rand, count=25
        # But if called directly via python scribere.py start rand --count 25
        pass
    elif args.command == 'config':
        print(f"Config: {CONFIG_FILE}")
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(0)

    # Launch curses
    try:
        curses.wrapper(lambda stdscr: main_cli(stdscr, args))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
