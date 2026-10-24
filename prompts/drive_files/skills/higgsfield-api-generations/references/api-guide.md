# Higgsfield API guide

Verified against official Higgsfield documentation and live API behavior on 2026-09-17.

## Source priority

1. Live authenticated API responses for the student’s account.
2. The selected model’s API reference in Higgsfield Console.
3. Higgsfield shared API documentation.
4. This bundled snapshot.

The API catalog changes. A missing model in an old snapshot does not prove it is unavailable, and a listed model does not prove the current account can run it.

## Authentication

- Base URL: `https://api.higgsfield.ai`
- Header: `Authorization: Key KEY_ID:KEY_SECRET`
- New integrations should use the Authorization header, not legacy `hf-api-key` and `hf-secret` headers.
- Credentials must remain server-side.

## Discovery

The authenticated live catalog was available at:

```http
GET https://api.higgsfield.ai/models
Authorization: Key KEY_ID:KEY_SECRET
```

On 2026-09-17 it returned 76 endpoints. Treat this as observed live behavior. Higgsfield’s shared documentation directs developers to Console model pages as the authoritative source for model-specific schemas.

## Model-specific documentation

For a model slug such as `bytedance/seedance-2.5/text-to-video`, use:

```text
https://console.higgsfield.ai/models/bytedance%2Fseedance-2.5%2Ftext-to-video/api-reference
```

Confirm required fields, defaults, enums, duration limits, resolutions, audio behavior, and environment before submitting.

## Submit

Each model slug is also its generation path:

```http
POST https://api.higgsfield.ai/{model-slug}
Authorization: Key KEY_ID:KEY_SECRET
Content-Type: application/json
```

The initial response normally contains:

```json
{
  "status": "queued",
  "request_id": "...",
  "status_url": "https://api.higgsfield.ai/requests/.../status",
  "cancel_url": "https://api.higgsfield.ai/requests/.../cancel"
}
```

Store `request_id` and the returned URLs immediately.

## Estimate cost

Send the identical generation payload to:

```http
POST https://api.higgsfield.ai/estimate/{model-slug}
```

Many models return:

```json
{
  "credits": "1.500",
  "usd": "0.094"
}
```

Use authenticated `usd` as the authoritative successful-generation cost for that payload.

Some token-metered routes, including Seedance 2.5 at the verification date, returned only:

```json
{
  "type": "description",
  "pricing_description": "Token-metered pricing ... Rates shown are before any applicable customer discount."
}
```

That response does not expose the exact net discounted charge. Report the formula or list-cost calculation, label it correctly, and direct the student to Console Analytics for the final net charge. Never convert this into a falsely precise “exact charged” number.

## Seedance 2.5 defaults

Text-to-video slug:

```text
bytedance/seedance-2.5/text-to-video
```

Default payload:

```json
{
  "prompt": "...",
  "duration": 5,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "output_format": "mp4",
  "generate_audio": false
}
```

Documented text-to-video bounds on 2026-09-17:

- Duration: 4 to 30 seconds
- Resolution: 480p or 720p
- Aspect ratio: model-specific page must be checked live
- Output: MP4 or MOV
- Optional native audio

The estimate description documented this formula for 480p and 720p:

```text
video_tokens = ceil((input_video_seconds + generated_video_seconds) * width * height * 24 / 1024)
list_usd = video_tokens / 1000 * 0.0214
```

Image and audio references do not count as video input. Video references do. The formula is before applicable discounts.

Seedance 2.5 uses different media fields by route:

- Image-to-video: one `image_url`, optional `end_image_url`; the input image determines framing, so the documented schema does not include `aspect_ratio`.
- Reference-to-video: `image_urls`, `video_urls`, and `audio_urls` arrays; this route documents `aspect_ratio`.

## Polling

Poll the returned `status_url`.

Statuses:

| Status | Terminal | Meaning |
|---|---:|---|
| `queued` | No | Waiting and usually cancelable |
| `in_progress` | No | Generation started and cannot be canceled |
| `completed` | Yes | Output URL is present |
| `failed` | Yes | Generation failed |
| `nsfw` | Yes | Moderation rejected input or output |
| `canceled` | Yes | Canceled before processing |

Polling policy:

- Start at about two seconds.
- Increase gradually to ten seconds.
- Add jitter for concurrent workers.
- Retry transient GET/network/5xx failures with backoff.
- Stop on terminal status.
- Do not reconstruct URLs when the server already returned them.

## Charges and refunds

- Successful generations are charged.
- `failed` and `nsfw` requests are not charged. Reserved funds are refunded.
- A successfully canceled queued request is refunded.
- API billing uses a separate US-dollar balance from the normal higgsfield.ai subscription and plan credits.
- Funds expire one year after top-up.

## Media uploads

For a local image, audio file, or MP4, request a presigned URL:

```http
POST https://api.higgsfield.ai/files/generate-upload-url
Content-Type: application/json

{"content_type":"image/jpeg"}
```

The response includes `upload_url`, `public_url`, and `upload_headers`. PUT the bytes to `upload_url` with every returned header. Do not send Higgsfield API credentials to the storage URL. Pass `public_url` to the model.

Supported documented types:

- Images: JPEG, PNG, WebP, GIF
- Audio: WAV
- Video: MP4

## Output and retention

Completed responses can contain `images`, `video`, `audio`, or model-specific artifacts. Download them. Higgsfield guarantees availability for at least seven days and may remove them afterward.

## Error policy

| HTTP | Meaning | Action |
|---:|---|---|
| 400 | Invalid input or concurrency reached | Correct input or wait |
| 401 | Invalid credentials | Stop and fix credentials |
| 403 | Insufficient balance | Fund account |
| 404 | Request/model unavailable to account | Stop and verify |
| 422 | Schema validation failed | Correct payload |
| 423 | Model temporarily blocked | Retry later |
| 500 | Server failure | Retry safe GETs with backoff |
| 503 | Model disabled/not ready | Retry later or choose another model |

Do not automatically retry an ambiguous generation POST. The API does not currently accept an idempotency key. Record `X-Correlation-ID` and `request_id` for support.

## Official sources

- <https://docs.higgsfield.ai/docs/llms.txt>
- <https://docs.higgsfield.ai/docs/quickstart.md>
- <https://docs.higgsfield.ai/docs/authentication.md>
- <https://docs.higgsfield.ai/docs/concepts/requests.md>
- <https://docs.higgsfield.ai/docs/concepts/polling.md>
- <https://docs.higgsfield.ai/docs/concepts/file-uploads.md>
- <https://docs.higgsfield.ai/docs/concepts/errors.md>
- <https://docs.higgsfield.ai/docs/concepts/rate-limits.md>
- <https://docs.higgsfield.ai/docs/concepts/billing-and-retention.md>
- <https://docs.higgsfield.ai/docs/how-to/sdk.md>
- <https://github.com/higgsfield-ai/higgsfield-js>
- <https://github.com/higgsfield-ai/higgsfield-client>
