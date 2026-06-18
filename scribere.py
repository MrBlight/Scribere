import curses
import random
import time
import os
import json
import sys
import argparse
import urllib.request
import io
from typing import List, Dict, Any, Optional, Tuple

# Try to import Pillow for the easter egg
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- Configuration & Constants ---

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".scribere")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SCORES_FILE = os.path.join(CONFIG_DIR, "scores.json")

# Display constants
MIN_TERMINAL_WIDTH = 40
MIN_TERMINAL_HEIGHT = 15
MAX_HISTORY_SIZE = 100
MAX_HIGHSCORES_DISPLAY = 15
MENU_WIDTH = 60
MENU_HEIGHT = 14
SUBMENU_WIDTH = 40
SUBMENU_HEIGHT = 10

# Easter egg configuration
EASTER_EGG_URL = "https://f4.bcbits.com/img/a1664460568_10.jpg"
EASTER_EGG_TIMEOUT = 10

# ASCII art gradient characters (from dark to light) - IMPROVED QUALITY
ASCII_GRADIENT = "█▓▒░ "

# Word count validation
MIN_WORD_COUNT = 5
MAX_WORD_COUNT = 500
DEFAULT_WORD_COUNT = 25

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

# Weighted list: Common words appear multiple times
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

def ensure_config() -> None:
    """Ensure configuration directory and files exist with defaults."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE):
        default_config: Dict[str, Any] = {
            "color_theme": "default",
            "minimal_stats": False,
            "word_bank": "common",
            "smart_sentences": False,
            "default_mode": "rand",
            "default_count": DEFAULT_WORD_COUNT
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            json.dump([], f)

def load_config() -> Dict[str, Any]:
    """Load configuration from file with fallback defaults."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "word_bank": "common",
            "smart_sentences": False,
            "minimal_stats": False,
            "default_mode": "rand",
            "default_count": DEFAULT_WORD_COUNT
        }

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_scores() -> List[Dict[str, Any]]:
    """Load scores from file with fallback to empty list."""
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_scores(scores: List[Dict[str, Any]]) -> None:
    """Save scores to file."""
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def get_random_words(count: int, word_bank: str = "common", smart: bool = False) -> str:
    """Generate random words or smart sentences for typing practice."""
    # Validate count
    count = max(MIN_WORD_COUNT, min(MAX_WORD_COUNT, count))
    
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

# --- Easter Egg Logic ---

def fetch_and_convert_image(url: str) -> List[str]:
    """Fetch an image from URL and convert to ASCII art with improved quality."""
    if not PIL_AVAILABLE:
        return ["Pillow library not installed.", "Run: pip install Pillow"]
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=EASTER_EGG_TIMEOUT)
        img_data = response.read()
        
        img = Image.open(io.BytesIO(img_data))
        
        # Get terminal size
        h_term, w_term = os.get_terminal_size()
        # Calculate max usable size (leave some margin)
        max_w = w_term - 4
        max_h = h_term - 6  # Extra space for instructions
        
        # Resize image maintaining aspect ratio
        # Terminal characters are typically ~2x taller than wide
        aspect = img.width / img.height
        new_w = max_w
        new_h = int(new_w / aspect * 0.5)
        
        if new_h > max_h:
            new_h = max_h
            new_w = int(new_h * aspect * 2)  # Compensate for character aspect ratio
            
        img = img.convert('L').resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        pixels = list(img.getdata())
        
        # Use gradient characters for better detail representation
        ascii_lines = []
        for i in range(new_h):
            line = ""
            for j in range(new_w):
                pixel = pixels[i * new_w + j]
                # Map pixel value (0-255) to gradient index
                char_idx = min(pixel // (256 // len(ASCII_GRADIENT)), len(ASCII_GRADIENT) - 1)
                line += ASCII_GRADIENT[char_idx]
            ascii_lines.append(line)
        
        return ascii_lines
    except urllib.error.URLError as e:
        return [f"Network error: {str(e)}", "Check internet connection."]
    except Exception as e:
        return [f"Error loading image: {str(e)}", "Try again later."]


def show_secret_screen(stdscr) -> None:
    """Display the Easter egg image without text."""
    stdscr.clear()
    stdscr.nodelay(False)
    curses.curs_set(0)
    
    h, w = stdscr.getmaxyx()
    
    # Fetch and display image only (no title text)
    lines = fetch_and_convert_image(EASTER_EGG_URL)
    
    start_y = 1
    for i, line in enumerate(lines):
        if start_y + i >= h - 2:
            break
        x_pos = max(0, (w - len(line)) // 2)
        try:
            # Use cyan color for the image
            stdscr.addstr(start_y + i, x_pos, line, curses.color_pair(6) | curses.A_BOLD)
        except curses.error:
            pass
    
    msg = " Press any key to return "
    try:
        stdscr.addstr(h - 2, (w - len(msg)) // 2, msg, curses.color_pair(5) | curses.A_DIM)
    except curses.error:
        pass
    stdscr.refresh()
    stdscr.getch()

# --- Application Logic ---

class TypingApp:
    def __init__(self, stdscr, mode='rand', target_count=25, word_bank="common"):
        self.stdscr = stdscr
        self.mode = mode
        self.target_count = target_count
        self.word_bank = word_bank
        self.config = load_config()
        
        self.smart_mode = self.config.get("smart_sentences", False)
            
        self.text = ""
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.cursor_pos = 0
        self.errors = 0
        self.total_chars_typed = 0
        self.show_menu = False
        self.show_main_menu = False
        
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

    def draw_main_menu(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()
        
        # Main Menu Box
        menu_h, menu_w = MENU_HEIGHT, MENU_WIDTH
        start_y, start_x = (h - menu_h) // 2, (w - menu_w) // 2
        
        win = curses.newwin(menu_h, menu_w, start_y, start_x)
        win.box()
        win.keypad(True)
        
        title = " SCRIBERE MAIN MENU "
        win.addstr(0, (menu_w - len(title)) // 2, title, curses.color_pair(5) | curses.A_BOLD)
        
        options = [
            f"1. Start Random ({self.target_count} words)",
            f"2. Start Zen Mode ({self.target_count} words)",
            "3. Toggle Word Bank (Common/Complex)",
            "4. Toggle Smart Sentences",
            "5. Set Word Count",
            "6. View High Scores",
            "7. Secret",
            "8. Quit"
        ]
        
        for i, opt in enumerate(options):
            win.addstr(2 + i, 2, opt, curses.color_pair(6))
        
        status = f" Current: {self.word_bank.upper()} | Smart: {'ON' if self.smart_mode else 'OFF'} "
        win.addstr(menu_h - 2, 2, status, curses.color_pair(5) | curses.A_DIM)
        win.addstr(menu_h - 3, 2, " Select (1-8) ", curses.color_pair(5) | curses.A_DIM)
        win.refresh()
        
        while True:
            key = win.getch()
            if key == ord('1'):
                self.mode = 'rand'
                self.show_main_menu = False
                self.reset_test()
                break
            elif key == ord('2'):
                self.mode = 'zen'
                self.show_main_menu = False
                self.reset_test()
                break
            elif key == ord('3'):
                self.config["word_bank"] = "complex" if self.config.get("word_bank") == "common" else "common"
                save_config(self.config)
                self.word_bank = self.config["word_bank"]
                self.draw_main_menu() # Redraw to update status
                break
            elif key == ord('4'):
                self.config["smart_sentences"] = not self.config.get("smart_sentences", False)
                save_config(self.config)
                self.smart_mode = self.config["smart_sentences"]
                self.draw_main_menu()
                break
            elif key == ord('5'):
                # Simple input for count with validation
                curses.echo()
                win.addstr(menu_h - 2, 2, f" Enter word count ({MIN_WORD_COUNT}-{MAX_WORD_COUNT}): ")
                win.refresh()
                try:
                    input_str = win.getstr(menu_h - 2, 48, 4).decode('utf-8')
                    if input_str.isdigit():
                        count = int(input_str)
                        if MIN_WORD_COUNT <= count <= MAX_WORD_COUNT:
                            self.target_count = count
                            self.config["default_count"] = self.target_count
                            save_config(self.config)
                        else:
                            win.addstr(menu_h - 1, 2, f" Please enter {MIN_WORD_COUNT}-{MAX_WORD_COUNT} ", curses.color_pair(2))
                except (ValueError, UnicodeDecodeError):
                    pass
                curses.noecho()
                self.draw_main_menu()
                break
            elif key == ord('6'):
                self.show_main_menu = False
                self.show_highscores()
                self.show_main_menu = True # Return to menu after scores
                self.draw_main_menu()
                break
            elif key == ord('7'):
                self.show_main_menu = False
                show_secret_screen(self.stdscr)
                self.show_main_menu = True
                self.draw_main_menu()
                break
            elif key == ord('8') or key == 27:
                self.running = False
                break

    def draw_screen(self) -> None:
        """Draw the main typing screen with text and statistics."""
        if self.show_main_menu:
            self.draw_main_menu()
            return
        
        if self.show_menu:
            self.draw_submenu()
            return
        
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        # Validate terminal size
        if height < MIN_TERMINAL_HEIGHT or width < MIN_TERMINAL_WIDTH:
            try:
                self.stdscr.addstr(0, 0, f"Terminal too small. Need {MIN_TERMINAL_WIDTH}x{MIN_TERMINAL_HEIGHT}", curses.color_pair(2))
            except curses.error:
                pass
            self.stdscr.refresh()
            return
        
        try:
            self.stdscr.box()
            self.stdscr.attron(curses.color_pair(5))
            self.stdscr.box()
            self.stdscr.attroff(curses.color_pair(5))
        except curses.error:
            pass
        
        title = " SCRIBERE "
        start_x = max(0, (width - len(title)) // 2)
        try:
            self.stdscr.addstr(0, start_x, title, curses.color_pair(5) | curses.A_BOLD)
        except curses.error:
            pass
        
        status = f" Mode: {self.mode.upper()} | Words: {self.target_count} | Bank: {self.word_bank} "
        if self.finished:
            status = " TEST COMPLETE "
        try:
            self.stdscr.addstr(2, 2, status, curses.color_pair(5))
        except curses.error:
            pass
        
        start_row = 4
        max_rows = height - 8
        max_cols = width - 4
        
        # Word wrapping logic
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
        
        # Find cursor line index
        current_flat = 0
        cursor_line_idx = 0
        for l_idx, line in enumerate(wrapped_lines):
            if current_flat + len(line) >= flat_cursor:
                cursor_line_idx = l_idx
                break
            current_flat += len(line)
        
        # Calculate scroll offset to keep cursor visible
        scroll_offset = 0
        if cursor_line_idx >= max_rows:
            scroll_offset = cursor_line_idx - max_rows + 1
        
        visible_lines = wrapped_lines[scroll_offset : scroll_offset + max_rows]
        global_flat_idx = sum(len(l) for l in wrapped_lines[:scroll_offset])
        
        # Render visible lines
        for r_idx, line in enumerate(visible_lines):
            screen_r = start_row + r_idx
            if screen_r >= height - 2:
                break
            
            for c_idx, char in enumerate(line):
                char_idx_global = global_flat_idx + c_idx
                
                attr = curses.color_pair(4)
                
                if char_idx_global < len(self.user_input):
                    u_char = self.user_input[char_idx_global]
                    if u_char == char:
                        attr = curses.color_pair(1)  # Correct
                    else:
                        attr = curses.color_pair(2)  # Error
                
                if char_idx_global == flat_cursor and not self.finished:
                    attr = curses.color_pair(3) | curses.A_REVERSE  # Cursor
                
                try:
                    self.stdscr.addch(screen_r, 2 + c_idx, char, attr)
                except curses.error:
                    pass
            
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
            except curses.error:
                pass
        
        self.stdscr.refresh()

    def draw_submenu(self) -> None:
        """Draw the pause submenu."""
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()
        menu_h, menu_w = SUBMENU_HEIGHT, SUBMENU_WIDTH
        start_y, start_x = (h - menu_h) // 2, (w - menu_w) // 2
        win = curses.newwin(menu_h, menu_w, start_y, start_x)
        win.box()
        win.addstr(0, (menu_w - 6) // 2, " PAUSE ", curses.color_pair(5) | curses.A_BOLD)
        opts = ["1. Resume", "2. Main Menu", "3. Quit"]
        for i, o in enumerate(opts):
            win.addstr(2 + i, 2, o, curses.color_pair(6))
        win.addstr(menu_h - 2, 2, " Select (1-3) ", curses.color_pair(5))
        win.refresh()
        
        key = win.getch()
        if key == ord('1'):
            self.show_menu = False
        elif key == ord('2'):
            self.show_menu = False
            self.show_main_menu = True
        elif key == ord('3'):
            self.running = False

    def reset_test(self) -> None:
        """Reset the typing test with new text."""
        self.text = get_random_words(self.target_count, self.word_bank, self.smart_mode)
        self.user_input = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.cursor_pos = 0
        self.errors = 0
        self.total_chars_typed = 0

    def get_accuracy(self) -> float:
        """Calculate typing accuracy as a percentage."""
        if len(self.user_input) == 0:
            return 100.0
        correct = sum(1 for i, c in enumerate(self.user_input) if i < len(self.text) and c == self.text[i])
        return (correct / len(self.user_input)) * 100

    def draw_results(self, row: int, width: int) -> None:
        """Draw the results screen after test completion."""
        elapsed = 0.0
        if self.start_time and self.end_time:
            elapsed = self.end_time - self.start_time
        
        # Avoid division by zero
        if elapsed > 0:
            wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0))
        else:
            wpm = 0
        
        acc = self.get_accuracy()
        
        try:
            self.stdscr.addstr(row, max(0, (width - 9) // 2), " RESULTS ", curses.color_pair(5) | curses.A_BOLD)
        except curses.error:
            pass
        
        minimal = self.config.get("minimal_stats", False)
        if minimal:
            stats = f" WPM: {wpm} | Accuracy: {acc:.1f}% "
        else:
            stats = f" WPM: {wpm} | Accuracy: {acc:.1f}% | Errors: {self.errors} | Time: {elapsed:.1f}s "
        
        try:
            self.stdscr.addstr(row + 2, 2, stats, curses.color_pair(1) | curses.A_BOLD)
            self.stdscr.addstr(row + 4, 2, " Enter: Retry | M: Scores | Esc: Menu ", curses.color_pair(5) | curses.A_DIM)
        except curses.error:
            pass

    def handle_input(self, key: int) -> None:
        """Handle keyboard input for typing and navigation."""
        if self.show_main_menu or self.show_menu:
            return  # Handled in respective draw methods
        
        if self.finished:
            if key in (10, curses.KEY_ENTER):
                self.reset_test()
            elif key in (ord('m'), ord('M')):
                self.show_highscores()
            elif key == 27:
                self.show_menu = True
            return
        
        if key == 27:
            self.show_menu = True
            return
        
        if self.mode == 'zen' and key in (10, curses.KEY_ENTER, 343):
            self.finish_test()
            return
        
        if key in (curses.KEY_BACKSPACE, 127, 8):
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
                        self.user_input = self.user_input[:self.cursor_pos] + char + self.user_input[self.cursor_pos + 1:]
                    else:
                        self.user_input += char
                
                if self.cursor_pos < len(self.text):
                    if self.user_input[self.cursor_pos] != self.text[self.cursor_pos]:
                        self.errors += 1
                
                self.cursor_pos += 1
                self.total_chars_typed += 1
                
                if self.cursor_pos == len(self.text):
                    self.finish_test()
        
        # Start timer on first keystroke
        if not self.finished and self.start_time is None and len(self.user_input) > 0:
            self.start_time = time.time()

    def finish_test(self) -> None:
        """Mark test as finished and save score."""
        if not self.finished:
            self.finished = True
            self.end_time = time.time()
            self.save_score()

    def save_score(self) -> None:
        """Save the current test score to the scores file."""
        elapsed = self.end_time - self.start_time if self.end_time and self.start_time else 0.0
        
        # Avoid division by zero
        if elapsed > 0:
            wpm = int((len(self.user_input) / 5.0) / (elapsed / 60.0))
        else:
            wpm = 0
        
        acc = self.get_accuracy()
        
        score_entry: Dict[str, Any] = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "mode": self.mode,
            "word_bank": self.word_bank,
            "smart": self.smart_mode,
            "wpm": wpm,
            "accuracy": round(acc, 1),
            "errors": self.errors,
            "chars": len(self.user_input)
        }
        
        scores = load_scores()
        scores.append(score_entry)
        scores.sort(key=lambda x: x['wpm'], reverse=True)
        save_scores(scores[:MAX_HISTORY_SIZE])

    def show_highscores(self) -> None:
        """Display the high scores screen."""
        scores = load_scores()
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        self.stdscr.addstr(2, max(0, (w - 13) // 2), " HIGH SCORES ", curses.color_pair(5) | curses.A_BOLD)
        
        if not scores:
            self.stdscr.addstr(5, 5, "No scores recorded yet.", curses.color_pair(4))
        else:
            self.stdscr.addstr(4, 5, "Date       Mode    WPM  Acc%   Bank", curses.color_pair(5))
            for i, s in enumerate(scores[:MAX_HIGHSCORES_DISPLAY]):
                bank = s.get('word_bank', 'N/A')
                if s.get('smart'):
                    bank += " (Smart)"
                line = f"{s['date']} {s['mode']:<6} {s['wpm']:>3} {s['accuracy']:>5.1f}   {bank}"
                try:
                    self.stdscr.addstr(6 + i, 5, line, curses.color_pair(1 if i == 0 else 4))
                except curses.error:
                    pass
        
        self.stdscr.addstr(h - 2, 2, " Press Enter to close ", curses.color_pair(5) | curses.A_DIM)
        self.stdscr.refresh()
        
        while True:
            k = self.stdscr.getch()
            if k in (10, curses.KEY_ENTER):
                break

    def run(self) -> None:
        """Main application loop."""
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        # Start with Main Menu
        self.show_main_menu = True
        
        while self.running:
            self.draw_screen()
            try:
                key = self.stdscr.getch()
                if key != -1 and not self.show_main_menu and not self.show_menu:
                    self.handle_input(key)
            except KeyboardInterrupt:
                break
        
        curses.curs_set(1)

def main_cli(stdscr, args) -> None:
    """Main CLI entry point."""
    ensure_config()
    
    if args.command == 'secret':
        show_secret_screen(stdscr)
        return
    
    # If launched via CLI with args, skip main menu
    if args.command == 'start':
        # Validate count argument
        count = max(MIN_WORD_COUNT, min(MAX_WORD_COUNT, args.count))
        app = TypingApp(stdscr, mode=args.mode, target_count=count, word_bank=args.bank)
        app.show_main_menu = False
        app.run()
    else:
        # Default launch (double click) -> Main Menu
        config = load_config()
        default_count = config.get('default_count', DEFAULT_WORD_COUNT)
        # Ensure default count is within bounds
        default_count = max(MIN_WORD_COUNT, min(MAX_WORD_COUNT, default_count))
        app = TypingApp(
            stdscr,
            mode=config.get('default_mode', 'rand'),
            target_count=default_count,
            word_bank=config.get('word_bank', 'common')
        )
        app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scribere Typing Tutor")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    start_parser = subparsers.add_parser('start', help='Start a typing test')
    start_parser.add_argument('mode', choices=['rand', 'zen'], help='Test mode')
    start_parser.add_argument('--count', '-c', type=int, default=DEFAULT_WORD_COUNT, help=f'Number of words ({MIN_WORD_COUNT}-{MAX_WORD_COUNT})')
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
        args.command = 'default'
    
    try:
        curses.wrapper(lambda stdscr: main_cli(stdscr, args))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
