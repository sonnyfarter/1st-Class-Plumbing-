#!/usr/bin/env python3
"""Pull exact Google reviews via the official Places API and bake them into index.html.

Usage:
    GOOGLE_MAPS_API_KEY=xxx python3 scripts/fetch_reviews.py [--dry-run]

Finds the business's place_id, fetches rating / total review count / the five
reviews Google returns, and replaces the review cards between the
<!-- REVIEWS:START --> and <!-- REVIEWS:END --> markers in index.html.
Google's API returns at most five reviews per place; that is a Google limit.
"""
import html
import json
import os
import sys
import urllib.parse
import urllib.request

BUSINESS_QUERY = "1st Class Plumbing & Gas LLC West Columbia SC"
INDEX = os.path.join(os.path.dirname(__file__), "..", "index.html")
START, END = "<!-- REVIEWS:START -->", "<!-- REVIEWS:END -->"


def api(path: str, **params) -> dict:
    params["key"] = os.environ["GOOGLE_MAPS_API_KEY"]
    url = f"https://maps.googleapis.com/maps/api/place/{path}/json?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    if data.get("status") not in ("OK", "ZERO_RESULTS"):
        sys.exit(f"Places API error: {data.get('status')} {data.get('error_message', '')}")
    return data


def card(review: dict) -> str:
    stars = "★" * int(review.get("rating", 5))
    text = html.escape(review.get("text", "").strip())
    author = html.escape(review.get("author_name", "Google user"))
    when = html.escape(review.get("relative_time_description", ""))
    return (
        '      <article class="rev">\n'
        f'        <span class="s">{stars}</span>\n'
        f'        <p>{text}"</p>\n'
        f'        <footer>{author} · Google review · {when}</footer>\n'
        "      </article>"
    )


def main() -> None:
    dry = "--dry-run" in sys.argv
    found = api("findplacefromtext", input=BUSINESS_QUERY, inputtype="textquery", fields="place_id,name")
    candidates = found.get("candidates") or sys.exit("Business not found on Google Places.")
    place_id = candidates[0]["place_id"]

    details = api(
        "details",
        place_id=place_id,
        reviews_no_translations="true",
        fields="name,rating,user_ratings_total,reviews,url",
    )["result"]

    reviews = [r for r in details.get("reviews", []) if r.get("rating", 0) >= 4 and r.get("text")]
    if not reviews:
        sys.exit("No usable reviews returned.")
    print(f"{details['name']}: {details.get('rating')}★ ({details.get('user_ratings_total')} reviews); "
          f"{len(reviews)} review texts fetched")

    block = f"{START}\n" + "\n".join(card(r) for r in reviews) + "\n    "
    src = open(INDEX, encoding="utf-8").read()
    pre, rest = src.split(START, 1)
    _, post = rest.split(END, 1)
    out = pre + block + END + post

    if dry:
        print(block)
        return
    open(INDEX, "w", encoding="utf-8").write(out)
    print("index.html updated. Review, commit, and redeploy.")


if __name__ == "__main__":
    main()
