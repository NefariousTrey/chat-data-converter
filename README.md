# Distill (free)

`chatconv.py` is the Distill program file; the commands below work as before.

Convert chat transcripts between plain text and JSONL (the `{"messages":[...]}` format used for chat datasets). One Python 3 file, standard library only, no installs, runs offline.

## Usage

    python3 chatconv.py txt2jsonl samples/chat.txt out.jsonl
    python3 chatconv.py jsonl2txt out.jsonl back.txt

## Text format
- Lines start with `User:`, `Assistant:` or `System:` (any capitalization).
- Lines without a prefix continue the previous message.
- Separate conversations with a line containing only `---`.
- Sections with no messages are skipped.

## Tests

    python3 test_chatconv.py

## Other products
See OTHER-PRODUCTS.md

## Support
Questions or bugs: open an issue on this repo or email nefarioustrey-support@agentmail.to

## License
License: see LICENSE
