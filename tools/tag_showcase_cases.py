#!/usr/bin/env python3
"""Assign semicolon-separated gallery tags to showcase-cases.csv."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN_FILES = [
    "film_tv_generation_plan.csv",
    "film_tv_generation_plan_wave2.csv",
    "film_tv_generation_plan_wave3.csv",
    "production_rerun_plan.csv",
]


def load_plans() -> dict[str, dict[str, str]]:
    plans: dict[str, dict[str, str]] = {}
    for name in PLAN_FILES:
        path = ROOT / "data" / name
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                plans[row["case_id"]] = row
    return plans


REGION_RULES = [
    ("Native American", "Native American"),
    ("Australian Aboriginal", "Australia"),
    ("African diaspora", "African diaspora"),
    ("Middle Eastern", "MENA"),
    ("Latin American", "Latin America"),
    ("Pacific island", "Pacific Islands"),
    ("South African", "South Africa"),
    ("Arab Gulf", "Gulf"),
    ("Hong Kong", "Hong Kong"),
    ("American", "USA"),
    ("Chinese", "China"),
    ("Japanese", "Japan"),
    ("Korean", "Korea"),
    ("British", "UK"),
    ("Indian", "India"),
    ("Turkish", "Turkey"),
    ("Nollywood", "Nigeria"),
    ("Bollywood", "India"),
    ("Thai", "Thailand"),
    ("Indonesian", "Indonesia"),
    ("Filipino", "Philippines"),
    ("Nordic", "Nordic"),
    ("French", "France"),
    ("German", "Germany"),
    ("Spanish", "Spain"),
    ("Brazilian", "Brazil"),
    ("Mexican", "Mexico"),
    ("Maori", "Aotearoa"),
    ("Māori", "Aotearoa"),
    ("Caribbean", "Caribbean"),
    ("Israeli", "Israel"),
    ("Egyptian", "Egypt"),
    ("Persian", "Persia"),
    ("Queer", "LGBTQ"),
    ("Children's", "Kids"),
    ("Polish", "Poland"),
    ("Italian", "Italy"),
    ("Greek", "Greece"),
    ("Portuguese", "Portugal"),
    ("Dutch", "Netherlands"),
    ("Sami", "Sami"),
    ("Sámi", "Sami"),
    ("Inuit", "Inuit"),
    ("Quebec", "Quebec"),
    ("Argentine", "Argentina"),
    ("Chile", "Chile"),
    ("Chilean", "Chile"),
    ("Peruvian", "Peru"),
    ("Colombian", "Colombia"),
    ("Cuban", "Cuba"),
    ("Jamaican", "Jamaica"),
    ("Vietnamese", "Vietnam"),
    ("Malaysian", "Malaysia"),
    ("Singapore", "Singapore"),
    ("Taiwan", "Taiwan"),
    ("Mongolian", "Mongolia"),
    ("Kazakh", "Kazakhstan"),
    ("Uzbek", "Uzbekistan"),
    ("Pakistani", "Pakistan"),
    ("Bangladeshi", "Bangladesh"),
    ("Ethiopian", "Ethiopia"),
    ("Moroccan", "Morocco"),
    ("Kenyan", "Kenya"),
    ("Roma family", "Roma"),
]

LANGUAGE_RULES = [
    ("Chinese title", "Chinese text"),
    ("Japanese title", "Japanese text"),
    ("Korean title", "Korean text"),
    ("Spanish title", "Spanish text"),
    ("Arabic title", "Arabic text"),
    ("Turkish title", "Turkish text"),
    ("Thai title", "Thai text"),
    ("Tagalog title", "Tagalog text"),
    ("Greek title", "Greek text"),
    ("French title", "French text"),
    ("Traditional Chinese title", "Traditional Chinese text"),
    ("Include exactly one English title", "English text"),
    ("Include exactly one Turkish title", "Turkish text"),
    ("Include exactly one Thai title", "Thai text"),
    ("Include exactly one Tagalog title", "Tagalog text"),
    ("Include exactly one Spanish title", "Spanish text"),
    ("Include exactly one Arabic title", "Arabic text"),
    ("Include exactly one Greek title", "Greek text"),
    ("Include exactly one French title", "French text"),
]

GENRE_RULES = [
    ("superhero", "Superhero"),
    ("crime", "Crime"),
    ("detective", "Crime"),
    ("thriller", "Thriller"),
    ("romance", "Romance"),
    ("romantic", "Romance"),
    ("family", "Family drama"),
    ("drama", "Drama"),
    ("comedy", "Comedy"),
    ("horror", "Horror"),
    ("sci-fi", "Sci-fi"),
    ("science", "Sci-fi"),
    ("fantasy", "Fantasy"),
    ("historical", "Historical"),
    ("period", "Period drama"),
    ("music", "Music"),
    ("musical", "Music"),
    ("dance", "Dance"),
    ("heist", "Heist"),
    ("legal", "Legal"),
    ("court", "Legal"),
    ("political", "Political"),
    ("documentary", "Docudrama"),
    ("docudrama", "Docudrama"),
    ("reality", "Reality TV"),
    ("cooking", "Reality TV"),
    ("competition", "Reality TV"),
    ("sports", "Sports"),
    ("pirate", "Adventure"),
    ("survival", "Survival"),
    ("post-apocalyptic", "Post-apocalyptic"),
    ("magical realism", "Magical realism"),
    ("noir", "Noir"),
    ("mystery", "Mystery"),
]

ASSET_RULES = [
    ("turnaround", "Character Design"),
    ("character production", "Character Design"),
    ("character design", "Character Design"),
    ("line art", "Line Art"),
    ("line-art", "Line Art"),
    ("lineup", "Character Lineup"),
    ("height chart", "Character Lineup"),
    ("storyboard", "Storyboard"),
    ("poster", "Poster & Key Art"),
    ("key art", "Poster & Key Art"),
    ("thumbnail", "Poster & Key Art"),
    ("still", "Production Still"),
    ("key frame", "Production Still"),
    ("production still", "Production Still"),
    ("prop", "Props"),
    ("object macro", "Props"),
    ("costume", "Costume Design"),
    ("texture sheet", "Costume Design"),
    ("material", "Costume Design"),
    ("board", "Production Board"),
    ("lighting", "Lighting Study"),
    ("vfx", "VFX"),
    ("concept plate", "VFX"),
    ("set extension", "Set Extension"),
    ("set design", "Set Design"),
    ("production design", "Set Design"),
    ("transparent", "Transparent Asset"),
    ("reference", "Reference-driven"),
]


def contains(haystack: str, needle: str) -> bool:
    escaped = re.escape(needle.strip().lower())
    return re.search(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", haystack) is not None


def add(tags: list[str], value: str) -> None:
    if value and value not in tags:
        tags.append(value)


def apply_rules(tags: list[str], haystack: str, rules: list[tuple[str, str]]) -> None:
    for needle, tag in rules:
        if contains(haystack, needle):
            add(tags, tag)


def film_tags(row: dict[str, str], plans: dict[str, dict[str, str]]) -> str:
    plan = plans.get(row["case_id"], {})
    subject = plan.get("subject") or row.get("subject", "")
    scene = plan.get("scene") or row.get("scene", "")
    prompt = plan.get("prompt") or row.get("prompt", "")
    notes = plan.get("notes", "")
    haystack = f"{subject} {scene} {prompt} {notes}".lower()
    tags = ["Film & TV"]
    apply_rules(tags, haystack, REGION_RULES)
    apply_rules(tags, haystack, GENRE_RULES)
    apply_rules(tags, haystack, ASSET_RULES)
    before_language = len(tags)
    apply_rules(tags, haystack, LANGUAGE_RULES)
    if len(tags) > before_language:
        add(tags, "Multilingual text test")
    if any(phrase in haystack for phrase in ("no readable text", "no text", "blank", "blank signs", "blank panels")):
        add(tags, "No-text production asset")
    if any(word in haystack for word in ("diverse", "multicultural", "multiethnic", "multiracial")):
        add(tags, "Diverse casting")
    if any(word in f"{subject} {prompt}" for word in ("Indigenous", "Sámi", "Māori", "Aboriginal", "Inuit", "Native American")):
        add(tags, "Indigenous representation")
    return "; ".join(tags)


def basic_tags(row: dict[str, str]) -> str:
    tags: list[str] = []
    for key in ("industry", "subject", "collection"):
        add(tags, row.get(key, ""))
    prompt = row.get("prompt", "").lower()
    scene = row.get("scene", "").lower()
    if row.get("reference_image") or row.get("reference_url"):
        add(tags, "Reference-driven")
    if "no text" in prompt or "blank" in prompt:
        add(tags, "No-text production asset")
    if "poster" in scene or "banner" in scene:
        add(tags, "Poster & Key Art")
    if row.get("subject") in {"Mathematics", "Physics", "Biology", "Chemistry", "Engineering"}:
        add(tags, "STEM")
    return "; ".join(tags)


def main() -> int:
    plans = load_plans()
    csv_path = ROOT / "data" / "showcase-cases.csv"
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    fields = list(rows[0].keys())
    if "tags" not in fields:
        fields.append("tags")
    for row in rows:
        row["tags"] = film_tags(row, plans) if row.get("industry") == "Film & TV" else basic_tags(row)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"tagged {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
