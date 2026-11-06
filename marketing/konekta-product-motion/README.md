# Konekta — real-app product-motion film

45-second vertical launch film built around the approved phone rotation, UI zooms, floating cards, dark/white transitions and corrected two-person Krio soundtrack. Adds a 15-second music-led sequence of scrolling features, a real-photo mosaic and cards converging into Konekta before the closing spoken CTA.

## Render / edit

Requires Python 3.10+ and FFmpeg with libx264 on PATH.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python render-45.py --stills
python render-45.py
```

Final output: `output/konekta-product-motion-45sec.mp4`.
Cover: `output/konekta-45-cover.png`.
The 30-second alternate can be reproduced with `python render-final.py`.
To render the opening 7.8-second proof: `python render-preview.py`.

### Editable source
- `render-45.py`: final 45-second timeline, added feature/mosaic scenes and soundtrack edit.
- `render-final.py`: original 30-second timeline and shared animated feature scenes.
- `render-preview.py`: continuous phone reveal / UI push-in / marketplace card extraction.
- `real_assets.py`: official screenshot handling, device frame, cropped real product photos.
- `styleframes.py`: graphics, typography, perspective projection and original concept-frame utilities. Its original drawn UI is not used in the final film.
- `assets/official/`: the four official Google Play screenshots and their source URLs.
- `assets/fonts/`: Manrope / Inter with SIL Open Font License files.
- `audio/approved-soundtrack.m4a`: the approved two-speaker Krio mix, copied without re-encoding.
- `audio/instrumental.wav`: existing generated music used to extend the film. The 45-second master preserves the approved voice delivery and wording, inserts 15 seconds of music at 26 seconds and moves the closing CTA to 41.3 seconds. Music joins are smoothed within 50ms of the edit boundaries; the final longer mix is AAC-encoded, not bit-identical to the earlier film.

This is editable Python animation source, not an After Effects project or 3D scene file. Phones/cards use rigid perspective-projected planes with a modeled graphic frame.

## Authenticity and sources

Official app: https://play.google.com/store/apps/details?id=com.konekta.sl — Konekta, developer Mohamed Barry. Source URLs are in `assets/official/sources.json`.

Phone screens show the official marketplace, messages and wallet screenshots. The laptop, property, photographer and cable-tester photos are crops from the official marketplace screenshot. These are existing listing images, not invented products. Their live availability and prices are not independently verified.

Voice/video-call, voice-note, protection, ticket and AI cards are promotional feature graphics, not fabricated screenshots. No invented balances, transaction outcomes, testimonials or active call sessions were added. The official wallet screenshot remains unchanged.

Reference videos informed movement/composition only. No reference creator footage, audio, or Apple/Spotify/ChatGPT branding appears in the final film. No private voice recordings, extracted clone samples or credentials are included.

## QA

- 45.000 seconds; 1080×1920; 30fps; 1,350 frames; H.264/yuv420p; stereo AAC 48kHz.
- No voice regeneration or time-stretch. Final transcript confirms “land and house,” feature dialogue and closing Google Play CTA.
- Chrome decoded all 1,350 frames, zero dropped frames, no playback error.
- Integrated audio −17.21 LUFS; true peak −2.49 dBTP.
- Scene contact sheets inspected; payment terms appear below the phone for readability. Source product photos are repeated in the decorative mosaic; this is not a claim of distinct additional listings.