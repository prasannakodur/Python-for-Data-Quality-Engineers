"""Record type definitions and formatting for the user-generated news feed tool.
Functional style: each factory returns a finalized string ready to append.

Types:
1. News: inputs -> text, city; publish time auto timestamp.
2. PrivateAd: inputs -> text, expiration date (YYYY-MM-DD); publish time auto, days left computed (0 if expired).
3. Recipe (unique type): inputs -> title, ingredients (comma-separated).
   Publish rule: we compute ingredient count, average ingredient name length, and assign a recipe complexity label:
       SIMPLE (<=4 ingredients), MODERATE (5-8), COMPLEX (>8).
   Timestamp added.

All records share a consistent block format separated by a line of dashes.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
from typing import List
import re

TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"
SEPARATOR = "\n" + ("-" * 40) + "\n"

# ---------------- Utilities ---------------- #

def _now() -> datetime:
    return datetime.now()

def _parse_date(raw: str) -> date:
    return datetime.strptime(raw.strip(), "%Y-%m-%d").date()

def _days_left(expiration: date) -> int:
    today = date.today()
    return max((expiration - today).days, 0)

# ---------------- News ---------------- #

@dataclass(frozen=True)
class News:
    text: str
    city: str
    published: datetime

    def format(self) -> str:
        return (
            f"NEWS: {self.text.strip()}\n"
            f"City: {self.city.strip()}\n"
            f"Published: {self.published.strftime(TIMESTAMP_FMT)}"
        )

# ---------------- Private Ad ---------------- #

@dataclass(frozen=True)
class PrivateAd:
    text: str
    expiration: date
    published: datetime

    def format(self) -> str:
        days = _days_left(self.expiration)
        status = "EXPIRED" if days == 0 and date.today() > self.expiration else f"Days left: {days}"
        return (
            f"PRIVATE AD: {self.text.strip()}\n"
            f"Expires: {self.expiration.isoformat()} ({status})\n"
            f"Published: {self.published.strftime(TIMESTAMP_FMT)}"
        )

# ---------------- Recipe (Unique) ---------------- #

@dataclass(frozen=True)
class Recipe:
    title: str
    ingredients: List[str]
    published: datetime

    def format(self) -> str:
        clean = [ing.strip() for ing in self.ingredients if ing.strip()]
        count = len(clean)
        avg_len = (sum(len(i) for i in clean) / count) if count else 0
        if count <= 4:
            complexity = "SIMPLE"
        elif count <= 8:
            complexity = "MODERATE"
        else:
            complexity = "COMPLEX"
        return (
            f"RECIPE: {self.title.strip()}\n"
            f"Ingredients ({count}): {', '.join(clean)}\n"
            f"Avg name length: {avg_len:.1f} | Complexity: {complexity}\n"
            f"Published: {self.published.strftime(TIMESTAMP_FMT)}"
        )

# ---------------- Factories ---------------- #

def create_news(text: str, city: str) -> str:
    return News(text=text, city=city, published=_now()).format() + SEPARATOR

def create_private_ad(text: str, expiration_raw: str) -> str:
    exp = _parse_date(expiration_raw)
    return PrivateAd(text=text, expiration=exp, published=_now()).format() + SEPARATOR

def create_recipe(title: str, ingredients_raw: str) -> str:
    ingredients = re.split(r",|;", ingredients_raw)
    return Recipe(title=title, ingredients=ingredients, published=_now()).format() + SEPARATOR

TYPE_MAP = {
    "1": ("News", create_news, ["News text", "City"]),
    "2": ("Private Ad", create_private_ad, ["Advertisement text", "Expiration date (YYYY-MM-DD)"]),
    "3": ("Recipe", create_recipe, ["Recipe title", "Ingredients (comma or semicolon separated)"]),
}

__all__ = [
    "create_news",
    "create_private_ad",
    "create_recipe",
    "TYPE_MAP",
]
