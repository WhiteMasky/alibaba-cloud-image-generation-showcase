# Alibaba Cloud Image Generation Showcase

Static GitHub Pages site for presenting image generation case studies.

The current collection focuses on education scenarios, including STEM diagrams,
biology illustrations, textbook scenes, and multilingual dialogue examples.

## Structure

- `index.html`: site entry point
- `styles.css`: visual system and responsive layout
- `app.js`: gallery filters, CSV loading, and case detail dialog
- `assets/`: generated image files
- `data/showcase-cases.csv`: expandable case database
- `.nojekyll`: makes GitHub Pages serve files directly

## Add More Industries

Append rows to `data/showcase-cases.csv`.

Required columns:

```csv
collection,industry,case_id,subject,scene,model,status,image,prompt
```

Example:

```csv
Retail,Retail,RET-01,E-commerce,Product hero,qwen-image-2.0-pro,ok,assets/qwen-retail-product-hero.png,"Create a premium product hero image..."
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
