# Repository Guidelines

## Project Structure & Module Organization

This repository contains Manim Community Edition scenes for a five-chapter video on "Beyond Decoding: Meta-Generation Algorithms for Large Language Models." Source files live under `content/chapter<N>/scene_<N>.<M>/` and follow the pattern `scene_<N>_<M>.py` with a matching class such as `Scene3_1`. Generated render output appears in per-scene `media/` folders, typically under `content/chapter<N>/scene_<N>.<M>/media/videos/scene_<N>_<M>/<quality>/`; treat these as build artifacts unless a rendered sample is intentionally needed. Reference materials live in `slide/`, subtitles in `subtitle/`, shared images in `content/images/`, helper scripts in `scripts/`, and the full narration/script in `full_video_script.md`.

## Build, Test, and Development Commands

Install runtime tools before rendering:

```bash
pip install manim
```

Render from the scene directory. Use low quality for review and high quality for final output:

```bash
cd content/chapter3/scene_3.1
manim -pql scene_3_1.py Scene3_1
manim -pqh scene_3_1.py Scene3_1
```

For quick syntax checks, run:

```bash
python -m py_compile content/chapter3/scene_3.1/scene_3_1.py
```

## Coding Style & Naming Conventions

Use Python with Manim idioms already present in the scenes. Keep file names, folder names, and class names aligned: `content/chapter4/scene_4.2/scene_4_2.py` should define `Scene4_2`. Prefer clear helper functions for repeated text, shape, or animation setup within a scene file. Use 4-space indentation, descriptive local names, and concise comments only for timing, narration alignment, or non-obvious animation logic. Preserve the existing temp directory setup for Manim text and TeX caches:

```python
config.text_dir = os.path.join(tempfile.gettempdir(), "manim_text")
config.tex_dir = os.path.join(tempfile.gettempdir(), "manim_tex")
```

## Testing Guidelines

There is no formal test suite. Validate changes by rendering the affected scene with `-ql` from its `content/chapter<N>/scene_<N>.<M>/` directory and visually checking layout, timing, fonts, and Vietnamese text. For small helper or geometry checks, add focused test/demo scene files like `test_ground_line.py` in the relevant scene directory, then render them directly. Do not commit generated `__pycache__/`, `partial_movie_files/`, debug frames, or routine media output.

## Commit & Pull Request Guidelines

Current history uses short messages such as `update manim` and `update`; keep commits brief but more specific when possible, for example `update scene 4.2 timing` or `add chapter 5 outro visuals`. Pull requests should describe the changed scenes, list render commands used for verification, and include screenshots or video clips for visual changes. Link related script, subtitle, or slide updates when a scene depends on them.

## Security & Configuration Tips

Manim requires FFmpeg for video output and may need system fonts such as Segoe UI for Vietnamese text and math symbols. Avoid hard-coding machine-specific absolute paths; keep assets referenced relative to the scene or repository root.

## Personal References & Notes

Read `IMPORTANT.md` before making or rendering scene changes, especially for audio, timing, visual verification, font, and user preference requirements.
