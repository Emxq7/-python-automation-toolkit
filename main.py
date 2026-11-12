"""Inventory a directory and optionally organize files by extension."""
from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


def extension_group(path: Path) -> str:
    return path.suffix.lower().lstrip(".") or "no_extension"


def inventory(folder: Path, recursive: bool = False) -> list[dict]:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")
    candidates = folder.rglob("*") if recursive else folder.iterdir()
    rows = []
    for path in candidates:
        if path.is_file() and not path.is_symlink():
            rows.append({
                "name": path.name,
                "extension": extension_group(path),
                "size_bytes": path.stat().st_size,
                "path": str(path),
            })
    return rows


def safe_target(directory: Path, filename: str) -> Path:
    target = directory / filename
    if not target.exists():
        return target
    source = Path(filename)
    index = 1
    while True:
        candidate = directory / f"{source.stem}_{index}{source.suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def write_report(rows: list[dict], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    columns = ["name", "extension", "size_bytes", "path"]
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def organize(rows: list[dict], root: Path) -> list[tuple[str, str]]:
    moved = []
    for row in rows:
        source = Path(row["path"])
        destination_dir = root / row["extension"]
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = safe_target(destination_dir, source.name)
        shutil.move(str(source), str(destination))
        moved.append((str(source), str(destination)))
    return moved


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Move files after inventory")
    parser.add_argument("--report", type=Path, default=Path("output/inventory.csv"))
    args = parser.parse_args()

    try:
        rows = inventory(args.folder, args.recursive)
        write_report(rows, args.report)
        print(f"Inventory contains {len(rows)} files. Report: {args.report}")
        if args.apply:
            moved = organize(rows, args.folder.expanduser().resolve())
            print(f"Moved {len(moved)} files.")
        else:
            print("Dry run only: no files were moved. Add --apply to organize.")
            for row in rows[:10]:
                print(f"{row['extension']:>12} | {row['name']} ({row['size_bytes']} bytes)")
    except (OSError, NotADirectoryError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
