# Higgsfield API model catalog

Authenticated snapshot: 2026-09-17. The live `GET /models` response contained 76 endpoints: 13 image outputs and 63 video outputs. Refresh the catalog before making a current-availability claim.

## Default routing

| Need | Default endpoint | Why |
|---|---|---|
| Text-to-video | `bytedance/seedance-2.5/text-to-video` | User-selected skill default, up to 30 seconds, native audio option |
| Image-to-video | `bytedance/seedance-2.5/image-to-video` | One start image with optional end image |
| Multi-reference video | `bytedance/seedance-2.5/reference-to-video` | Images, videos, or audio references |
| Video edit | `bytedance/seedance-2.5/video-edit` | Modify an existing clip |
| Video extension | `bytedance/seedance-2.5/video-extend` | Continue an existing clip |
| Text-to-image | `higgsfield-ai/soul/v2/standard` | Higgsfield’s documented API quickstart image route |
| Vector/design image | `recraft/v4.1/text-to-image` | Design and vector-specialized family |
| Image editing | `alibaba/qwen-image-3/edit` | Dedicated edit endpoint |
| Campaign image | `marketing-studio/image` | Marketing-specific generation or editing |

These are routing defaults, not universal quality rankings. Use an explicitly requested model when it supports the task.

## Image endpoints

| Model | Endpoint | Operations |
|---|---|---|
| Grok Imagine 2.0 | `xai/grok-imagine-image-2.0` | text-to-image, image edit |
| Ideogram 4.0 | `ideogram/v4.0` | text-to-image, image edit |
| Marketing Studio Image | `marketing-studio/image` | text-to-image, image edit |
| Qwen Image 3 | `alibaba/qwen-image-3/text-to-image` | text-to-image |
| Qwen Image 3 | `alibaba/qwen-image-3/edit` | image edit |
| Recraft V4.1 | `recraft/v4.1/text-to-image` | text-to-image |
| Recraft V4.1 Pro | `recraft/v4.1/pro/text-to-image` | text-to-image |
| Recraft V4.1 Utility | `recraft/v4.1/utility/text-to-image` | text-to-image |
| Recraft V4.1 Utility Pro | `recraft/v4.1/utility/pro/text-to-image` | text-to-image |
| Soul 2 | `higgsfield-ai/soul/v2/standard` | text-to-image |
| Soul Standard | `higgsfield-ai/soul/standard` | text-to-image |
| Soul ID | `soul-id` | reusable character identity |
| Z-Image Turbo | `z-image/turbo` | text-to-image |

## Video endpoints

### ByteDance Seedance

- `bytedance/seedance-2.5/text-to-video`
- `bytedance/seedance-2.5/image-to-video`
- `bytedance/seedance-2.5/reference-to-video`
- `bytedance/seedance-2.5/video-edit`
- `bytedance/seedance-2.5/video-extend`
- `bytedance/seedance-2.0/text-to-video`
- `bytedance/seedance-2.0/image-to-video`
- `bytedance/seedance-2.0/reference-to-video`

### Kling

- `kling-video/v2.5-turbo/pro/text-to-video`
- `kling-video/v2.5-turbo/pro/image-to-video`
- `kling-video/v2.5-turbo/standard/image-to-video`
- `kling-video/v2.6/pro/text-to-video`
- `kling-video/v2.6/pro/image-to-video`
- `kling-video/motion-control/pro`
- `kling-video/motion-control/std`
- `kling-video/v3.0/std/text-to-video`
- `kling-video/v3.0/pro/text-to-video`
- `kling-video/v3.0/4k/text-to-video`
- `kling-video/v3.0/std/image-to-video`
- `kling-video/v3.0/pro/image-to-video`
- `kling-video/v3.0/4k/image-to-video`
- `kling-video/v3.0-turbo/text-to-video`
- `kling-video/v3.0-turbo/image-to-video`
- `kling-video/v3/motion-control/std`
- `kling-video/v3/motion-control/pro`
- `kling-video/o3/first-last-frame`
- `kling-video/o3/image-reference`
- `kling-video/o3/video-reference`
- `kling-video/o3/video-edit`
- `kling-video/omni/first-last-frame`
- `kling-video/omni/image-reference`
- `kling-video/omni/video-reference`
- `kling-video/omni/video-edit`

### Wan

- `wan/v2.6/text-to-video`
- `wan/v2.6/image-to-video`
- `wan/v2.6/reference-to-video`
- `wan/v2.7/text-to-video`
- `wan/v2.7/image-to-video`
- `wan/v2.7/reference-to-video`
- `alibaba/wan-3.0/text-to-video`
- `alibaba/wan-3.0/image-to-video`
- `alibaba/wan-3.0/reference-to-video`
- `alibaba/wan-3.0-prime/text-to-video`
- `alibaba/wan-3.0-prime/image-to-video`
- `alibaba/wan-3.0-prime/reference-to-video`

### LTX

- `lightricks/ltx-2.5/text-to-video/fast`
- `lightricks/ltx-2.5/image-to-video/fast`
- `lightricks/ltx-2.5/text-to-video/pro`
- `lightricks/ltx-2.5/image-to-video/pro`

### MiniMax

- `minimax/h3/text-to-video`
- `minimax/h3/image-to-video`
- `minimax/h3/reference-to-video`
- `minimax/hailuo-2.3/standard/text-to-video`
- `minimax/hailuo-2.3/standard/image-to-video`

### Other video families

- `xai/grok-imagine-video/v1.5/reference-to-video`
- `pixverse/v6/text-to-video`
- `pixverse/v6/image-to-video`
- `alibaba/happy-horse/text-to-video`
- `alibaba/happy-horse/image-to-video`
- `alibaba/happy-horse/reference-to-video`
- `alibaba/happy-horse/v1.1/text-to-video`
- `alibaba/happy-horse/v1.1/image-to-video`
- `alibaba/happy-horse/v1.1/reference-to-video`

## Catalog caveats

- The live catalog’s operation labels were imperfect on the verification date. Some Happy Horse text-to-video slugs were tagged `image2video`. Trust the model-specific page and submission schema over a broad catalog tag.
- Model names repeat across different modes and quality tiers. Use slugs, not display titles, in API calls.
- Pricing, discounts, duration bounds, resolutions, and parameter combinations can change independently of this snapshot.
- Never assume a parameter supported by one endpoint in a family works on another endpoint.

