#!/usr/bin/env bash
# Copy the Friendstead notes out of the Obsidian vault into this repo.
# The vault (~/Documents/Notes) is where notes are edited; this folder is the versioned copy.
set -euo pipefail
VAULT="${VAULT:-$HOME/Documents/Notes}"
HERE="$(cd "$(dirname "$0")" && pwd)"
rsync -a --delete --exclude '.obsidian' "$VAULT/10 Projects/Friendstead/" "$HERE/Friendstead/"
mkdir -p "$HERE/Library" "$HERE/Attachments"
cp -p "$VAULT/30 Library/Papers/Texas Self-Build Community Structure Memo.md" "$HERE/Library/"
rsync -a --delete --include 'friendstead-*' --exclude '*' "$VAULT/Attachments/" "$HERE/Attachments/"
echo "synced $(find "$HERE/Friendstead" -name '*.md' | wc -l) notes, $(ls "$HERE/Attachments" | wc -l) attachments"
