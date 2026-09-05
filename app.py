import random
import re
import time
import urllib.error
import urllib.request

# user-generator
# tiny tiktok username checker

GREEN = "\033[92m"
RED = "\033[91m"
GRAY = "\033[90m"
RESET = "\033[0m"

LETTERS = "abcdefghijklmnopqrstuvwxyz"
RARE = "qzxvkjyw"
VOWELS = "aeiou"
DIGITS = "0123456789"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/152.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def rare_username():
    length = random.choice((3, 3, 4, 4, 4))
    style = random.randint(1, 5)

    if style == 1:
        # short + pronounceable: vex, qin, zov
        name = random.choice(RARE) + random.choice(VOWELS) + random.choice(LETTERS)
        if length == 4:
            name += random.choice(LETTERS)

    elif style == 2:
        # sharper looking: qvx, zyk, xvra
        name = "".join(
            random.choice(RARE if i % 2 == 0 else LETTERS)
            for i in range(length)
        )

    elif style == 3:
        # clean random letters
        name = "".join(random.choice(LETTERS) for _ in range(length))

    elif style == 4:
        # one number, still 3-4 chars
        chars = [random.choice(LETTERS) for _ in range(length)]
        chars[random.randrange(length)] = random.choice(DIGITS)
        name = "".join(chars)

    else:
        # rare first/last character
        if length == 3:
            name = random.choice(RARE) + random.choice(LETTERS) + random.choice(RARE)
        else:
            name = (
                random.choice(RARE)
                + random.choice(LETTERS)
                + random.choice(VOWELS)
                + random.choice(RARE)
            )

    return name.lower()


def is_available(username):
    url = f"https://www.tiktok.com/@{username}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=7) as response:
            html = response.read().decode("utf-8", errors="ignore")

        # TikTok normally embeds the profile's uniqueId in the page when it exists.
        patterns = (
            rf'"uniqueId":"{re.escape(username)}"',
            rf'\\"uniqueId\\":\\"{re.escape(username)}\\"',
        )

        return not any(re.search(pattern, html, re.IGNORECASE) for pattern in patterns)

    except urllib.error.HTTPError as error:
        if error.code == 404:
            return True
        return None
    except (urllib.error.URLError, TimeoutError):
        return None


def main():
    print("user-generator")
    print(f"{GRAY}tiktok / 3-4 char usernames{RESET}\n")

    seen = set()
    available = 0

    try:
        while True:
            username = rare_username()
            if username in seen:
                continue

            seen.add(username)
            result = is_available(username)

            if result is True:
                available += 1
                print(f"{GREEN}[available]{RESET} {username}")
            elif result is False:
                print(f"{RED}[taken]{RESET}     {username}")
            else:
                print(f"{GRAY}[retry]{RESET}     {username}")

            time.sleep(random.uniform(0.65, 1.15))

    except KeyboardInterrupt:
        print(f"\n{GRAY}stopped / found {available} available{RESET}")


if __name__ == "__main__":
    main()
