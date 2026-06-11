from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "full_video_script.md"
OUTPUT_DIR = ROOT / "voiceover"

SCENE_HEADING_RE = re.compile(r"^### Scene (\d+)\.(\d+) - (.+)$")
TIME_RANGE_RE = re.compile(r"^\*\*Thời lượng:\*\*\s*(\d{2}):(\d{2})-(\d{2}):(\d{2})")


def scene_id(chapter: str, scene: str) -> str:
    return f"scene_{chapter}_{scene}"


def clean_quote_line(line: str) -> str:
    line = line.strip()
    if not line.startswith(">"):
        return ""
    return line[1:].strip()


def to_seconds(minutes: str, seconds: str) -> float:
    return int(minutes) * 60 + int(seconds)


def format_timestamp(seconds: float) -> str:
    minutes, secs = divmod(max(0, int(round(seconds))), 60)
    return f"{minutes:02d}:{secs:02d}"


def estimate_cues(
    paragraphs: list[str], scene_start: float | None, scene_end: float | None
) -> list[dict[str, object]]:
    if scene_start is None or scene_end is None or scene_end <= scene_start:
        return [
            {
                "index": index,
                "start": None,
                "end": None,
                "start_label": None,
                "end_label": None,
                "text": paragraph,
            }
            for index, paragraph in enumerate(paragraphs, start=1)
        ]

    weights = [max(1, len(paragraph)) for paragraph in paragraphs]
    total_weight = sum(weights)
    duration = scene_end - scene_start
    cursor = scene_start
    cues = []

    for index, (paragraph, weight) in enumerate(zip(paragraphs, weights), start=1):
        end = scene_end if index == len(paragraphs) else cursor + duration * weight / total_weight
        cues.append(
            {
                "index": index,
                "start": round(cursor, 2),
                "end": round(end, 2),
                "start_label": format_timestamp(cursor),
                "end_label": format_timestamp(end),
                "text": paragraph,
            }
        )
        cursor = end

    return cues


def extract_voiceovers(markdown: str) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    current_scene: str | None = None
    current_title: str | None = None
    current_start: float | None = None
    current_end: float | None = None
    in_voiceover = False
    paragraphs: list[str] = []
    current_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal current_lines
        text = " ".join(part.strip() for part in current_lines if part.strip())
        if text:
            paragraphs.append(text)
        current_lines = []

    def flush_scene() -> None:
        nonlocal paragraphs, current_scene, current_title, current_start, current_end, in_voiceover
        flush_paragraph()
        if current_scene and paragraphs:
            result[current_scene] = {
                "title": current_title or current_scene,
                "start": current_start,
                "end": current_end,
                "paragraphs": paragraphs,
            }
        paragraphs = []
        current_start = None
        current_end = None
        in_voiceover = False

    for raw_line in markdown.splitlines():
        heading = SCENE_HEADING_RE.match(raw_line)
        if heading:
            flush_scene()
            chapter, scene, title = heading.groups()
            current_scene = scene_id(chapter, scene)
            current_title = f"Scene {chapter}.{scene} - {title}"
            continue

        time_range = TIME_RANGE_RE.match(raw_line.strip())
        if current_scene and time_range:
            start_min, start_sec, end_min, end_sec = time_range.groups()
            current_start = to_seconds(start_min, start_sec)
            current_end = to_seconds(end_min, end_sec)
            continue

        if current_scene is None:
            continue

        if raw_line.strip() == "**Voiceover:**":
            in_voiceover = True
            continue

        if in_voiceover and raw_line.startswith("### Scene "):
            flush_scene()
            heading = SCENE_HEADING_RE.match(raw_line)
            if heading:
                chapter, scene, title = heading.groups()
                current_scene = scene_id(chapter, scene)
                current_title = f"Scene {chapter}.{scene} - {title}"
            continue

        if not in_voiceover:
            continue

        if raw_line.startswith("##") or raw_line.startswith("**Visual"):
            flush_scene()
            continue

        quote = clean_quote_line(raw_line)
        if quote:
            current_lines.append(quote)
        elif raw_line.strip() == ">":
            flush_paragraph()
        elif raw_line.strip() == "":
            flush_paragraph()
        else:
            flush_scene()

    flush_scene()
    return result


def write_outputs(data: dict[str, dict[str, object]]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    manifest: dict[str, object] = {"source": str(SCRIPT_PATH.relative_to(ROOT)), "scenes": {}}

    for scene, payload in sorted(data.items()):
        scene_dir = OUTPUT_DIR / scene
        scene_dir.mkdir(parents=True, exist_ok=True)

        paragraphs = payload["paragraphs"]
        assert isinstance(paragraphs, list)
        cues = estimate_cues(paragraphs, payload["start"], payload["end"])

        files = []
        for cue in cues:
            index = cue["index"]
            paragraph = cue["text"]
            filename = f"{index:03d}.txt"
            path = scene_dir / filename
            path.write_text(str(paragraph).strip() + "\n", encoding="utf-8")
            files.append(
                {
                    "file": filename,
                    "start": cue["start"],
                    "end": cue["end"],
                    "start_label": cue["start_label"],
                    "end_label": cue["end_label"],
                    "text": str(paragraph),
                }
            )

        scene_manifest = {
            "title": payload["title"],
            "start": payload["start"],
            "end": payload["end"],
            "start_label": format_timestamp(payload["start"]) if payload["start"] is not None else None,
            "end_label": format_timestamp(payload["end"]) if payload["end"] is not None else None,
            "directory": str(scene_dir.relative_to(ROOT)),
            "files": files,
        }
        manifest["scenes"][scene] = scene_manifest

    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    markdown = SCRIPT_PATH.read_text(encoding="utf-8")
    data = extract_voiceovers(markdown)
    write_outputs(data)

    total_files = sum(len(payload["paragraphs"]) for payload in data.values())
    print(f"Extracted {total_files} voiceover text files for {len(data)} scenes.")
    print(f"Wrote {OUTPUT_DIR.relative_to(ROOT)}/manifest.json")


if __name__ == "__main__":
    main()
