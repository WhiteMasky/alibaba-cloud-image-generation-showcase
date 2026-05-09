# Advertising and E-commerce Batch Review

## Scope

- 14 advertising and ecommerce prompts.
- 2 models tested: Wan2.7-Image and Qwen-Image-2.0-Pro.
- 28 generated images total.
- Main language: English.
- Multilingual auxiliary tests: Japanese, French, Spanish, Arabic, Chinese.
- Added real reference images for selected cases. In the website detail dialog, these cases show a side-by-side comparison: reference image on the left and generated result on the right.

## Prompt and Reference Sources

| Source | What It Informed |
|---|---|
| https://www.media.io/ai-prompts/ai-product-photography-photo-prompts.html | White-background product hero, skincare, luxury product photography structure. |
| https://nanoads.ai/prompts/image | Ad-ready product photography, floating product, lifestyle and app campaign compositions. |
| https://randomprompts.org/ai-product-photography-prompt | Prompt structure: product, background, lighting, angle, commercial use case. |
| https://promptitin.com/prompts/product-photography | Surface, lighting, camera angle, material and mood fields. |
| https://p20v.com/blog/prompt-engineering-cheat-sheet-ecommerce-product-photos | Marketplace listing and ecommerce carousel direction. |
| https://unsplash.com/photos/a-brown-paper-bag-full-of-coffee-beans--fHykZfnjJA | Real coffee bag and beans product photography reference. |
| https://www.pexels.com/search/shoes%20product/ | Real footwear product photography reference. |

## Overall Findings

| Area | Wan2.7-Image | Qwen-Image-2.0-Pro |
|---|---|---|
| Product realism | Strong. Serum, headphones, shoe, coffee, air purifier, watch are commercially usable as concept visuals. | Strong. Often cleaner and more realistic in product shape and lighting. |
| Ecommerce catalog scenes | Good, especially MKT-06 bottle carousel and MKT-04 coffee. | Good, often cleaner and less illustrative. |
| Lifestyle scenes | Good, warm and polished. | Good, more realistic in several cases. |
| English no-text ad scenes | Best use case. Both models perform well when text is left for post-production. | Best use case. Strong for product-only visuals. |
| Multilingual text | Mixed. Japanese, French, and Chinese were usable or near-usable; Spanish and Arabic had errors. | Mixed. Japanese and Chinese were stronger; French, Spanish, Arabic, and unwanted text in MKT-14 were problematic. |

## Notable Results

| Case | Review |
|---|---|
| MKT-01 Premium serum hero | Both models created strong commercial skincare shots with blank labels. Good production direction. |
| MKT-02 Wireless headphones launch ad | Both models produced polished premium tech visuals. Suitable for hero banner experiments. |
| MKT-03 Running shoe action banner | Both models captured dynamic retail energy. Wan has stronger motion graphic feel; Qwen looks cleaner and more realistic. |
| MKT-04 Artisanal coffee product page | Both models are strong; Qwen is especially realistic and clean. |
| MKT-06 Product comparison carousel | Both models followed catalog structure well and kept blank label zones. |
| MKT-08 App campaign key visual | Qwen kept the no-text instruction better. Wan added unwanted English text and a typo. |
| MKT-09 Japanese skincare poster | Both models rendered Japanese headline well enough for a first-pass test. Still needs proofreading before publication. |
| MKT-10 French fragrance poster | Wan rendered the French headline cleanly. Qwen put text on the bottle and did not preserve the exact requested phrase. |
| MKT-11 Spanish sneaker sale banner | Both models failed exact Spanish rendering. Wan wrote a near phrase with typo; Qwen produced corrupted Spanish. |
| MKT-12 Arabic electronics campaign | Both models failed exact Arabic rendering. Use blank layout and add Arabic text later. |
| MKT-13 Chinese home appliance poster | Both models handled Chinese headline relatively well. |
| MKT-14 UGC lifestyle ad frame | Wan followed the no-text instruction better. Qwen added unwanted nonsensical bottom text. |

## Production Recommendation

For advertising and ecommerce, use the image model for:

1. Product lighting and scene composition.
2. Lifestyle staging.
3. Catalog layout and blank label areas.
4. Ad-safe negative space.

Add these later in Figma, Photoshop, code, or a design system:

1. Brand logos.
2. Product label artwork.
3. Prices, discount claims, and CTA copy.
4. Spanish, Arabic, French, and other exact multilingual campaign text.

Direct text rendering can be tested for Chinese, English, and short Japanese slogans, but every output should be proofread before publishing.
