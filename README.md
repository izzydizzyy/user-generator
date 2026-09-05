# user-generator

small terminal-based TikTok username generator/checker.

generates short 3-4 character usernames and checks whether they look available on TikTok.

## features

- generates 3-4 character usernames
- tries to make them feel short / rare
- checks multiple usernames at once
- supports up to 5000 usernames per run
- colored terminal output
- no extra packages required

## requirements

- Python 3
- internet connection

## setup

clone the repo:

```bash
git clone https://github.com/izzydizzyy/user-generator.git
cd user-generator
```

or just download `app.py`.

## run

Windows:

```powershell
py app.py
```

macOS / Linux:

```bash
python3 app.py
```

then enter how many usernames you want generated:

```text
user-generator
tiktok / 3-4 char usernames

[?] how many do u want generated... 500
```

max: `5000`

## output

```text
[available] qvx
[taken]     izzy
[available] z7k
[retry]     xva
```

- `[available]` - the username appears to be available
- `[taken]` - a TikTok profile was found for the username
- `[retry]` - TikTok did not return a reliable result, usually because of a request error or rate limit

when the run finishes you'll get a small summary:

```text
done / checked 500 / found 12 available
```

## note

availability checks are not guaranteed to be 100% accurate. TikTok can rate-limit requests or change how profile pages respond, so always double-check a username before using it.

## license

use it, change it, mess with it. just don't be weird with it lol.
