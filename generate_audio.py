#!/usr/bin/env python3
"""Export the app's Supertonic 3 F1 voice as static, per-page MP3 files.

Requires numpy, onnxruntime, soundfile and ffmpeg. Pass the upstream MIT helper
explicitly; model files remain local and are never included in the website.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--helper", type=Path, required=True)
    parser.add_argument("--models", type=Path, default=ROOT.parent.parent / "content/tts/supertonic")
    args = parser.parse_args()
    import numpy as np
    import soundfile as sf
    spec = importlib.util.spec_from_file_location("supertonic_helper", args.helper)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    engine = helper.load_text_to_speech(str(args.models / "onnx"))
    voice = helper.load_voice_style([str(args.models / "voice_styles/F1.json")])
    books = json.loads((ROOT / "data/books.json").read_text())
    manifest_path = ROOT / "data/audio-manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for book in books:
        for number, page in enumerate(book["pages"], 1):
            out = ROOT / page["audio"]
            digest = hashlib.sha256((page["text"] + "|supertonic-3|F1|8|1.05").encode()).hexdigest()
            if out.exists() and manifest.get(page["audio"], {}).get("input_sha256") == digest:
                continue
            np.random.seed(7300 + number)
            wav, duration = engine(page["text"], "en", voice, 8, speed=1.05)
            seconds = float(duration.flatten()[0])
            samples = wav.flatten()[:round(seconds * engine.sample_rate)]
            assert np.isfinite(samples).all() and np.max(np.abs(samples)) > 0.01
            out.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix="storyleaf-audio-") as temp:
                source = Path(temp) / "page.wav"
                sf.write(str(source), samples, engine.sample_rate)
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                                "-i", str(source), "-af", "loudnorm=I=-18:TP=-2:LRA=7",
                                "-c:a", "libmp3lame", "-b:a", "96k", str(out)], check=True)
            manifest[page["audio"]] = {"input_sha256": digest, "duration": round(seconds, 3),
                                       "engine": "Supertonic 3", "voice": "F1", "steps": 8,
                                       "speed": 1.05, "text": page["text"],
                                       "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
            print(f"{book['id']} page {number}: {seconds:.1f}s", flush=True)


if __name__ == "__main__":
    main()
