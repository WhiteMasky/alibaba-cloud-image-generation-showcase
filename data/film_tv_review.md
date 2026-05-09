# Film & TV Batch Review

## Scope

- 14 production-oriented film and television prompts.
- 2 models tested: Qwen-Image-2.0-Pro and Wan2.7-Image.
- 28 accepted gallery images.
- Main prompt language: English.
- Auxiliary multilingual text tests: Chinese, Japanese, Korean, Spanish, Arabic.
- Production chain coverage: character sheets, expression/turnaround sheets, line art, cinematic stills, scene lighting, prop sheets, storyboards, vertical posters, relationship/key art.

## Prompt Strategy

The prompts use commercial production language instead of direct imitation of protected IP or named living-artist styles. For example, they test "American superhero comic character production sheet", "Japanese sports anime key visual", and "hand-painted fantasy prop sheet" rather than asking for exact Superman, Kuroko no Basket, or Studio Ghibli duplication.

The strongest production pattern is:

1. Use the image model for composition, camera language, casting diversity, costume, lighting, mood, object design, and blank text zones.
2. Keep exact titles, billing blocks, legal lines, logos, subtitles, prices, and multilingual copy as a post-production design layer.

## Overall Scores

Scores use a 1-5 scale.

| Area | Qwen-Image-2.0-Pro | Wan2.7-Image | Notes |
|---|---:|---:|---|
| Realistic live-action stills | 4.5 | 4.4 | Both produced strong drama, thriller, period, and sci-fi scenes. |
| Animation and comic design | 4.4 | 4.2 | Both are useful for character and prop exploration; Qwen was slightly cleaner on sheets. |
| Storyboard and board layout | 4.2 | 4.1 | Reruns reduced fake labels; Qwen kept cleaner board structure. |
| Poster/key art aesthetics | 4.4 | 4.2 | Both produced presentation-ready key art compositions. |
| Multilingual exact text | 3.6 | 2.8 | Chinese, Korean, and Spanish were usable or close; Japanese and Arabic remained risky, especially Wan. |
| Production readiness | 4.2 | 4.0 | Image composition is strong; exact typography still needs manual overlay for release use. |

## Case Notes

| Case | Qwen-Image-2.0-Pro | Wan2.7-Image | Decision |
|---|---|---|---|
| FTV-01 superhero turnaround | Strong sheet, clean expressions, no text after rerun. | Improved after rerun; clean enough for concept review. | Accepted both. |
| FTV-02 interrogation storyboard | Strong cinematic close-ups and lighting. | Good panel logic, slightly more graphic. | Accepted both. |
| FTV-03 Chinese costume poster | Strong Chinese title and poster mood. | Good poster composition and title. | Accepted both. |
| FTV-04 donghua line art | Clean xianxia production sheet. | Strong line-art sheet with useful pose/weapon details. | Accepted both. |
| FTV-05 Japanese sports anime | Strong action visual; title is close/usable for test review. | Rerun improved art, but Japanese title remains unreliable. | Accepted with text caveat. |
| FTV-06 Japanese live-action still | Excellent grounded rainy station drama still. | Strong realism and environment mood. | Accepted both. |
| FTV-07 Korean drama poster | Strong K-drama poster; Korean title is usable. | Good noir poster; Korean title is usable/near-usable. | Accepted both. |
| FTV-08 British period still | Strong ensemble blocking and period mood. | Good manor scene and candlelit atmosphere. | Accepted both. |
| FTV-09 Latin American telenovela | Strong family-poster composition and Spanish title. | Good melodrama poster and title. | Accepted both. |
| FTV-10 Afrofuturist drama still | Strong character and artifact focus. | Stronger environment scale and production design. | Accepted both. |
| FTV-11 Arabic historical poster | Good art direction; Arabic title is closer but still needs proofreading. | Arabic title remains unreliable after rerun. | Accepted with text caveat. |
| FTV-12 Indian thriller board | Strong board without fake text after rerun. | Strong thriller tiles without the prior title labels. | Accepted both. |
| FTV-13 fantasy prop sheet | Good isolated props, production-friendly. | Good isolated props, consistent style. | Accepted both. |
| FTV-14 heist storyboard | Strong continuity and panel variety after rerun. | Strong heist storyboard after rerun, no major text issue. | Accepted both. |

## Production Recommendation

Use these models directly for:

- Character ideation, wardrobe variants, expression sheets, and turnarounds.
- Live-action mood frames, lighting studies, and scene exploration.
- Prop sheets and art-department boards.
- Storyboard thumbnails and shot-planning boards.
- Poster/key-art composition before final typography.

Use a design tool, compositing pipeline, or code overlay for:

- Exact multilingual titles, especially Japanese kana and Arabic.
- Billing blocks, subtitles, captions, episode text, logos, and compliance copy.
- Any customer-facing final typography.

The final gallery keeps the multilingual outputs because they are useful model capability evidence, but the review flags which ones should not be treated as final release typography.
