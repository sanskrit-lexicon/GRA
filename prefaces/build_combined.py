#!/usr/bin/env python3
# Build consolidated single-file editions (German / English / Russian) of the
# GRA front matter from the per-page graprefNN.* transcriptions/translations.
# Adapted from PWG/prefaces/build_combined.py (canonical preface-OCR builder).
# Run from the prefaces/ directory:  python build_combined.py
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))

# NN, volume, (en_label, de_label, ru_label)
PAGES = [
    ("01", 1, "Title page (1873)", "Titelblatt (1873)", "Титульный лист (1873)"),
    ("02", 1, "Foreword, 1", "Vorwort, 1", "Предисловие, 1"),
    ("03", 1, "Foreword, 2", "Vorwort, 2", "Предисловие, 2"),
    ("04", 1, "Foreword, 3", "Vorwort, 3", "Предисловие, 3"),
    ("05", 1, "Foreword, 4", "Vorwort, 4", "Предисловие, 4"),
    ("06", 1, "English translation (F. Rau, 2018)", "Englische Übersetzung (F. Rau, 2018)", "Английский перевод (Ф. Рау, 2018)"),
]

# language -> (file suffix, output name, doc title, page-word, vol-word, label index, intro)
LANGS = {
    "de": (".md",    "grapref_all.de.md",
           "Wörterbuch zum Rig-Veda (Hermann Grassmann) — Vorspann, vollständig (Deutsch)",
           "Seite", "Band", 3,
           "OCR-Transkription des gesamten Vorspanns (Titelblatt, Vorwort) des *Wörterbuchs zum Rig-Veda* (Hermann Grassmann, Leipzig: F. A. Brockhaus, 1873), in der ursprünglichen Orthographie."),
    "en": (".en.md", "grapref_all.en.md",
           "Dictionary to the Rig-Veda (Hermann Grassmann) — Front Matter, complete (English)",
           "Page", "vol.", 2,
           "English rendering of the complete front matter (title page, foreword) of the *Wörterbuch zum Rig-Veda* (Hermann Grassmann, Leipzig: F. A. Brockhaus, 1873). Foreword translation courtesy of Dr. Felix Rau, University of Cologne, 2018."),
    "ru": (".ru.md", "grapref_all.ru.md",
           "Словарь к Ригведе (Герман Грассман) — предварительные материалы, полностью (русский)",
           "Страница", "том", 4,
           "Русский перевод всех предварительных материалов (титульный лист, предисловие) *Словаря к Ригведе* (Герман Грассман, Лейпциг: Ф. А. Брокгауз, 1873). Орфография дореформенная."),
}

TOC_WORD = {"de": "Inhalt", "en": "Contents", "ru": "Содержание"}
SRC_WORD = {"de": "Quelle (Scan)", "en": "Source (scan)", "ru": "Источник (скан)"}

def strip_page(text):
    """Remove the opening YAML block and the first H1 heading; return (meta, body)."""
    meta = {}
    lines = text.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            m = re.match(r"\s*([A-Za-z_]+):\s*(.*)$", lines[i])
            if m:
                meta[m.group(1)] = m.group(2).strip()
            i += 1
        i += 1  # skip closing ---
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith("# "):
        i += 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    body = "\n".join(lines[i:]).rstrip()
    return meta, body

def slug(s):
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s.strip())
    return s

for lang, (suf, outname, title, pageword, volword, labidx, intro) in LANGS.items():
    out = []
    out.append(f"# {title}\n")
    out.append(intro + "\n")
    out.append(f"Source index: [README.md](README.md). Per-page files: `graprefNN{suf}`.\n")
    out.append(f"## {TOC_WORD[lang]}\n")
    for nn, vol, *labels in PAGES:
        label = labels[labidx - 2]
        htext = f"{pageword} {nn} — {label}"
        out.append(f"- [{htext}](#{slug(htext)})")
    out.append("")
    for nn, vol, *labels in PAGES:
        label = labels[labidx - 2]
        src = os.path.join(HERE, f"grapref{nn}{suf}")
        if not os.path.exists(src):
            continue
        with open(src, encoding="utf-8") as f:
            meta, body = strip_page(f.read())
        htext = f"{pageword} {nn} — {label}"
        scan = meta.get("source_scan", "")
        url = meta.get("source_url", "")
        body = re.sub(r"(?m)^(#{1,5})(\s)", r"#\1\2", body)
        out.append("\n---\n")
        out.append(f"## {htext}\n")
        if url and scan and "none" not in scan.lower():
            out.append(f"<sub>{SRC_WORD[lang]}: [{scan}]({url})</sub>\n")
        elif url:
            out.append(f"<sub>{SRC_WORD[lang]}: [{url}]({url})</sub>\n")
        out.append(body + "\n")
    with open(os.path.join(HERE, outname), "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip() + "\n")
    print(f"wrote {outname}")

print("done")
