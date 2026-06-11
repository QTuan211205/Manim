from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VOICEOVER_DIR = ROOT / "voiceover"
SENTENCE_MANIFEST_PATH = VOICEOVER_DIR / "sentence_audio_manifest.json"
CONFIG_PATH = VOICEOVER_DIR / "elevenlabs_config.json"
SENTENCE_OUTPUT_DIR = VOICEOVER_DIR / "generated_sentence_level"
SENTENCE_DURATION_MANIFEST = VOICEOVER_DIR / "sentence_duration_manifest.json"
MANIFEST_NAME = "elevenlabs_manifest.json"
MAX_RETRIES = 5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate ElevenLabs voiceover MP3s from sentence-level voiceover manifests."
    )
    parser.add_argument(
        "chapter",
        nargs="?",
        type=int,
        help="Optional chapter to generate, e.g. 3 generates all scene_3_* cues.",
    )
    parser.add_argument(
        "--scene",
        help="Optional scene id to generate, for example scene_1_1.",
    )
    parser.add_argument(
        "--start",
        help="Optional first cue. Accepts scene_3_2_004, scene_3_2/004, sc32_004, or sc32_4.",
    )
    parser.add_argument(
        "--manifest",
        default=str(SENTENCE_MANIFEST_PATH.relative_to(ROOT)),
        help="Manifest to read. Default: voiceover/sentence_audio_manifest.json.",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for generated MP3 files. Default comes from the selected manifest.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel API requests. Increase only if your ElevenLabs plan allows it. Default: 1.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate MP3 files that already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the files that would be generated without calling ElevenLabs.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def parse_start(value: str) -> tuple[int, int, int]:
    patterns = [
        re.compile(r"^scene_(\d+)_(\d+)_(\d+)$"),
        re.compile(r"^scene_(\d+)_(\d+)/(\d+)$"),
        re.compile(r"^sc(\d+)(\d+)_(\d+)$"),
    ]
    for pattern in patterns:
        match = pattern.match(value.strip())
        if match:
            chapter, scene, cue = (int(part) for part in match.groups())
            return chapter, scene, cue
    raise SystemExit(
        f"Invalid --start value: {value}. Use scene_3_2_4, scene_3_2/004, or sc32_4."
    )


def scene_key(scene_id: str) -> tuple[int, int]:
    match = re.fullmatch(r"scene_(\d+)_(\d+)", scene_id)
    if not match:
        raise ValueError(f"Invalid scene id in manifest: {scene_id}")
    return int(match.group(1)), int(match.group(2))


def cue_number(value: Any) -> int:
    if isinstance(value, int):
        return value
    text = Path(str(value)).stem
    match = re.search(r"(\d+)$", text)
    if not match:
        raise ValueError(f"Could not parse cue number from {value!r}")
    return int(match.group(1))


def resolve_root_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / path


def task_from_sentence_manifest(
    scene_id: str,
    item: dict[str, Any],
    *,
    output_dir: Path,
    output_dir_overridden: bool,
) -> dict[str, Any]:
    cue_id = item["cue"]
    cue = cue_number(cue_id)
    text_path = resolve_root_path(item["text_file"])

    if output_dir_overridden:
        audio_path = output_dir / f"{cue_id}.mp3"
    else:
        audio_path = resolve_root_path(item["audio_file"])

    text = item.get("text")
    if not text:
        text = text_path.read_text(encoding="utf-8").strip()

    return {
        "scene": scene_id,
        "cue": cue_id,
        "cue_number": cue,
        "text_file": text_path,
        "audio_file": audio_path,
        "text": text.strip(),
        "source_paragraph_file": item.get("source_paragraph_file"),
        "source_start": item.get("source_start"),
        "source_end": item.get("source_end"),
        "anchor": item.get("anchor", ""),
    }


def iter_tasks(
    manifest: dict[str, Any],
    *,
    chapter_filter: int | None,
    scene_filter: str | None,
    start: tuple[int, int, int] | None,
    output_dir: Path,
    output_dir_overridden: bool,
) -> list[dict[str, Any]]:
    scenes = manifest.get("scenes", {})
    if not isinstance(scenes, dict):
        raise SystemExit("Invalid manifest: expected a top-level `scenes` object.")

    tasks: list[dict[str, Any]] = []
    if start is not None:
        start_chapter, start_scene, start_cue = start
        if chapter_filter is not None and start_chapter != chapter_filter:
            raise SystemExit(
                f"--start points to chapter {start_chapter}, but requested chapter {chapter_filter}."
            )
        if scene_filter is not None and scene_filter != f"scene_{start_chapter}_{start_scene}":
            raise SystemExit(
                f"--start points to scene_{start_chapter}_{start_scene}, but requested {scene_filter}."
            )
    else:
        start_scene = 0
        start_cue = 1

    for scene_id, scene_payload in sorted(scenes.items(), key=lambda item: scene_key(item[0])):
        chapter, scene = scene_key(scene_id)
        if chapter_filter is not None and chapter != chapter_filter:
            continue
        if scene_filter is not None and scene_id != scene_filter:
            continue
        if scene < start_scene:
            continue

        for item in scene_payload["files"]:
            cue = cue_number(item.get("cue", item.get("file")))
            if scene == start_scene and cue < start_cue:
                continue

            if "text_file" not in item or "audio_file" not in item:
                raise SystemExit(
                    "Invalid sentence manifest entry: expected `text_file` and `audio_file`."
                )

            task = task_from_sentence_manifest(
                scene_id,
                item,
                output_dir=output_dir,
                output_dir_overridden=output_dir_overridden,
            )

            tasks.append(task)

    return tasks


def request_audio(*, api_key: str, config: dict[str, Any], text: str) -> bytes:
    voice_id = config["voice_id"]
    output_format = config.get("output_format", "mp3_44100_128")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format={output_format}"
    payload = {
        "text": text,
        "model_id": config.get("model_id", "eleven_multilingual_v2"),
        "voice_settings": config.get("voice_settings", {}),
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            retryable = error.code in {409, 429} or 500 <= error.code <= 599
            if not retryable or attempt == MAX_RETRIES:
                raise RuntimeError(f"ElevenLabs API error {error.code}: {body}") from error
            time.sleep(min(2**attempt, 30))
        except urllib.error.URLError as error:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"Could not reach ElevenLabs API: {error}") from error
            time.sleep(min(2**attempt, 30))

    raise RuntimeError("ElevenLabs request failed after retries.")


def probe_duration(path: Path) -> float | None:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    try:
        return round(float(result.stdout.strip()), 3)
    except ValueError:
        return None


def build_manifest_entry(
    task: dict[str, Any],
    *,
    config: dict[str, Any],
    status: str,
    error: str | None = None,
) -> dict[str, Any]:
    voice_settings = config.get("voice_settings", {})
    audio_path = task["audio_file"]
    entry = {
        "text_file": str(task["text_file"].relative_to(ROOT)),
        "audio_file": str(audio_path.relative_to(ROOT)),
        "scene": task["scene"],
        "cue": task["cue"],
        "cue_number": task["cue_number"],
        "voice_id": config["voice_id"],
        "model_id": config.get("model_id"),
        "output_format": config.get("output_format"),
        "stability": voice_settings.get("stability"),
        "similarity_boost": voice_settings.get("similarity_boost"),
        "speed": voice_settings.get("speed"),
        "status": status,
        "duration_seconds": probe_duration(audio_path) if audio_path.exists() else None,
        "start": task.get("start"),
        "end": task.get("end"),
        "start_label": task.get("start_label"),
        "end_label": task.get("end_label"),
        "source_paragraph_file": task.get("source_paragraph_file"),
        "source_start": task.get("source_start"),
        "source_end": task.get("source_end"),
        "anchor": task.get("anchor"),
    }
    if error:
        entry["error"] = error
    return entry


def is_paid_plan_required(entry: dict[str, Any]) -> bool:
    return (
        entry.get("status") == "failed"
        and "paid_plan_required" in str(entry.get("error", ""))
    )


def generate_one(
    task: dict[str, Any],
    *,
    api_key: str,
    config: dict[str, Any],
    force: bool,
    dry_run: bool,
) -> dict[str, Any]:
    audio_path = task["audio_file"]
    tmp_path = audio_path.with_suffix(audio_path.suffix + ".tmp")

    if audio_path.exists() and not force:
        print(f"skip existing {audio_path.relative_to(ROOT)}")
        return build_manifest_entry(task, config=config, status="skipped")

    if dry_run:
        print(f"would generate {audio_path.relative_to(ROOT)}")
        return build_manifest_entry(task, config=config, status="planned")

    print(f"generate {audio_path.relative_to(ROOT)}")
    try:
        audio = request_audio(api_key=api_key, config=config, text=task["text"])
        tmp_path.write_bytes(audio)
        tmp_path.replace(audio_path)
        return build_manifest_entry(task, config=config, status="generated")
    except Exception as error:
        if tmp_path.exists():
            tmp_path.unlink()
        return build_manifest_entry(task, config=config, status="failed", error=str(error))


def main() -> None:
    args = parse_args()
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1.")
    if args.chapter is None and args.scene is None:
        raise SystemExit("Provide a chapter number or --scene scene_N_M.")

    manifest_path = resolve_root_path(args.manifest)
    manifest = load_json(manifest_path)
    config = load_json(CONFIG_PATH)

    if args.output_dir:
        output_dir = resolve_root_path(args.output_dir)
        output_dir_overridden = True
    else:
        output_dir = resolve_root_path(manifest.get("output_dir", str(SENTENCE_OUTPUT_DIR.relative_to(ROOT))))
        output_dir_overridden = False

    output_dir.mkdir(parents=True, exist_ok=True)

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key and not args.dry_run:
        raise SystemExit("Missing ELEVENLABS_API_KEY. Export it before generating audio.")

    start = parse_start(args.start) if args.start else None
    tasks = iter_tasks(
        manifest,
        chapter_filter=args.chapter,
        scene_filter=args.scene,
        start=start,
        output_dir=output_dir,
        output_dir_overridden=output_dir_overridden,
    )
    if not tasks:
        target = args.scene or f"chapter {args.chapter}"
        raise SystemExit(f"No voiceover cues found for {target}.")

    total_chars = sum(len(task["text"]) for task in tasks)
    target = args.scene or f"chapter {args.chapter}"
    print(f"Selected {target}: {len(tasks)} file(s), {total_chars} character(s).")

    results: list[dict[str, Any]] = []
    if args.workers == 1:
        for task in tasks:
            result = generate_one(
                task,
                api_key=api_key or "",
                config=config,
                force=args.force,
                dry_run=args.dry_run,
            )
            results.append(result)
            if is_paid_plan_required(result):
                print("Stopping early: this voice requires a paid ElevenLabs plan for API use.")
                break
    else:
        first_result = generate_one(
            tasks[0],
            api_key=api_key or "",
            config=config,
            force=args.force,
            dry_run=args.dry_run,
        )
        results.append(first_result)
        if is_paid_plan_required(first_result):
            print("Stopping early: this voice requires a paid ElevenLabs plan for API use.")
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = [
                    executor.submit(
                        generate_one,
                        task,
                        api_key=api_key or "",
                        config=config,
                        force=args.force,
                        dry_run=args.dry_run,
                    )
                    for task in tasks[1:]
                ]
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())

    results.sort(key=lambda item: (*scene_key(item["scene"]), item["cue_number"]))
    output_manifest = {
        "source_manifest": str(manifest_path.relative_to(ROOT)),
        "config": str(CONFIG_PATH.relative_to(ROOT)),
        "chapter": args.chapter,
        "scene": args.scene,
        "start": args.start,
        "total_characters": total_chars,
        "output_dir": str(output_dir.relative_to(ROOT)),
        "entries": results,
    }
    manifest_path = output_dir / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(output_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if not args.dry_run:
        durations = {
            Path(entry["audio_file"]).name: entry["duration_seconds"]
            for entry in results
            if entry.get("duration_seconds") is not None
        }
        SENTENCE_DURATION_MANIFEST.write_text(
            json.dumps(durations, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    counts = {status: 0 for status in ["generated", "skipped", "planned", "failed"]}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1

    print(
        "Done: "
        f"{counts.get('generated', 0)} generated, "
        f"{counts.get('skipped', 0)} skipped, "
        f"{counts.get('planned', 0)} planned, "
        f"{counts.get('failed', 0)} failed."
    )
    print(f"Wrote {manifest_path.relative_to(ROOT)}")
    if not args.dry_run:
        print(f"Wrote {SENTENCE_DURATION_MANIFEST.relative_to(ROOT)}")

    if counts.get("failed", 0):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
