import math
import random
import time
import os

class PasswordStrengthChecker:
    def __init__(self):
        """Initialize password checker"""
        
        # Default built-in wordlists
        self.common_passwords = [
            "password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567",
            "letmein", "trustno1", "dragon", "baseball", "iloveyou", "master", "sunshine",
            "ashley", "bailey", "passw0rd", "shadow", "123123", "654321", "superman",
            "qazwsx", "michael", "football", "password1", "password123", "batman",
            "login", "admin", "welcome", "hello", "charlie", "donald", "password12",
            "admin123", "root", "toor", "pass", "test", "guest", "master123", "fuckyou"
        ]
        
        self.dictionary_words = [
            "apple", "brave", "cloud", "dance", "eagle", "flame", "grape", "happy",
            "island", "jumbo", "kite", "lemon", "magic", "night", "ocean", "planet",
            "quest", "rainy", "solar", "tiger", "unity", "vivid", "whale", "xenon",
            "yacht", "zebra", "alarm", "bloom", "crest", "dream", "earth", "frost",
            "guard", "heart", "ivory", "joy", "king", "leaf", "mount", "noble"
        ]
        
        self.strong_words = [
            "apple", "brave", "cloud", "dance", "eagle", "flame", "grape", "happy",
            "island", "jumbo", "kite", "lemon", "magic", "night", "ocean", "planet",
            "quest", "rainy", "solar", "tiger", "unity", "vivid", "whale", "xenon",
            "yacht", "zebra", "alarm", "bloom", "crest", "dream", "earth", "frost",
            "guard", "heart", "ivory", "joy", "king", "leaf", "mount", "noble"
        ]
        
        # Load custom wordlist
        self.custom_wordlist = []
        self.wordlist_path = "rockyou.txt"
        self.load_wordlist()
        
        self.leetspeak_map = {
            'a': ['4', '@'], 'b': ['8'], 'e': ['3'], 'g': ['9', '6'],
            'i': ['1', '!'], 'o': ['0'], 's': ['5', '$'], 't': ['7', '+'], 'z': ['2']
        }
        
        self.common_suffixes = ["123", "456", "789", "000", "1", "2", "12", "21", "2023", "2024"]
    
    def load_wordlist(self):
        """Load custom wordlist from file"""
        print(f"\n📂 Loading wordlist from: {self.wordlist_path}")
        
        start_time = time.time()
        
        try:
            if os.path.exists(self.wordlist_path):
                with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.custom_wordlist = [line.strip() for line in f if line.strip()]
                
                elapsed = time.time() - start_time
                print(f"✅ Loaded {len(self.custom_wordlist):,} passwords in {elapsed:.2f} seconds")
            else:
                print(f"⚠️  Wordlist file not found: {self.wordlist_path}")
                print(f"   Using built-in wordlist only")
                elapsed = time.time() - start_time
                print(f"⚠️  Loaded 0 passwords in {elapsed:.2f} seconds")
                
        except Exception as e:
            print(f"❌ Error loading wordlist: {e}")
            self.custom_wordlist = []
    
    def get_charset_size(self, password):
        """Determine character set size"""
        size = 0
        has_lower = has_upper = has_digit = has_symbol = False
        
        for char in password:
            if char.islower():
                has_lower = True
            elif char.isupper():
                has_upper = True
            elif char.isdigit():
                has_digit = True
            elif not char.isalnum():
                has_symbol = True
        
        if has_lower:
            size += 26
        if has_upper:
            size += 26
        if has_digit:
            size += 10
        if has_symbol:
            size += 32
        
        return size if size > 0 else 26
    
    def calculate_entropy(self, password):
        """Calculate password entropy"""
        pool_size = self.get_charset_size(password)
        entropy = len(password) * math.log2(pool_size)
        return entropy, pool_size
    
    def format_time_detailed(self, seconds):
        """Convert seconds to detailed time units"""
        if seconds <= 0:
            return {"seconds": 0, "days": 0, "months": 0, "years": 0, "centuries": 0}
        
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        weeks = days / 7
        months = days / 30
        years = days / 365
        centuries = years / 100
        
        result = {
            "seconds": round(seconds, 2),
            "minutes": round(minutes, 1),
            "hours": round(hours, 1),
            "days": round(days, 1),
            "weeks": round(weeks, 1),
            "months": round(months, 1),
            "years": round(years, 1),
            "centuries": round(centuries, 1)
        }
        
        return result
    
    def calculate_bruteforce_time(self, password):
        """Calculate brute force time"""
        pool_size = self.get_charset_size(password)
        length = len(password)
        
        total_combinations = pool_size ** length
        avg_guesses = total_combinations / 2
        
        guesses_per_second = 1000000000  # 1 billion
        seconds = avg_guesses / guesses_per_second
        
        return seconds, total_combinations
    
    def check_wordlist(self, password):
        """Check password against wordlists"""
        results = []
        check_start = time.time()
        
        # Check exact match in custom wordlist
        if self.custom_wordlist:
            # Convert to set for faster lookup
            wordlist_set = set(self.custom_wordlist)
            
            if password in wordlist_set:
                results.append({
                    "type": "ROCKYOU WORDLIST",
                    "severity": "🔴 CRITICAL",
                    "description": f"Found in rockyou.txt ({len(self.custom_wordlist):,} passwords)",
                    "time": "INSTANT",
                    "check_time": 0
                })
            elif password.lower() in wordlist_set:
                results.append({
                    "type": "ROCKYOU WORDLIST (lowercase)",
                    "severity": "🔴 CRITICAL",
                    "description": "Found in rockyou.txt (case-insensitive)",
                    "time": "INSTANT",
                    "check_time": 0
                })
        
        # Check built-in common passwords
        if password in self.common_passwords or password.lower() in self.common_passwords:
            results.append({
                "type": "BUILT-IN COMMON PASSWORD",
                "severity": "🔴 CRITICAL",
                "description": "Found in top 50 common passwords",
                "time": "INSTANT",
                "check_time": 0
            })
        
        # Check dictionary words
        if password.lower() in self.dictionary_words:
            results.append({
                "type": "DICTIONARY WORD",
                "severity": "🟠 HIGH",
                "description": "Is a plain dictionary word",
                "time": "INSTANT",
                "check_time": 0
            })
        
        # Check leetspeak variants
        password_lower = password.lower()
        for word in self.dictionary_words:
            if self.is_leetspeak_variant(password_lower, word):
                results.append({
                    "type": "LEETSPEAK VARIANT",
                    "severity": "🟠 HIGH",
                    "description": f"Common word with substitutions (e.g. {word})",
                    "time": "MILLISECONDS",
                    "check_time": 0
                })
                break
        
        # Check word + suffix
        for word in self.dictionary_words:
            for suffix in self.common_suffixes:
                if password_lower == word + suffix:
                    results.append({
                        "type": "WORD + SUFFIX",
                        "severity": "🟠 HIGH",
                        "description": f"Word with number appended ({word} + {suffix})",
                        "time": "INSTANT",
                        "check_time": 0
                    })
                    break
        
        # Check reversed word
        if password_lower[::-1] in self.dictionary_words:
            results.append({
                "type": "REVERSED WORD",
                "severity": "🟡 MEDIUM",
                "description": "Reversed dictionary word",
                "time": "INSTANT",
                "check_time": 0
            })
        
        check_time = time.time() - check_start
        return results, check_time
    
    def is_leetspeak_variant(self, password, word):
        """Check if password is a leetspeak variant"""
        if len(password) != len(word):
            return False
        
        for i, char in enumerate(password):
            if char == word[i]:
                continue
            if char in self.leetspeak_map.get(word[i], []):
                continue
            return False
        
        return True
    
    def get_strength_score(self, password):
        """Calculate password strength score"""
        score = 0
        entropy, pool_size = self.calculate_entropy(password)
        length = len(password)
        
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 10:
            score += 20
        elif length >= 8:
            score += 15
        elif length >= 6:
            score += 10
        else:
            score += 5
        
        if pool_size >= 70:
            score += 40
        elif pool_size >= 36:
            score += 30
        elif pool_size >= 26:
            score += 15
        else:
            score += 5
        
        if entropy >= 80:
            score += 30
        elif entropy >= 60:
            score += 20
        elif entropy >= 40:
            score += 10
        
        return min(score, 100)
    
    def get_strength_rating(self, score):
        """Get strength rating"""
        if score >= 80:
            return "VERY STRONG", "🛡️"
        elif score >= 60:
            return "STRONG", "⚠️"
        elif score >= 40:
            return "MODERATE", "⚠️⚠️"
        elif score >= 20:
            return "WEAK", "❌"
        else:
            return "VERY WEAK", "🚫"
    
    def check_password(self, password):
        """Check password strength with full analysis"""
        print("\n" + "="*60)
        print("              PASSWORD ANALYSIS")
        print("="*60)
        
        print(f"\n📝 Password: {password}")
        print(f"📏 Length: {len(password)} characters")
        
        # Wordlist analysis
        print(f"\n🔍 WORDLIST CHECKS:")
        wordlist_results, check_time = self.check_wordlist(password)
        
        if wordlist_results:
            for result in wordlist_results:
                print(f"   {result['severity']} {result['type']}")
                print(f"      → {result['description']}")
                print(f"      → Crack Time: {result['time']}")
        else:
            print("   ✅ No vulnerabilities found in wordlist checks")
        
        # Show check time
        print(f"\n⏱️  Wordlist Check Time: {check_time*1000:.4f} ms")
        
        # Entropy and stats
        entropy, pool_size = self.calculate_entropy(password)
        seconds, total_combos = self.calculate_bruteforce_time(password)
        time_data = self.format_time_detailed(seconds)
        score = self.get_strength_score(password)
        rating, icon = self.get_strength_rating(score)
        
        print(f"\n📊 STATISTICS:")
        print(f"   • Character Pool: {pool_size}")
        print(f"   • Total Combinations: {total_combos:,}")
        print(f"   • Entropy: {entropy:.2f} bits")
        
        print(f"\n⏱️  TIME TO BRUTE FORCE:")
        print(f"   ├─ Seconds: {time_data['seconds']:,.0f}")
        print(f"   ├─ Days: {time_data['days']:,.0f}")
        print(f"   ├─ Months: {time_data['months']:,.0f}")
        print(f"   ├─ Years: {time_data['years']:,.0f}")
        print(f"   └─ Centuries: {time_data['centuries']:,.0f}")
        
        print(f"\n💪 Strength: {rating} {icon} (Score: {score}/100)")
        
        # Recommendations
        print(f"\n💡 Tips:")
        if wordlist_results:
            print(f"   ❌ Password found in wordlist - DO NOT USE")
        if len(password) < 12:
            print(f"   ❌ Use at least 12 characters")
        if pool_size < 70:
            print(f"   ❌ Add UPPERCASE, numbers, and symbols")
        if score >= 80 and not wordlist_results:
            print(f"   ✅ Excellent! Very secure.")
        
        print("="*60)
        
        return score
    
    def generate_password(self):
        """Generate strong password"""
        words = random.sample(self.strong_words, 3)
        num = random.randint(1000, 9999)
        symbol = random.choice("!@#$%^&*")
        password = f"{words[0].capitalize()}-{words[1].capitalize()}-{words[2].capitalize()}-{num}{symbol}"
        return password
    
    def suggest_passwords(self, count=5):
        """Suggest multiple strong passwords"""
        print("\n" + "="*60)
        print("         SUGGESTED STRONG PASSWORDS")
        print("="*60)
        
        for i in range(count):
            pwd = self.generate_password()
            seconds, _ = self.calculate_bruteforce_time(pwd)
            time_data = self.format_time_detailed(seconds)
            score = self.get_strength_score(pwd)
            rating, icon = self.get_strength_rating(score)
            
            # Check wordlist
            wordlist, _ = self.check_wordlist(pwd)
            
            print(f"\n{i+1}. {pwd}")
            if wordlist:
                print(f"   ⚠️ May be in wordlist!")
            else:
                print(f"   Days: {time_data['days']:,.0f} | Years: {time_data['years']:,.0f}")
            print(f"   Strength: {rating} {icon}")


def main():
    checker = PasswordStrengthChecker()
    
    print("\n" + "🔐"*20)
    print("    PASSWORD STRENGTH CHECKER")
    print("🔐"*20)
    
    while True:
        print("\n" + "-"*40)
        print("OPTIONS:")
        print("  1. Check password strength")
        print("  2. Generate strong passwords")
        print("  3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            password = input("Enter password to check: ")
            checker.check_password(password)
            
        elif choice == "2":
            checker.suggest_passwords(5)
            
        elif choice == "3":
            print("\nGoodbye! Stay secure! 🔐\n")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
