import random
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

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
WORKERS = 20

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
        name = random.choice(RARE) + random.choice(VOWELS) + random.choice(LETTERS)
        if length == 4:
            name += random.choice(LETTERS)

    elif style == 2:
        name = "".join(
            random.choice(RARE if i % 2 == 0 else LETTERS)
            for i in range(length)
        )

    elif style == 3:
        name = "".join(random.choice(LETTERS) for _ in range(length))

    elif style == 4:
        chars = [random.choice(LETTERS) for _ in range(length)]
        chars[random.randrange(length)] = random.choice(DIGITS)
        name = "".join(chars)

    else:
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


def generate_usernames(amount):
    names = set()

    while len(names) < amount:
        names.add(rare_username())

    return list(names)


def is_available(username):
    url = f"https://www.tiktok.com/@{username}"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=4) as response:
            html = response.read().decode("utf-8", errors="ignore")

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


def ask_amount():
    while True:
        try:
            amount = int(input("[?] how many do u want generated... "))

            if 1 <= amount <= 5000:
                return amount

            print(f"{GRAY}[!] max is 5000{RESET}")

        except ValueError:
            print(f"{GRAY}[!] enter a number{RESET}")


def main():
    print("user-generator")
    print(f"{GRAY}tiktok / 3-4 char usernames{RESET}\n")

    amount = ask_amount()
    usernames = generate_usernames(amount)
    available = 0

    print()

    try:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            jobs = {
                pool.submit(is_available, username): username
                for username in usernames
            }

            for job in as_completed(jobs):
                username = jobs[job]
                result = job.result()

                if result is True:
                    available += 1
                    print(f"{GREEN}[available]{RESET} {username}")
                elif result is False:
                    print(f"{RED}[taken]{RESET}     {username}")
                else:
                    print(f"{GRAY}[retry]{RESET}     {username}")

    except KeyboardInterrupt:
        print(f"\n{GRAY}stopped / found {available} available{RESET}")
        return

    print(f"\n{GRAY}done / checked {amount} / found {available} available{RESET}")


if __name__ == "__main__":
    main()
