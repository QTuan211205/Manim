# Important Notes

## Required Working Habit

- Read this file before making or rendering scene changes.
- Update this file whenever a new problem, cause, fix, verification rule, or recurring user requirement is discovered.
- Treat audio completeness as a hard requirement: every audio file that belongs to a scene must be scheduled and must survive the final render.
- Only do the exact changes the user requests. Do not make extra scene, audio, layout, or style edits without being asked.
- Always ask carefully before acting when the request is unclear. If any requirement, target scene/time, asset, or expected visual result is ambiguous, ask the user for clarification before editing or rendering.

## User Style Preferences

- Keep visuals simple. Avoid adding explanatory text, decorative headers, or extra scenes unless explicitly requested.
- Use colors consistently across a scene. Prefer a restrained, continuous palette over many accent colors.
- When the user asks for slide-based visuals, use actual images/crops from the provided slide PDF instead of recreating charts or diagrams manually.
- Source text should appear below slide-derived images when requested.
- Audio timing should follow visual meaning: keep the screen blank or neutral until the narration reaches the relevant concept, then show the matching visual cue.
- For title/box beats, hold the visual long enough to be read; do not transition immediately after it appears.

## Manim Audio Rendering

- For audio or timing changes, render with cache disabled and flushed:
  `manim -ql --flush_cache --disable_caching scene_1_1.py Scene1_1`.
- Normal cached renders can reuse stale partial movie files and produce a final MP4 with missing or shifted audio, even when the scene code calls `add_sound`.
- Verify audio timing after render with `ffmpeg` silence detection. For example, the first Scene 1.1 voiceover should now begin around 3 seconds.
- Do not trust a successful Manim render alone for audio correctness. Also check scene code for expected voiceover files, validate that every expected file exists, and use render/audio probes when timing changes are involved.
- When concatenating rendered scenes, do not use plain concat if a scene's audio stream is shorter than its video stream. Pad each scene's audio to that scene's video duration before concatenating, otherwise later scene audio can shift earlier or the combined output can be too short.

## Chapter 1 Voiceovers

- Chapter 1 scenes must use every matching sentence-level file in `voiceover/generated_sentence_level`.
- Scene 1.1 uses `sc11_001.mp3` through `sc11_007.mp3`.
- Scene 1.2 uses `sc12_001.mp3` through `sc12_008.mp3`.
- Scene 1.3 uses `sc13_001.mp3` through `sc13_011.mp3`.
- Scene 1.4 uses `sc14_001.mp3` through `sc14_008.mp3`.
- The scenes should validate expected voiceover files and track scheduled voiceovers. If a future edit skips one, the render should fail instead of silently producing a bad video.
- Do not use stale references to `voiceover/generated_unsorted`; that directory is absent in this workspace.

## Font And Spacing

- The project asks for `Segoe UI`, but this machine does not have it installed.
- A local Selawik font fallback is used because it is closer to Segoe UI metrics than the default Linux fallback. Font changes can shift Manim text bounding boxes and therefore alter spacing.
- Scenes 1.2, 1.3, and 1.4 currently request `Arial`, but this machine does not have Arial installed. Manim falls back and prints very large font warnings during render. This can also change text metrics and spacing, so visual checks are required after edits to those scenes.
- Layout changes involving text should be checked from rendered frames, not judged only from code.

## Visual Verification

- For layout edits, render the affected section or full scene, extract representative frames with `ffmpeg`, and inspect them.
- Use actual visual evidence for overlap/alignment fixes. Recent examples: the “How should we call, control...” question and the “Inference algorithms + LLM OS” diagram needed frame checks after code changes.
- If a partial render is used for inspection, remember it can overwrite the normal scene output path. Regenerate the full scene afterward.

## Text Language

- Scene display text and inline scene comments should stay in English unless the user explicitly requests another language.
- After language edits, scan scene files with a precise Vietnamese-character regex instead of broad Unicode ranges, because broad ranges also catch math symbols and proper names.

## Current Status

- Left off at Scene 2.1.
- Need to fix audio: the voiceovers have been migrated to the sentence-level audio files, but the animation and wait timings need to be adjusted to align correctly with the audio tracks.
