# GitHub Pages Deployment

## Repository Name

Recommended:

```text
alibaba-image-generation-showcase
```

This gives you a clear public URL:

```text
https://YOUR_USERNAME.github.io/alibaba-image-generation-showcase/
```

## Deploy Steps

1. Create a new public repository on GitHub.
2. Upload every file in this folder to the repository root.
3. Go to `Settings` -> `Pages`.
4. Choose `Deploy from a branch`.
5. Select:
   - Branch: `main`
   - Folder: `/root`
6. Save and wait for GitHub to publish.

## Updating Later

To add another industry:

1. Add generated images to `assets/`.
2. Add rows to `data/showcase-cases.csv`.
3. Commit and push.

The filters and gallery update automatically from the CSV.
