# Alibaba Cloud Image Generation Showcase

Static GitHub Pages site for presenting image generation case studies.

The current collections include education scenarios and advertising/e-commerce
scenarios. They cover STEM diagrams, textbook scenes, product photography,
campaign banners, marketplace catalog layouts, and multilingual ad text tests.

## Structure

- `index.html`: site entry point
- `styles.css`: visual system and responsive layout
- `app.js`: gallery filters, CSV loading, and case detail dialog
- `data/showcase-cases.js`: browser-safe data file used by the site, including when opened locally with `file://`
- `assets/`: generated image files
- `data/showcase-cases.csv`: expandable case database
- `.nojekyll`: makes GitHub Pages serve files directly

## Add More Industries

Append rows to `data/showcase-cases.csv`.
After editing the CSV, regenerate `data/showcase-cases.js` from the same rows
before publishing. The JS file lets the site work both on GitHub Pages and when
opened directly from a local folder.

Required columns:

```csv
collection,industry,case_id,subject,scene,model,status,image,prompt
```

Optional columns:

```csv
reference_image,reference_url
```

When `reference_image` is present, the case detail dialog shows a side-by-side
comparison: reference image on the left and generated result on the right.

Example:

```csv
Retail,Retail,RET-01,E-commerce,Product hero,qwen-image-2.0-pro,ok,assets/qwen-retail-product-hero.png,"Create a premium product hero image...",assets/reference/ret-01.jpg,https://example.com/reference-source
```

Place the referenced image in `assets/`.

## Deploy to GitHub Pages

1. Create a public GitHub repository.
2. Upload all files from this folder to the repository root.
3. Open `Settings` -> `Pages`.
4. Set source to `Deploy from a branch`.
5. Select branch `main` and folder `/root`.

The site will publish at:

```text
https://YOUR_USERNAME.github.io/YOUR_REPOSITORY_NAME/
```
