#!/usr/bin/env python3
"""Generate Alibaba Cloud image-model cases and append them to the gallery data.

The script reads a plan CSV, calls Alibaba Cloud Model Studio through the
international DashScope endpoint, downloads expiring image URLs immediately,
and appends rows to data/showcase-cases.csv.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENDPOINT = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
DEFAULT_MODELS = ("qwen-image-2.0-pro", "wan2.7-image")
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_gallery_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def make_payload(model: str, plan: dict[str, str], n: int) -> dict:
    parameters: dict[str, object] = {
        "n": n,
        "watermark": False,
    }

    size = plan.get("size", "").strip()
    if model.startswith("qwen-image"):
        parameters["size"] = size or "2048*2048"
        parameters["prompt_extend"] = plan.get("prompt_extend", "true").lower() != "false"
        negative_prompt = plan.get("negative_prompt", "").strip()
        if negative_prompt:
            parameters["negative_prompt"] = negative_prompt
    else:
        parameters["size"] = size or "2K"
        parameters["thinking_mode"] = plan.get("thinking_mode", "true").lower() != "false"

    content: list[dict[str, str]] = []
    reference_url = (plan.get("model_reference_url", "") or plan.get("reference_url", "")).strip()
    if reference_url:
        content.append({"image": reference_url})
    content.append({"text": plan["prompt"].strip()})

    return {
        "model": model,
        "input": {"messages": [{"role": "user", "content": content}]},
        "parameters": parameters,
    }


def post_json(endpoint: str, api_key: str, payload: dict, timeout: int) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code}: {body}") from error


def extract_image_urls(response: dict) -> list[str]:
    if response.get("code"):
        raise RuntimeError(f"{response.get('code')}: {response.get('message')}")

    urls: list[str] = []
    choices = response.get("output", {}).get("choices", [])
    for choice in choices:
        content = choice.get("message", {}).get("content", [])
        for item in content:
            image_url = item.get("image")
            if image_url:
                urls.append(image_url)
    if not urls:
        raise RuntimeError(f"No image URLs in response: {json.dumps(response, ensure_ascii=False)[:800]}")
    return urls


def download(url: str, path: Path, timeout: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "showcase-generator/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        path.write_bytes(response.read())


def model_slug(model: str) -> str:
    return model.replace("/", "-").replace("_", "-")


def next_variant_path(case_id: str, model: str, index: int) -> Path:
    suffix = f"-{index + 1}" if index else ""
    return ROOT / "assets" / f"{model_slug(model)}_{case_id}{suffix}.png"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default="data/industry_generation_plan.csv")
    parser.add_argument("--gallery", default="data/showcase-cases.csv")
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument("--endpoint", default=os.getenv("DASHSCOPE_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--api-key", default=os.getenv("DASHSCOPE_API_KEY"))
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--only-case", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--sleep", type=float, default=31.0, help="Delay between model calls; qwen-image-2.0-pro is 2/min.")
    parser.add_argument("--write-each", action="store_true", help="Persist CSV after every successful image download.")
    args = parser.parse_args()

    plan_path = ROOT / args.plan
    gallery_path = ROOT / args.gallery
    plan_rows = read_csv(plan_path)
    gallery_rows = read_csv(gallery_path)
    existing = {(row["case_id"], row["model"]) for row in gallery_rows}
    models = [item.strip() for item in args.models.split(",") if item.strip()]
    only_cases = set(args.only_case)

    if not args.api_key and not args.dry_run:
        print("Missing DASHSCOPE_API_KEY. Set it first or run with --dry-run.", file=sys.stderr)
        return 2

    appended: list[dict[str, str]] = []
    for plan in plan_rows:
        if only_cases and plan["case_id"] not in only_cases:
            continue
        for model in models:
            key = (plan["case_id"], model)
            if key in existing:
                print(f"skip existing {plan['case_id']} {model}")
                continue

            payload = make_payload(model, plan, args.n)
            if args.dry_run:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                continue

            print(f"generating {plan['case_id']} with {model}")
            response = post_json(args.endpoint, args.api_key, payload, args.timeout)
            image_urls = extract_image_urls(response)

            for index, image_url in enumerate(image_urls):
                case_id = plan["case_id"] if len(image_urls) == 1 else f"{plan['case_id']}-{index + 1}"
                image_path = next_variant_path(case_id, model, 0)
                download(image_url, image_path, args.timeout)
                rel_image = image_path.relative_to(ROOT).as_posix()
                row = {
                    "collection": plan["collection"],
                    "industry": plan["industry"],
                    "case_id": case_id,
                    "subject": plan["subject"],
                    "scene": plan["scene"],
                    "model": model,
                    "status": "ok",
                    "image": rel_image,
                    "prompt": plan["prompt"],
                    "reference_image": plan.get("reference_image", ""),
                    "reference_url": plan.get("source_url", "") or plan.get("reference_url", ""),
                    "tags": plan.get("tags", ""),
                }
                appended.append(row)
                if args.write_each:
                    gallery_rows.append(row)
                    write_gallery_csv(gallery_path, gallery_rows)
                print(f"saved {rel_image}")

            existing.add(key)
            time.sleep(args.sleep)

    if appended and not args.write_each:
        gallery_rows.extend(appended)
        write_gallery_csv(gallery_path, gallery_rows)
        print(f"appended {len(appended)} rows to {gallery_path.relative_to(ROOT)}")
    elif appended:
        print(f"appended {len(appended)} rows to {gallery_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
