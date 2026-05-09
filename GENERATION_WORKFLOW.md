# Generation Workflow

This repo is meant to work as a repeatable showcase pipeline:

1. Research or write one industry prompt per row in `data/industry_generation_plan.csv`.
2. Generate the same case with `qwen-image-2.0-pro` and `wan2.7-image`.
3. Download the expiring result URLs into `assets/`.
4. Append both model results to `data/showcase-cases.csv`.
5. Regenerate `data/showcase-cases.js` so the gallery works on GitHub Pages and local `file://`.

## API Setup

Use an Alibaba Cloud Model Studio international API key:

```powershell
$env:DASHSCOPE_API_KEY = "sk-..."
```

The scripts use the Singapore endpoint by default:

```text
https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

## Dry Run

Preview payloads without calling the API:

```powershell
python tools/generate_showcase_cases.py --dry-run --only-case HC-01
```

## Generate Images

Generate one case with both target models:

```powershell
python tools/generate_showcase_cases.py --only-case HC-01
python tools/regenerate_showcase_cases_js.py
```

Generate all cases in the plan:

```powershell
python tools/generate_showcase_cases.py
python tools/regenerate_showcase_cases_js.py
```

The default delay is 31 seconds between model calls because the international
rate limit for `qwen-image-2.0-pro` is 2 calls per minute.

## Prompt Notes

- Keep exact logos, prices, legal claims, and multilingual copy outside the image whenever possible.
- Use blank text zones for production-safe post-processing.
- For Qwen, `negative_prompt` is passed through.
- For Wan2.7, `thinking_mode` is enabled by default.
