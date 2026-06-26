# Password Strength Analyzer

A command-line tool built in Python that evaluates password strength using rule-based complexity checks and a live data breach lookup via the [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3).

---

## Features

- **Complexity Scoring** — checks for length, uppercase, lowercase, digits, and special characters
- **Personal Info Detection** — warns if your password contains your name, username, or birth year
- **Live Breach Check** — securely checks if your password has appeared in known data breaches
- **Breach-Aware Rating** — a password cannot score well if it has been widely compromised, regardless of complexity

---

## How It Works

### Rule-Based Scoring
The tool evaluates five criteria and assigns a score out of 5:

| Criteria | Points |
|---|---|
| 8+ characters | +1 |
| Contains uppercase letter | +1 |
| Contains lowercase letter | +1 |
| Contains a digit | +1 |
| Contains a special character | +1 |

Final strength ratings:

| Score | Rating |
|---|---|
| 0 or below | Critically Weak |
| 1 – 2 | Weak |
| 3 | Fair |
| 4 | Strong |
| 5 | Very Strong |

### HaveIBeenPwned API — k-Anonymity
The breach check uses a technique called **k-anonymity** to ensure your actual password is never sent over the internet:

1. Your password is hashed locally using **SHA-1**
2. Only the **first 5 characters** of that hash are sent to the API
3. The API returns all hashes beginning with those 5 characters
4. Your device checks locally whether your full hash appears in the results

This means the API never sees your password or your full hash — only a partial prefix shared by thousands of other hashes.

---

## Installation

**1. Clone the repository**
```
git clone https://github.com/YOUR_USERNAME/password-strength-analyzer.git
cd password-strength-analyzer
```

**2. Install dependencies**
```
pip install requests
```

**3. Run the program**
```
python password_analyzer.py
```

---

## Example Output

```
---- Password Analysis ----
Length 8+:        ✅
Has Uppercase:    ✅
Has Lowercase:    ✅
Has Digit:        ✅
Has Special Char: ❌
Score:            4/5

⚠️  This password has appeared in 454,458 data breaches!

Final Password Strength: Critically Weak
```

---

## Technologies Used

- Python 3
- `re` — regular expressions for complexity checks
- `hashlib` — SHA-1 hashing
- `requests` — HTTP requests to the HaveIBeenPwned API

---

## Security Note

This tool is intended for educational purposes. Never test passwords you actively use in production systems. All breach lookups are performed using k-anonymity — your password is never transmitted in any readable form.

---

## Author

Built by [Your Name] — BYU Information Systems Student
