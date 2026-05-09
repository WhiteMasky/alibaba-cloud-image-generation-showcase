# Reference-driven Marketing Regeneration Review

## Scope

- Reworked all advertising/e-commerce cases that have reference images.
- Cases: MKT-01, MKT-02, MKT-03, MKT-04, MKT-07, MKT-09, MKT-11.
- Models: Wan2.7-Image and Qwen-Image-2.0-Pro.
- Final accepted outputs: 14 images.

## Method

1. Replaced weak reference images with more suitable real product photos where needed.
2. Used image-input generation/editing, not text-only generation.
3. Prompted the models to preserve product silhouette, material, color blocking, proportions, and recognizable appearance.
4. Reviewed the first pass for product fidelity and marketing visual quality.
5. Rejected and reran MKT-04 and MKT-09 after discovering unsuitable reference images.
6. Replaced the accepted outputs in the website assets and regenerated the site data file.

## Final Review

| Case | Wan2.7-Image | Qwen-Image-2.0-Pro | Decision |
|---|---|---|---|
| MKT-01 serum/dropper bottle | Preserves bottle silhouette and cap; polished skincare hero. | Preserves bottle and adds stronger botanical styling. | Accepted both. |
| MKT-02 headphones | Preserves over-ear form, removes cable for wireless ad direction. | Preserves over-ear form and cable structure more closely. | Accepted both. |
| MKT-03 running shoes | Preserves three-shoe reference and color blocking, good campaign energy. | Strong single-shoe campaign, preserves the main shoe appearance well. | Accepted both. |
| MKT-04 coffee bag | After rerun, preserves kraft bag concept and creates ecommerce product scene. | After rerun, preserves burlap coffee-sack look and improves realism. | Accepted both. |
| MKT-07 watch | Strong preservation of dial, strap, metal color, and luxury lighting. | Strong preservation of dial and gold/silver case styling. | Accepted both. |
| MKT-09 cream jar | After rerun, preserves open jar, lid, cream texture, and soft beauty mood. | After rerun, preserves jar/lid/cream and adds poster-like water styling. | Accepted both. |
| MKT-11 sneaker banner | Preserves three-shoe layout and color blocking. | Preserves shoes and creates cleaner retail banner. | Accepted both. |

## Production Notes

- These outputs are much stronger than the previous text-only generation because the models used product photos as visual inputs.
- The most reliable production approach is still to keep text, logo, price, CTA, and legal claims as a separate design layer.
- For customer-facing demos, the side-by-side dialog now clearly shows reference image vs generated result.
