#!/usr/bin/env python3
"""Rerender selected showcase cases in place with Alibaba Cloud image models."""

from __future__ import annotations

import argparse
import csv
import os
import time
from pathlib import Path

from PIL import Image, ImageOps

from generate_showcase_cases import DEFAULT_ENDPOINT, DEFAULT_MODELS, download, extract_image_urls, make_payload, model_slug, post_json, read_csv, write_gallery_csv


ROOT = Path(__file__).resolve().parents[1]
CSV_FIELDS = [
    "collection",
    "industry",
    "case_id",
    "subject",
    "scene",
    "model",
    "status",
    "image",
    "prompt",
    "reference_image",
    "reference_url",
    "tags",
]


def update_thumb(image_path: Path) -> None:
    thumb_dir = ROOT / "assets" / "thumbs"
    thumb_dir.mkdir(exist_ok=True)
    with Image.open(image_path) as image:
        thumb = ImageOps.exif_transpose(image).convert("RGB")
        thumb.thumbnail((640, 640), Image.Resampling.LANCZOS)
        thumb.save(thumb_dir / f"{image_path.stem}.webp", "WEBP", quality=76, method=6)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--gallery", default="data/showcase-cases.csv")
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument("--api-key", default=os.getenv("DASHSCOPE_API_KEY"))
    parser.add_argument("--endpoint", default=os.getenv("DASHSCOPE_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--only-case", action="append", default=[])
    parser.add_argument("--sleep", type=float, default=31.0)
    parser.add_argument("--timeout", type=int, default=420)
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Missing DASHSCOPE_API_KEY")

    plans = read_csv(ROOT / args.plan)
    gallery_path = ROOT / args.gallery
    gallery = read_csv(gallery_path)
    by_key = {(row["case_id"], row["model"]): row for row in gallery}
    only = set(args.only_case)
    models = [model.strip() for model in args.models.split(",") if model.strip()]

    for plan in plans:
        if only and plan["case_id"] not in only:
            continue
        for model in models:
            key = (plan["case_id"], model)
            if key not in by_key:
                print(f"skip missing gallery row {plan['case_id']} {model}")
                continue
            print(f"rerendering {plan['case_id']} with {model}")
            payload = make_payload(model, plan, 1)
            response = post_json(args.endpoint, args.api_key, payload, args.timeout)
            image_url = extract_image_urls(response)[0]
            image_path = ROOT / "assets" / f"{model_slug(model)}_{plan['case_id']}.png"
            download(image_url, image_path, args.timeout)
            update_thumb(image_path)

            row = by_key[key]
            row.update(
                {
                    "collection": plan["collection"],
                    "industry": plan["industry"],
                    "subject": plan["subject"],
                    "scene": plan["scene"],
                    "status": "ok",
                    "image": image_path.relative_to(ROOT).as_posix(),
                    "prompt": plan["prompt"],
                    "reference_image": plan.get("reference_image", ""),
                    "reference_url": plan.get("source_url", "") or plan.get("reference_url", ""),
                    "tags": plan.get("tags", row.get("tags", "")),
                }
            )
            write_gallery_csv(gallery_path, gallery)
            time.sleep(args.sleep)

    write_gallery_csv(gallery_path, gallery)
    print(f"updated {gallery_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
