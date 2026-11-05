 # Konekta — 30-second launch film

Final film: `../../packages/web/public/videos/konekta-launch-30sec.mp4` when this package is in `marketing/konekta-launch/`.
Cover: `../../packages/web/public/images/konekta-launch-cover.png`.

## Editable source

`render.py` is the animation source: seven Pillow-rendered scenes, editable typography, timing, colors, photo pans, masked reveals, waveforms, icon animation and transitions. It is not an After Effects project. All source images, fonts, dialogue and music needed to reproduce the film are included.

Requirements: Python 3.10+ and FFmpeg (with libx264) available on PATH.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python render.py --preview
python render.py
```

Outputs are written to `output/`. Final output is 30 seconds, 1080×1920, 30 fps, H.264/yuv420p with stereo AAC at 48 kHz. `output/audio-edit.json` records the dialogue timing edits. Dialogue and ducked music are mastered with NumPy/SciPy; FFmpeg encodes and muxes the result.

## Timeline

| Seconds | Scene |
| --- | --- |
| 0–3 | Sierra Leone, let's connect |
| 3–7.8 | Buying, selling, services, land and homes |
| 7.8–13.6 | Voice/video calls, voice notes and private chat |
| 13.6–17 | Payments and Konekta Protection / escrow |
| 17–22 | Business catalogs and customer connections |
| 22–26 | Services, properties, tickets and Konekta AI |
| 26–30 | Connect with Konekta / Google Play / konekta.website |

## Assets and provenance

- Logo, app preview and shop scene: approved Konekta website assets supplied through the existing project.
- Business and service scenes: generated illustrative Sierra Leone scenes using OpenAI image generation; they are not customer testimonials or documentary footage. There is no on-image generated-imagery label.
- Manrope and Inter fonts: bundled website fonts, distributed under the SIL Open Font License. See the included font licenses.
- Dialogue: generated together using the user-approved saved voices `Konekta Krio A` and `Konekta Krio B`. First-speaker wording explicitly says “house.” See `dialogue.txt`.
- Instrumental bed: generated for this film, with no vocals.

Personal source recordings, extracted clone samples, credentials and private transcripts are deliberately excluded. Regenerating speech requires access to the saved voices; rendering the included audio does not.

## Verification

Final mux: exactly 30.000 seconds / 900 frames; 1080×1920; 30 fps; stereo 48 kHz AAC. Measured audio: −15.73 LUFS integrated, −2.51 dB true peak. Final transcription confirms the feature dialogue, “land and house,” and Google Play CTA. Automated transcription is not a guarantee of native pronunciation.