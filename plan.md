# Sentence-Level Voiceover Workflow Plan

## Goal

Regenerate narration as short sentence-level or visual-cue-level audio files, then attach each cue directly to the matching Manim visual change with `self.add_sound(...)`.

The current paragraph-level audio makes the narration feel like one continuous stream while the animation runs independently. The new workflow should make each sentence start near the visual beat it describes, with short breathing gaps between cues and longer pauses at section transitions.

## Core Decision

Use smaller audio cues instead of paragraph-sized files.

Old style:

```text
sc11_1.mp3
sc11_2.mp3
sc11_3.mp3
```

New style:

```text
sc11_001.mp3
sc11_002.mp3
sc11_003.mp3
...
```

Each generated file should contain one sentence. If a visual change happens in the middle of a long sentence, split that sentence into shorter natural phrases.

## Scope

Start with `scene_1_1` only.

Do not regenerate all chapters first. Use Scene 1 as the pilot:

1. Split `scene_1_1` narration into sentence/visual-cue text files.
2. Generate new sentence-level MP3 files.
3. Wire those files into `chapter1/scene_1.1/scene_1_1.py`.
4. Render low quality and check pacing.
5. Render high quality once approved.
6. Apply the same pattern to the remaining scenes.

Write new audio into:

```text
voiceover/generated_sentence_level/
```

The old paragraph-level text folders, old `voiceover/generated_unsorted/` audio, and old `voiceover/duration_manifest.json` have been removed. Keep the sentence-level folders and manifests as the active workflow.

## File Naming

Use zero-padded cue numbers so sorting stays correct:

```text
voiceover/scene_1_1_sentence/
  001.txt
  002.txt
  003.txt

voiceover/generated_sentence_level/
  sc11_001.mp3
  sc11_002.mp3
  sc11_003.mp3
```

Recommended naming pattern:

```text
scene_N_M cue text: voiceover/scene_N_M_sentence/NNN.txt
scene_N_M audio:    voiceover/generated_sentence_level/scNM_NNN.mp3
```

Examples:

```text
voiceover/scene_3_2_sentence/007.txt
voiceover/generated_sentence_level/sc32_007.mp3
```

## Cue Manifest

Create a source-of-truth manifest for sentence-level cues:

```text
voiceover/sentence_audio_manifest.json
```

Example shape:

```json
{
  "scene_1_1": [
    {
      "cue": "sc11_001",
      "text_file": "voiceover/scene_1_1_sentence/001.txt",
      "audio_file": "voiceover/generated_sentence_level/sc11_001.mp3",
      "text": "Sentence one goes here.",
      "anchor": "intro_title"
    },
    {
      "cue": "sc11_002",
      "text_file": "voiceover/scene_1_1_sentence/002.txt",
      "audio_file": "voiceover/generated_sentence_level/sc11_002.mp3",
      "text": "Sentence two goes here.",
      "anchor": "first_visual_change"
    }
  ]
}
```

The `anchor` field should describe the visual beat in the scene code. It does not need to be executable at first; it is mainly for reliable manual placement.

## Audio Duration Manifest

After generation, measure every MP3 with `ffprobe` and store real durations:

```text
voiceover/sentence_duration_manifest.json
```

Example:

```json
{
  "sc11_001.mp3": 4.21,
  "sc11_002.mp3": 3.87
}
```

These durations should drive Manim waits so cues do not overlap or get cut off.

## ElevenLabs Generation

Use ElevenLabs as the TTS generation path.

Suggested config file:

```text
voiceover/elevenlabs_config.json
```

Suggested starting config:

```json
{
  "voice_id": "UgBBYS2sOqTuMpoF3BR0",
  "model_id": "eleven_multilingual_v2",
  "output_format": "mp3_44100_128",
  "voice_settings": {
    "stability": 0.65,
    "similarity_boost": 0.8,
    "speed": 0.95,
    "style": 0,
    "use_speaker_boost": true
  }
}
```

Use an environment variable for the API key. Do not commit the key.

```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

The generation script should:

- Read `voiceover/sentence_audio_manifest.json`.
- Read config from `voiceover/elevenlabs_config.json`.
- Read `ELEVENLABS_API_KEY` from the environment.
- Generate one `.mp3` per sentence/visual cue.
- Write output to `voiceover/generated_sentence_level/`.
- Skip existing `.mp3` files by default.
- Support `--force` to regenerate existing audio.
- Support scene-level generation, for example `--scene scene_1_1`.
- Write to `.mp3.tmp` first, then rename to `.mp3` after a successful response.
- Retry 429 and 5xx responses with exponential backoff.
- Store generation metadata and measured durations after generation.

## Manim Integration Pattern

Use `self.add_sound(...)` directly in the scene, right before the visual block it narrates.

Helper pattern:

```python
from pathlib import Path

VOICEOVER_DIR = Path(__file__).resolve().parents[2] / "voiceover" / "generated_sentence_level"

def wait_for_voiceover(scene, voiceover_start, duration, padding=0.35):
    remaining = voiceover_start + duration + padding - scene.renderer.time
    if remaining > 0:
        scene.wait(remaining)
```

Cue placement pattern:

```python
voiceover_start = self.renderer.time
self.add_sound(str(VOICEOVER_DIR / "sc11_001.mp3"))

self.play(...)
wait_for_voiceover(self, voiceover_start, 4.21, padding=0.35)
```

Then repeat for the next visual beat:

```python
voiceover_start = self.renderer.time
self.add_sound(str(VOICEOVER_DIR / "sc11_002.mp3"))

self.play(...)
wait_for_voiceover(self, voiceover_start, 3.87, padding=0.35)
```

## Timing Rules

- Add each audio cue immediately before the visual change it describes.
- Default sentence padding: `0.25` to `0.5` seconds.
- Use longer waits, around `0.8` to `1.2` seconds, between major sections.
- If a block animation is shorter than the cue, wait with the current visual still visible.
- The visual must stay on screen until the corresponding audio cue finishes. This is especially important for final slides and section-ending visuals.
- Do not place the wait after a fadeout unless a black screen is intentional. For normal narration, wait first, then fade out.
- Do not shorten complex visual animations just to match audio; extend holds instead.
- Avoid scheduling many audio files at scene start, because that recreates the continuous-stream problem.

## Pilot Implementation Steps

1. Review `chapter1/scene_1.1/scene_1_1.py` and identify every meaningful visual beat.
2. Split the current `scene_1_1` narration into sentence/visual-cue text files.
3. Create `voiceover/sentence_audio_manifest.json` entries for `scene_1_1`.
4. Generate `sc11_001.mp3`, `sc11_002.mp3`, etc. into `voiceover/generated_sentence_level/`.
5. Measure the generated durations and write `voiceover/sentence_duration_manifest.json`.
6. Replace the existing paragraph-level audio placement in `scene_1_1.py` with sentence-level cues.
7. Render low quality:

```bash
cd chapter1/scene_1.1
/home/me/Projects/Manim/.venv/bin/manim -ql scene_1_1.py Scene1_1
```

8. Check that every sentence starts near the intended visual beat.
9. Adjust waits and padding.
10. Render high quality:

```bash
cd chapter1/scene_1.1
/home/me/Projects/Manim/.venv/bin/manim -qh scene_1_1.py Scene1_1
```

11. If normal video players do not play audio, create a compatible copy:

```bash
ffmpeg -y -i media/videos/scene_1_1/1080p60/Scene1_1.mp4 \
  -map 0:v:0 -map 0:a:0 \
  -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -movflags +faststart \
  media/videos/scene_1_1/1080p60/Scene1_1_compatible.mp4
```

## Validation

For each updated scene:

1. Run syntax check:

```bash
/home/me/Projects/Manim/.venv/bin/python -m py_compile chapter1/scene_1.1/scene_1_1.py
```

2. Render low quality.
3. Use `ffprobe` to confirm the output has both video and audio streams.
4. Confirm video duration is greater than or equal to audio duration.
5. Watch and listen for cue alignment.
6. Confirm final visuals stay on screen until the final sentence finishes.

Useful `ffprobe` check:

```bash
ffprobe -v error \
  -show_entries format=duration \
  -show_entries stream=codec_type,codec_name,duration \
  -of json \
  media/videos/scene_1_1/1080p60/Scene1_1_compatible.mp4
```

## Acceptance Criteria

For `scene_1_1` pilot:

- Audio is regenerated as sentence-level or visual-cue-level files.
- Each sentence starts near the related visual change.
- Narration does not continue over unrelated visuals.
- There is a short breathing pause between sentences where appropriate.
- Major sections have a clearer break.
- The final visual remains visible until the final sentence completes, then fades out after the audio is done.
- The high-quality MP4 plays audio in a normal video player.

For the full project:

- Apply the same sentence-level workflow scene by scene.
- Skip `scene_3_5` until a matching Manim scene exists.
- Keep generated media artifacts out of source changes unless a rendered sample is intentionally requested.

## Notes

- `scene_3_5` exists in `full_video_script.md` and the sentence voiceover manifest, but the corresponding Manim file is missing.
- The current environment uses `/home/me/Projects/Manim/.venv/bin/manim`; plain `manim` is not available in PATH here.
- The active audio workflow is sentence-level only: `voiceover/scene_*_sentence/`, `voiceover/sentence_audio_manifest.json`, and `voiceover/generated_sentence_level/`.
