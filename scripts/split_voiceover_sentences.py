#!/usr/bin/env python3
"""Split paragraph-level voiceover text into sentence-level cue files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOICEOVER_DIR = ROOT / "voiceover"
SOURCE_MANIFEST = VOICEOVER_DIR / "manifest.json"
OUTPUT_MANIFEST = VOICEOVER_DIR / "sentence_audio_manifest.json"


ABBREVIATIONS = {
    "e.g.",
    "i.e.",
    "Mr.",
    "Mrs.",
    "Ms.",
    "Dr.",
    "Prof.",
    "vs.",
    "etc.",
}


def scene_prefix(scene_id: str) -> str:
    """Convert scene_3_2 to sc32."""
    match = re.fullmatch(r"scene_(\d+)_(\d+)", scene_id)
    if not match:
        raise ValueError(f"Unexpected scene id: {scene_id}")
    chapter, scene = match.groups()
    return f"sc{chapter}{scene}"


def protect_abbreviations(text: str) -> str:
    protected = text
    for abbreviation in ABBREVIATIONS:
        pattern = re.compile(rf"(?<![A-Za-z]){re.escape(abbreviation)}")
        protected = pattern.sub(abbreviation.replace(".", "<DOT>"), protected)
    return protected


def restore_abbreviations(text: str) -> str:
    return text.replace("<DOT>", ".")


def split_sentences(text: str) -> list[str]:
    """Split English narration into sentences while preserving common abbreviations."""
    normalized = re.sub(r"\s+", " ", text.strip())
    if not normalized:
        return []

    protected = protect_abbreviations(normalized)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", protected)
    return [restore_abbreviations(part).strip() for part in parts if part.strip()]


def write_text(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def build_sentence_manifest(scene_filter: str | None, force: bool) -> dict:
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    sentence_manifest = {
        "source": str(SOURCE_MANIFEST.relative_to(ROOT)),
        "output_dir": "voiceover/generated_sentence_level",
        "scenes": {},
    }

    for scene_id, scene_data in source["scenes"].items():
        if scene_filter and scene_id != scene_filter:
            continue

        prefix = scene_prefix(scene_id)
        scene_dir = VOICEOVER_DIR / f"{scene_id}_sentence"
        entries = []
        cue_index = 1

        for paragraph in scene_data["files"]:
            paragraph_file = paragraph["file"]
            for sentence in split_sentences(paragraph["text"]):
                text_file = scene_dir / f"{cue_index:03d}.txt"
                audio_file = VOICEOVER_DIR / "generated_sentence_level" / f"{prefix}_{cue_index:03d}.mp3"
                write_text(text_file, sentence, force=force)

                entries.append(
                    {
                        "cue": f"{prefix}_{cue_index:03d}",
                        "text_file": str(text_file.relative_to(ROOT)),
                        "audio_file": str(audio_file.relative_to(ROOT)),
                        "source_paragraph_file": paragraph_file,
                        "source_start": paragraph.get("start"),
                        "source_end": paragraph.get("end"),
                        "anchor": "",
                        "text": sentence,
                    }
                )
                cue_index += 1

        sentence_manifest["scenes"][scene_id] = {
            "title": scene_data.get("title", ""),
            "directory": str(scene_dir.relative_to(ROOT)),
            "files": entries,
        }

    return sentence_manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split voiceover/manifest.json paragraph text into sentence-level cue files."
    )
    parser.add_argument(
        "--scene",
        help="Only split one scene, for example scene_1_1. Default: split all scenes.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing sentence-level text files.",
    )
    args = parser.parse_args()

    if not SOURCE_MANIFEST.exists():
        raise SystemExit(f"Missing source manifest: {SOURCE_MANIFEST}")

    sentence_manifest = build_sentence_manifest(args.scene, force=args.force)

    if args.scene and OUTPUT_MANIFEST.exists():
        existing = json.loads(OUTPUT_MANIFEST.read_text(encoding="utf-8"))
        existing.setdefault("scenes", {}).update(sentence_manifest["scenes"])
        existing["source"] = sentence_manifest["source"]
        existing["output_dir"] = sentence_manifest["output_dir"]
        sentence_manifest = existing

    OUTPUT_MANIFEST.write_text(
        json.dumps(sentence_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    scene_count = len(sentence_manifest["scenes"])
    cue_count = sum(len(scene["files"]) for scene in sentence_manifest["scenes"].values())
    print(f"Wrote {cue_count} sentence cues across {scene_count} scenes")
    print(f"Manifest: {OUTPUT_MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
