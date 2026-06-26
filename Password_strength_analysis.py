import re
import hashlib
import requests

# -------------------------------------------------------
# FUNCTION: check_breach
# Hashes the password using SHA-1 and checks the first 5
# characters against the HaveIBeenPwned API (k-anonymity).
# Returns the number of times the password has been breached,
# or 0 if it has never appeared in a known breach.
# -------------------------------------------------------
def check_breach(password):
    # Hash the password using SHA-1 and convert to uppercase hex string
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # Split the hash — only the prefix is sent to the API
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    # Send only the prefix to the API (password is never exposed)
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    
    # Check each returned hash to see if our suffix matches
    for line in response.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return int(count)  # Return how many times this password was breached
    
    return 0  # Password not found in any known breach


# -------------------------------------------------------
# WELCOME & USER INPUT
# -------------------------------------------------------
print("---- Welcome to the Password Strength Analyzer, here we will gather data and calculate your password strength, and determine how likely you will be hacked. ----")
print()

# Collect personal info to check against the password later
name = input("Please enter your name: ")
username = input("Please enter your username: ")
birth_date = input("Please enter your birth year: ")
password = input("Enter your password (case sensitive): ")


# -------------------------------------------------------
# COMPLEXITY CHECKS
# Each check uses regex to detect a character type in the password
# -------------------------------------------------------
has_upper   = bool(re.search(r'[A-Z]', password))   # At least one uppercase letter
has_lower   = bool(re.search(r'[a-z]', password))   # At least one lowercase letter
has_digit   = bool(re.search(r'[0-9]', password))   # At least one number
has_special = bool(re.search(r'[!@#$%^&*]', password))  # At least one special character
is_long     = bool(re.search(r'.{8,}', password))   # At least 8 characters long


# -------------------------------------------------------
# SCORING
# Each passed complexity check adds 1 point (max score: 5)
# -------------------------------------------------------
score = 0

if is_long:     score += 1
if has_upper:   score += 1
if has_lower:   score += 1
if has_digit:   score += 1
if has_special: score += 1


# -------------------------------------------------------
# ANALYSIS OUTPUT
# -------------------------------------------------------
print()
print("---- Password Analysis ----")
print(f"Length 8+:        {is_long}")
print(f"Has Uppercase:    {has_upper}")
print(f"Has Lowercase:    {has_lower}")
print(f"Has Digit:        {has_digit}")
print(f"Has Special Char: {has_special}")
print(f"Score:            {score}/5")

# Warn the user if their password contains personal information
if name.lower() in password.lower() or birth_date in password or username.lower() in password.lower():
    print("Warning: Your password contains personal information — this makes it much easier to guess!")


# -------------------------------------------------------
# BREACH CHECK
# Adjusts the score based on how many times the password
# has appeared in real-world data breaches
# -------------------------------------------------------
breach_count = check_breach(password)

if breach_count > 100000:
    # Extremely common breached password — override score entirely
    print(f"⚠️  This password has appeared in {breach_count:,} data breaches!")
    score = 0
elif breach_count > 0:
    # Breached but less common — dock 2 points
    print(f"⚠️  This password has appeared in {breach_count:,} data breaches!")
    score -= 2
else:
    print("✅ This password has not appeared in any known breaches.")


# -------------------------------------------------------
# FINAL STRENGTH RATING
# Evaluated after breach adjustment so breach data is reflected
# -------------------------------------------------------
if score <= 0:
    password_strength = "Critically Weak"
elif score <= 2:
    password_strength = "Weak"
elif score == 3:
    password_strength = "Fair"
elif score == 4:
    password_strength = "Strong"
else:
    password_strength = "Very Strong"

print(f"Final Password Strength: {password_strength}")