# Production Image Audit

## Scope

- Reviewed every gallery row after the film and TV expansion.
- Starting gallery size before cleanup: 216 rows.
- Audit standard: production usefulness, realism within the requested environment, absence of obvious factual errors, and absence of release-blocking wrong text.
- Low-scoring images were rerun with production safer prompts. Most exact typography failures were changed to blank title/label areas for post-production overlay.

## Scoring Scale

- 5: Production-ready or near production-ready.
- 4: Usable for production ideation or layout, with normal art-direction review.
- 3: Useful as a concept but needs obvious manual cleanup.
- 2: Not production-ready because of objective errors, wrong text, or unwanted labels.
- 1: Delete.

## Rerun Actions

| Case | Model | Before | Action | After |
|---|---|---:|---|---:|
| MKT-08 | Wan2.7-Image | 2 | Removed unwanted fake campaign text by rerunning as a no-text app key visual. | 4 |
| MKT-12 | Qwen-Image-2.0-Pro | 2 | Replaced unreliable Arabic headline generation with a blank-title production visual. | 4 |
| MKT-12 | Wan2.7-Image | 2 | Replaced unreliable Arabic headline generation with a blank-title production visual. | 4 |
| MKT-14 | Qwen-Image-2.0-Pro | 2 | Removed nonsensical bottom text by rerunning as a no-text UGC frame. | 4 |
| FTV-05 | Wan2.7-Image | 2 | Replaced unstable Japanese title with blank title space. | 4 |
| FTV-11 | Qwen-Image-2.0-Pro | 2 | Replaced unreliable Arabic title with blank title space. | 4 |
| FTV-11 | Wan2.7-Image | 2 | Replaced unreliable Arabic title with blank title space. | 4 |
| FTV-15 | Wan2.7-Image | 2 | Replaced misspelled Turkish title with blank title space. | 4 |
| FTV-18 | Qwen-Image-2.0-Pro | 3 | Replaced uncertain Thai title rendering with blank title space. | 4 |
| FTV-18 | Wan2.7-Image | 3 | Replaced uncertain Thai title rendering with blank title space. | 4 |
| FTV-26 | Wan2.7-Image | 2 | Replaced misspelled Spanish title with blank title space. | 4 |
| FTV-31 | Wan2.7-Image | 2 | Replaced unreliable Arabic title with blank title space. | 4 |
| STEM-08 | Qwen-Image-2.0-Pro | 2 | Replaced misspelled biology labels with blank callout boxes for post-labeling. | 4 |
| STEM-08 | Wan2.7-Image | 2 | Replaced misspelled biology labels with blank callout boxes for post-labeling. | 4 |
| STEM-09 | Qwen-Image-2.0-Pro | 2 | Replaced unreliable DNA labels with blank callout boxes for post-labeling. | 4 |
| STEM-09 | Wan2.7-Image | 2 | Replaced unreliable DNA labels with blank callout boxes for post-labeling. | 4 |

## Deleted Images

| Case | Model | Reason |
|---|---|---|
| FTV-29 | Wan2.7-Image | Repeatedly added unwanted English labels to a concept sheet after no-text reruns. |
| FTV-60 | Wan2.7-Image | Repeatedly added unwanted labels to a costume/material sheet after no-text reruns. |

## Outcome

- Final gallery size: 214 rows.
- Deleted assets are removed from the local repository and no longer referenced by the gallery data.
- All retained low-score cases were changed to production-safe no-text or blank-label versions.
- The production rule going forward is to treat exact titles, subtitles, STEM labels, legal copy, logos, and multilingual typography as a separate design/compositing layer unless the model output is explicitly proofread.
