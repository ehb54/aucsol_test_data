#!/usr/bin/env python3
"""Generate synthetic .auc archives from a JSON spec.

The selected spec (default: config/specs/base.json) maps each experiment to
checked-in model, buffer, and simulation-parameter XML. Each channel is
simulated headlessly. Non-RA outputs are relabeled and their CRC updated, then
all channels for an experiment are packaged in one archive with a GNU SHA-256
manifest.

Standard output keeps the configured scan count and duration. --samples instead
writes a smaller tier using the reductions defined by the selected spec.

--us-bin-dir must contain us_sim_inputs_gen, us_astfem_sim, and
us_mwl_species_sim. Its sibling etc/ directory supplies rotor and centerpiece
definitions. See config/README.md for how the inputs relate and --help for
usage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import zlib
from pathlib import Path

SCRIPT_DIR    = Path(__file__).resolve().parent
TEST_DATA     = SCRIPT_DIR.parent
CONFIG_DIR    = TEST_DATA / "config"
SPECS_DIR     = CONFIG_DIR / "specs"
MODELS_DIR    = CONFIG_DIR / "models"
BUFFERS_DIR   = CONFIG_DIR / "buffers"
SIMPARAMS_DIR = CONFIG_DIR / "simparams"

# Populated by load_spec(); no spec is read at import time.
SPEC_PATH: Path | None = None
_SPEC_CONFIG: dict | None = None
_GENERATED_DIR: Path | None = None
SAMPLES_DIR: Path | None = None
EXPERIMENTS: dict | None = None
SAMPLE_DEFAULTS: dict | None = None

# Per-channel simparams overrides that do not change calculated geometry.
SIMPARAMS_SAFE_OVERRIDE_KEYS = ("rnoise", "lrnoise", "tinoise", "rinoise", "baseline")

# Per-channel model overrides. UltraScan's model generator writes signal="1".
MODEL_SAFE_OVERRIDE_KEYS = ("signal",)

# Supported fields that patch working XML copies.
SAFE_OVERRIDE_KEYS = SIMPARAMS_SAFE_OVERRIDE_KEYS + MODEL_SAFE_OVERRIDE_KEYS


def resolve_spec_path(spec_arg: str) -> Path:
    """Resolve a spec name under config/specs or an explicit JSON path."""
    p = Path(spec_arg)
    if p.exists():
        return p.resolve()
    candidate = SPECS_DIR / f"{spec_arg}.json"
    if candidate.exists():
        return candidate
    raise FileNotFoundError(
        f"spec file not found: tried {p} and {candidate}")


def load_spec(spec_path: Path) -> None:
    """Load the selected spec and derive its experiment and output globals."""
    global SPEC_PATH, _SPEC_CONFIG, _GENERATED_DIR, SAMPLES_DIR, EXPERIMENTS, SAMPLE_DEFAULTS
    SPEC_PATH = spec_path
    _SPEC_CONFIG = json.loads(spec_path.read_text())
    _GENERATED_DIR = TEST_DATA / "datasets" / "generated" / _SPEC_CONFIG["dataset_name"]
    SAMPLES_DIR = _GENERATED_DIR / "samples"
    EXPERIMENTS = {c["id"]: c for c in _SPEC_CONFIG["experiments"]}
    SAMPLE_DEFAULTS = _SPEC_CONFIG["sample_defaults"]


def model_path(channel: dict) -> Path:
    """Return the model XML selected by a channel."""
    return MODELS_DIR / channel["model"] / "model.xml"


def buffer_path(channel: dict) -> Path:
    """Return the buffer XML selected by a channel."""
    return BUFFERS_DIR / channel["buffer"] / "buffer.xml"


def simparams_path(exp_id: str) -> Path:
    """Return the simulation-parameter XML selected by an experiment."""
    return SIMPARAMS_DIR / EXPERIMENTS[exp_id]["simparams"] / "simparams.xml"


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def headless_env():
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    return env


def _patch_xml_attr(text: str, name: str, value, filename: str = "XML file") -> str:
    new_text, n = re.subn(rf'{name}="[^"]*"', f'{name}="{value}"', text)
    assert n >= 1, f"{name} attribute not found in {filename}"
    return new_text


def _xml_attr(text: str, name: str, filename: str = "XML file") -> str:
    m = re.search(rf'{name}="([^"]*)"', text)
    assert m, f"{name} attribute not found in {filename}"
    return m.group(1)


def resolve_sample_params(exp_id: str) -> dict:
    """Merge sample defaults with an experiment's sample overrides."""
    return {**SAMPLE_DEFAULTS, **EXPERIMENTS[exp_id].get("samples", {})}


def resolve_simparams(exp_id: str, channel: dict, work_dir: Path, samples: bool) -> Path:
    """Create a working simparams copy with channel and sample overrides.

    Centerpiece values are simulator flags because simparams XML does not
    persist the calculated bottom position.
    """
    dest = work_dir / "simparams.xml"
    text = simparams_path(exp_id).read_text()

    for key in SIMPARAMS_SAFE_OVERRIDE_KEYS:
        if key in channel:
            text = _patch_xml_attr(text, key, channel[key], filename="simparams.xml")

    if samples:
        sample_params = resolve_sample_params(exp_id)
        new_scans = sample_params["scans"]
        new_hrs, new_mins = sample_params["duration_hrs"], sample_params["duration_mins"]
        new_duration = new_hrs * 60 + new_mins

        orig_scans = int(_xml_attr(text, "scans", filename="simparams.xml"))
        orig_hrs = float(_xml_attr(text, "duration_hrs", filename="simparams.xml"))
        orig_mins = float(_xml_attr(text, "duration_mins", filename="simparams.xml"))
        orig_duration = orig_hrs * 60 + orig_mins

        assert new_scans >= 1, \
            f"{exp_id}: sample scans must be >=1, got {new_scans}"
        assert new_duration > 0, \
            f"{exp_id}: sample duration must be >0, got {new_hrs}h{new_mins}m"
        assert new_scans <= orig_scans, \
            f"{exp_id}: sample scans ({new_scans}) exceeds original ({orig_scans})"
        assert new_duration <= orig_duration, \
            f"{exp_id}: sample duration ({new_hrs}h{new_mins}m) exceeds original ({orig_hrs}h{orig_mins}m)"

        text = _patch_xml_attr(text, "scans", new_scans, filename="simparams.xml")
        text = _patch_xml_attr(text, "duration_hrs", new_hrs, filename="simparams.xml")
        text = _patch_xml_attr(text, "duration_mins", new_mins, filename="simparams.xml")

    dest.write_text(text)
    return dest


def resolve_channel_model(channel: dict, work_dir: Path) -> Path:
    """Create a working model copy with supported channel overrides."""
    dest = work_dir / "model.xml"
    text = model_path(channel).read_text()

    for key in MODEL_SAFE_OVERRIDE_KEYS:
        if key in channel:
            text = _patch_xml_attr(text, key, channel[key], filename="model.xml")

    dest.write_text(text)
    return dest


def channel_model_params(channel: dict):
    """Read model values used to create each wavelength model."""
    root = ET.parse(model_path(channel)).getroot()
    analyte = root.find(".//analyte")
    return analyte.get("mw"), analyte.get("vbar20"), analyte.get("f_f0")


def gen_wavelength_model(bin_dir, out_dir, run_id, channel_label, wavelength, channel=None):
    cmd = [
        bin_dir / "us_sim_inputs_gen", "--out", out_dir,
        "--run-id", run_id, "--channel", channel_label, "--wavelength", f"{wavelength:03d}",
    ]
    if channel:
        mw, vbar20, f_f0 = channel_model_params(channel)
        cmd += ["--mw", mw, "--vbar20", vbar20, "--f-f0", f_f0]
    run(cmd)
    model_path_out = out_dir / f"model_{channel_label}_{wavelength:03d}.xml"

    # The generator has no --signal flag, so patch its output when requested.
    if channel and "signal" in channel:
        text = _patch_xml_attr(model_path_out.read_text(), "signal", channel["signal"], filename="model.xml")
        model_path_out.write_text(text)

    return model_path_out


def _geometry_flags(channel: dict) -> list:
    """Return explicit geometry overrides; both indices default to zero."""
    flags = []
    if "centerpiece" in channel:
        flags += ["--centerpiece", str(channel["centerpiece"])]
    if "centerpiece_channel" in channel:
        flags += ["--centerpiece-channel", str(channel["centerpiece_channel"])]
    return flags


def run_astfem_sim(bin_dir, model_path, buffer_path, simparams_path, rotor, channel, out_dir):
    run([
        bin_dir / "us_astfem_sim",
        "--model", model_path,
        "--buffer", buffer_path,
        "--simparams", simparams_path,
        "--rotor", rotor,
        *_geometry_flags(channel),
        "--start", "--save", out_dir, "--close", "--errors-cl",
    ], env=headless_env())


def run_mwl_species_sim(bin_dir, model_paths, buffer_path, simparams_path, rotor, channel, out_dir):
    run([
        bin_dir / "us_mwl_species_sim",
        "--models", ",".join(str(p) for p in model_paths),
        "--buffer", buffer_path,
        "--simparams", simparams_path,
        "--rotor", rotor,
        *_geometry_flags(channel),
        "--start", "--save", out_dir, "--close", "--errors-cl",
    ], env=headless_env())


def relabel_auc_type(path: Path, new_type: str) -> Path:
    """Rewrite the 2-byte data type and recompute the trailing CRC-32.
    Returns the (possibly renamed) path, with the type substring in the
    filename updated to match, e.g. foo.RA.1.S.123.auc -> foo.RI.1.S.123.auc.
    """
    data = bytearray(path.read_bytes())
    assert data[:4] == b"UCDA", f"{path}: not a .auc file (bad magic)"
    old_type = data[6:8].decode("ascii")
    data[6:8] = new_type.encode("ascii")

    body = bytes(data[:-4])
    crc = zlib.crc32(body, 0xFFFFFFFF) & 0xFFFFFFFF
    data[-4:] = crc.to_bytes(4, "little")

    new_name = path.name.replace(f".{old_type}.", f".{new_type}.")
    new_path = path.with_name(new_name)
    new_path.write_bytes(data)
    if new_path != path:
        path.unlink()
    return new_path


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def package_experiment(exp_id: str, files: list[Path], tier_dir: Path | None = None, suffix: str = "synthetic"):
    """Package an experiment and update its tier's SHA-256 manifest."""
    if tier_dir is None:
        tier_dir = _GENERATED_DIR
    exp_dir = tier_dir / EXPERIMENTS[exp_id]["dir"]
    exp_dir.mkdir(parents=True, exist_ok=True)

    zip_path = exp_dir / f"{exp_id}_{suffix}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=f.name)

    update_checksums(zip_path, tier_dir)
    print(f"  -> {zip_path.relative_to(TEST_DATA)}")


def update_checksums(zip_path: Path, tier_dir: Path | None = None):
    if tier_dir is None:
        tier_dir = _GENERATED_DIR
    checksums_path = tier_dir / "checksums.sha256"
    rel = zip_path.relative_to(tier_dir).as_posix()
    digest = sha256_of(zip_path)

    lines = []
    if checksums_path.exists():
        for line in checksums_path.read_text().splitlines():
            if line.strip() and not line.endswith(rel):
                lines.append(line)
    lines.append(f"{digest}  {rel}")
    checksums_path.write_text("\n".join(lines) + "\n")


def channel_analyte_description_and_s(channel: dict) -> tuple[str, float]:
    """Return the model's analyte name and sedimentation value in Svedbergs."""
    root = ET.parse(model_path(channel)).getroot()
    analyte = root.find(".//analyte")
    return analyte.get("name"), float(analyte.get("s")) * 1e13


def summary_row(exp_id: str, tier_dir: Path, suffix: str) -> str | None:
    """Return a README row when the experiment archive exists."""
    entry = EXPERIMENTS[exp_id]
    zip_path = tier_dir / entry["dir"] / f"{exp_id}_{suffix}.zip"
    if not zip_path.exists():
        return None

    channel_bits = []
    for ch in entry["channels"]:
        _, s = channel_analyte_description_and_s(ch)
        s_str = f"{s:.2f}" if s < 1 else f"{s:.1f}"
        data_type = ch["data_type"]
        wavelengths = ch.get("wavelengths")
        if wavelengths:
            wl_list = wavelengths.split(",")
            tag = f"{data_type}; {len(wl_list)} wavelengths ({'/'.join(wl_list)} nm)"
        elif "/" in data_type:
            tag = data_type.replace("/", " + ")
        else:
            tag = data_type
        channel_bits.append(f"{ch['channel']}: {tag}; s ≈ {s_str} S")

    type_tags = ", ".join(dict.fromkeys(ch["data_type"] for ch in entry["channels"]))
    represents = f"{entry['description']} — {'; '.join(channel_bits)}"

    rel_zip = zip_path.relative_to(tier_dir).as_posix()
    return f"| `{exp_id}` | `{rel_zip}` | {type_tags} | {represents} |"


def write_readme(tier_dir: Path, samples: bool):
    """Write a generated README for all selected archives present in a tier."""
    suffix = "sample_synthetic" if samples else "synthetic"
    rows = [r for eid in EXPERIMENTS if (r := summary_row(eid, tier_dir, suffix))]
    table = "\n".join([
        "| Experiment ID | Archive | Data type | Description |",
        "|---|---|---|---|",
        *rows,
    ])

    spec_rel = SPEC_PATH.relative_to(TEST_DATA).as_posix() if SPEC_PATH.is_relative_to(TEST_DATA) else str(SPEC_PATH)
    is_default_spec = SPEC_PATH == (SPECS_DIR / "base.json")
    # Use a short --spec name for specs stored in config/specs.
    spec_display = SPEC_PATH.stem if SPEC_PATH.parent == SPECS_DIR else spec_rel
    spec_flag = "" if is_default_spec else f" --spec {spec_display}"

    if samples:
        sd = SAMPLE_DEFAULTS
        body = f"""# Synthetic Samples

> Generated by `scripts/generate_synthetic_data.py`. Do not edit by hand.

This is the smaller companion to the [standard synthetic dataset](../). It uses
the same chemistry but reduces each experiment by default to {sd['scans']} scans
over {sd['duration_hrs']} h {sd['duration_mins']} min. The `sample_defaults` in
`{spec_rel}` and any experiment-level `samples` values control these limits.

Use this tier for tests that do not need a full multi-scan run. See
[Generating synthetic data](../../../../README.md#generate-synthetic-data) for
the method and known limitations.

## Contents

{table}

## Regenerate

Run from the repository root:

```bash
python3 scripts/generate_synthetic_data.py --us-bin-dir /path/to/ultrascan/bin --samples{spec_flag}
```
"""
    else:
        body = f"""# Synthetic Data

> Generated by `scripts/generate_synthetic_data.py`. Do not edit by hand.

UltraScan's finite-element simulators compute these datasets from the checked-in
models, buffers, and simulation parameters. This standard tier keeps each
experiment's configured scan count and duration.

See [Generating synthetic data](../../../README.md#generate-synthetic-data) for
the generation method, inputs, and known limitations.

`{spec_rel}` defines this dataset. Its `dataset_name` selects the directory
under `datasets/generated/`; each experiment's `id` names its archive and its
`dir` selects the archive's subdirectory. Other specs generate separate sibling
datasets.

## Contents

{table}

## Regenerate

Run from the repository root:

```bash
python3 scripts/generate_synthetic_data.py --us-bin-dir /path/to/ultrascan/bin{spec_flag}
```
"""
    (tier_dir / "README.md").write_text(body)


def gather_sim_outputs(out_dir: Path) -> list[Path]:
    """Collect .auc files and their time-state metadata."""
    files = list(out_dir.glob("*.auc"))
    files += list(out_dir.glob("*.time_state.tmst"))
    files += list(out_dir.glob("*.time_state.xml"))
    return files


def build_channel(bin_dir: Path, exp_id: str, channel: dict, work: Path, samples: bool = False) -> list[Path]:
    """Simulate one channel and return its unpackaged output files."""
    label = f"{exp_id}-{channel['channel']}"
    entry = EXPERIMENTS[exp_id]

    inputs_dir = work / f"{label}-inputs"
    inputs_dir.mkdir()
    simparams = resolve_simparams(exp_id, channel, inputs_dir, samples)

    out_dir = work / f"{label}-out"
    out_dir.mkdir()

    wavelengths = channel.get("wavelengths")
    if wavelengths:
        wl_list = [int(w) for w in wavelengths.split(",")]
        model_paths = [
            gen_wavelength_model(bin_dir, inputs_dir, channel["mwl_run_id"], channel["channel"], wl, channel=channel)
            for wl in wl_list
        ]
        run_mwl_species_sim(bin_dir, model_paths, buffer_path(channel), simparams, entry["rotor"], channel, out_dir)
        for auc in out_dir.glob("*.auc"):
            relabel_auc_type(auc, "RI")
        return gather_sim_outputs(out_dir)

    model = resolve_channel_model(channel, inputs_dir)
    run_astfem_sim(bin_dir, model, buffer_path(channel), simparams, entry["rotor"], channel, out_dir)
    auc_files = list(out_dir.glob("*.auc"))
    assert len(auc_files) == 1, f"expected 1 .auc file, got {auc_files}"
    base = auc_files[0]

    data_type = channel["data_type"]
    if "/" in data_type:
        # Copy one simulation for each requested data-type tag.
        # Keep ".RA." in each name until relabel_auc_type() processes it.
        tags = data_type.split("/")
        copies = [base]
        for tag in tags[1:]:
            copy = base.with_name(base.stem + f"-{tag.lower()}" + base.suffix)
            shutil.copy(base, copy)
            copies.append(copy)
        for copy, tag in zip(copies, tags):
            relabel_auc_type(copy, tag)
    elif data_type != "RA":
        relabel_auc_type(base, data_type)

    return gather_sim_outputs(out_dir)


def build_experiment(bin_dir: Path, exp_id: str, work: Path, samples: bool = False):
    all_files = []
    for channel in EXPERIMENTS[exp_id]["channels"]:
        all_files += build_channel(bin_dir, exp_id, channel, work, samples)

    if samples:
        package_experiment(exp_id, all_files, SAMPLES_DIR, "sample_synthetic")
    else:
        package_experiment(exp_id, all_files)


def clean_target_dir(target_dir: Path):
    """Remove generated files and directories selected by the current spec."""
    dirs = {(target_dir / entry["dir"]) for entry in EXPERIMENTS.values()}
    for exp_dir in dirs:
        if exp_dir.exists():
            shutil.rmtree(exp_dir)
            print(f"  removed {exp_dir.relative_to(TEST_DATA)}")

    for name in ("checksums.sha256", "README.md"):
        f = target_dir / name
        if f.exists():
            f.unlink()
            print(f"  removed {f.relative_to(TEST_DATA)}")

    # Prune empty parents created by nested experiment directories.
    parents = sorted({p for d in dirs for p in d.parents if target_dir in p.parents},
        key=lambda p: len(p.parts), reverse=True)
    for p in parents:
        if p.exists() and not any(p.iterdir()):
            p.rmdir()

    # Remove the tier directory if nothing remains.
    if target_dir.exists() and not any(target_dir.iterdir()):
        target_dir.rmdir()
        print(f"  removed {target_dir.relative_to(TEST_DATA)}")


def load_centerpieces(bin_dir: Path) -> list[list[float]] | None:
    """Load zero-based centerpiece row bottoms from the runtime etc directory."""
    path = bin_dir.parent / "etc" / "abstractCenterpieces.xml"
    if not path.exists():
        return None
    root = ET.parse(path).getroot()
    return [
        [float(row.get("bottom")) for row in cp.findall("row")]
        for cp in root.findall("abstractCenterpiece")
    ]


def load_rotor_ids(bin_dir: Path) -> set[str]:
    """Rotor ids defined under <us_bin_dir>/../etc/rotors/*.xml."""
    rotors_dir = bin_dir.parent / "etc" / "rotors"
    ids = set()
    for f in rotors_dir.glob("R*.xml") if rotors_dir.exists() else []:
        rotor = ET.parse(f).getroot().find("Rotor")
        if rotor is not None and rotor.get("id"):
            ids.add(rotor.get("id"))
    return ids


def validate_config(bin_dir: Path | None) -> bool:
    """Validate referenced XML, sample limits, and optional runtime geometry.

    Errors fail validation; warnings do not. Runtime checks use zero-based
    centerpiece indices, matching the simulator CLI.
    """
    errors, warnings = [], []

    centerpieces = rotor_ids = None
    if bin_dir:
        centerpieces = load_centerpieces(bin_dir)
        if centerpieces is None:
            warnings.append(f"{bin_dir.parent / 'etc' / 'abstractCenterpieces.xml'} not found -- skipping centerpiece/bottom checks")
        rotor_ids = load_rotor_ids(bin_dir)
        if not rotor_ids:
            warnings.append(f"no rotor definitions found under {bin_dir.parent / 'etc' / 'rotors'} -- skipping rotor checks")

    for exp_id, entry in EXPERIMENTS.items():
        sp_path = simparams_path(exp_id)
        if not sp_path.exists():
            errors.append(f"{exp_id}: simparams not found: {sp_path}")
            continue
        try:
            sp_root = ET.parse(sp_path).getroot()
        except ET.ParseError as e:
            errors.append(f"{exp_id}: {sp_path} is not valid XML ({e})")
            continue

        params = sp_root.find(".//params")
        speedstep = sp_root.find(".//speedstep")
        if params is None or speedstep is None:
            errors.append(f"{exp_id}: {sp_path} missing <params>/<speedstep>")
            continue

        for attr in ("meshType", "gridType", "simpoints", "radialres", "meniscus", "bottom"):
            if params.get(attr) is None:
                errors.append(f"{exp_id}: {sp_path} <params> missing '{attr}'")
        for attr in ("rotorspeed", "scans", "duration_hrs", "duration_mins"):
            if speedstep.get(attr) is None:
                errors.append(f"{exp_id}: {sp_path} <speedstep> missing '{attr}'")

        bottom = None
        if params.get("bottom") is not None and params.get("meniscus") is not None:
            bottom, meniscus = float(params.get("bottom")), float(params.get("meniscus"))
            if meniscus >= bottom:
                errors.append(f"{exp_id}: {sp_path} meniscus ({meniscus}) >= bottom ({bottom})")

        if speedstep.get("scans") is not None and speedstep.get("duration_hrs") is not None:
            orig_scans = int(speedstep.get("scans"))
            orig_duration = float(speedstep.get("duration_hrs")) * 60 + float(speedstep.get("duration_mins"))
            sample_params = resolve_sample_params(exp_id)
            new_scans = sample_params["scans"]
            new_duration = sample_params["duration_hrs"] * 60 + sample_params["duration_mins"]
            if new_scans < 1:
                errors.append(f"{exp_id}: samples scans must be >=1, got {new_scans}")
            if new_duration <= 0:
                errors.append(f"{exp_id}: samples duration must be >0, got {sample_params['duration_hrs']}h{sample_params['duration_mins']}m")
            if new_scans > orig_scans:
                errors.append(f"{exp_id}: samples scans ({new_scans}) exceeds original ({orig_scans})")
            if new_duration > orig_duration:
                errors.append(f"{exp_id}: samples duration ({new_duration}m) exceeds original ({orig_duration}m)")

        if rotor_ids is not None and entry.get("rotor") not in rotor_ids:
            errors.append(f"{exp_id}: rotor id {entry.get('rotor')!r} not found under etc/rotors")

        for ch in entry["channels"]:
            label = f"{exp_id}-{ch['channel']}"

            mp = model_path(ch)
            if not mp.exists():
                errors.append(f"{label}: model not found: {mp}")
            else:
                try:
                    analyte = ET.parse(mp).getroot().find(".//analyte")
                    if analyte is None:
                        errors.append(f"{label}: {mp} has no <analyte>")
                    else:
                        for attr in ("mw", "vbar20", "f_f0", "s", "name"):
                            if analyte.get(attr) is None:
                                errors.append(f"{label}: {mp} analyte missing '{attr}'")
                except ET.ParseError as e:
                    errors.append(f"{label}: {mp} is not valid XML ({e})")

            bp = buffer_path(ch)
            if not bp.exists():
                errors.append(f"{label}: buffer not found: {bp}")
            else:
                try:
                    buf = ET.parse(bp).getroot().find(".//buffer")
                    if buf is None:
                        errors.append(f"{label}: {bp} has no <buffer>")
                    else:
                        for attr in ("density", "viscosity", "ph"):
                            if buf.get(attr) is None:
                                errors.append(f"{label}: {bp} buffer missing '{attr}'")
                except ET.ParseError as e:
                    errors.append(f"{label}: {bp} is not valid XML ({e})")

            if "wavelengths" in ch and "mwl_run_id" not in ch:
                errors.append(f"{label}: has 'wavelengths' but no 'mwl_run_id'")
            if "centerpiece_channel" in ch and "centerpiece" not in ch:
                warnings.append(f"{label}: has 'centerpiece_channel' but no 'centerpiece' (defaults to centerpiece 0)")
            if "signal" in ch and not (float(ch["signal"]) > 0):
                errors.append(f"{label}: 'signal' override must be >0, got {ch['signal']}")

            if centerpieces is not None and "centerpiece" in ch:
                cp_index = int(ch["centerpiece"])
                if cp_index < 0 or cp_index >= len(centerpieces):
                    errors.append(
                        f"{label}: centerpiece index {cp_index} out of range "
                        f"for abstractCenterpieces.xml ({len(centerpieces)} entries)")
                else:
                    rows = centerpieces[cp_index]
                    row_idx = ch.get("centerpiece_channel", 0)
                    if row_idx >= len(rows):
                        errors.append(f"{label}: centerpiece_channel {row_idx} out of range for centerpiece index {cp_index} ({len(rows)} row(s))")
                    elif bottom is not None:
                        cp_bottom = rows[row_idx]
                        if abs(cp_bottom - bottom) > 1e-6:
                            errors.append(
                                f"{label}: simparams bottom ({bottom}) doesn't match centerpiece index {cp_index} row "
                                f"{row_idx} bottom ({cp_bottom}) -- simulator will fail with 'not enough radial "
                                f"points'; point {exp_id}'s simparams at a variant with bottom={cp_bottom}"
                            )

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)"
          + ("" if bin_dir else " (centerpiece/rotor checks skipped -- pass --us-bin-dir to enable them)"))
    return not errors


SHORT_DESCRIPTION = (
    "Generate synthetic .auc archives from a spec using UltraScan's "
    "finite-element simulators. Defaults to config/specs/base.json; use "
    "--spec to select another spec. See config/README.md for the input model."
)

EPILOG = """\
Examples:
  python3 generate_synthetic_data.py --us-bin-dir /path/to/ultrascan/bin
  python3 generate_synthetic_data.py --us-bin-dir /path/to/ultrascan/bin --samples
  python3 generate_synthetic_data.py --spec examples --us-bin-dir /path/to/ultrascan/bin
  python3 generate_synthetic_data.py --validate --us-bin-dir /path/to/ultrascan/bin
  python3 generate_synthetic_data.py --clean
"""


def main():
    parser = argparse.ArgumentParser(description=SHORT_DESCRIPTION, epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--spec", default="base", metavar="NAME_OR_PATH",
        help="Spec name under config/specs (default: base) or path to a JSON "
             "spec. All operations use the selected spec.")
    parser.add_argument("--us-bin-dir",
        default=os.environ.get("US_BIN_DIR"),
        help="Path to an UltraScan3 bin/ directory "
             "(contains us_sim_inputs_gen, us_astfem_sim, "
             "us_mwl_species_sim); an installation or build output both "
             "work. Or set US_BIN_DIR. Required to "
             "generate; optional for --validate (enables its "
             "centerpiece/rotor checks); unused by --clean.")
    parser.add_argument("--keep-work-dir", action="store_true",
        help="Don't delete the scratch working directory on exit "
             "(useful for debugging a failed run)")
    parser.add_argument("--samples", action="store_true",
        help="Build the smaller samples tier instead of the standard tier. "
             "The selected spec supplies the reduced scan count and duration.")
    parser.add_argument("--clean", action="store_true",
        help="Remove this tier's generated output (each experiment's "
             "directory per the spec file's 'dir', plus checksums.sha256 "
             "and README.md) and exit, without generating anything. "
             "Combine with --samples to target the samples tier instead.")
    parser.add_argument("--validate", action="store_true",
        help="Validate the selected spec and referenced XML without generating. "
             "With --us-bin-dir, also validate rotor and centerpiece geometry.")
    args = parser.parse_args()

    try:
        spec_path = resolve_spec_path(args.spec)
    except FileNotFoundError as e:
        parser.error(str(e))
    load_spec(spec_path)
    print(f"spec: {spec_path.relative_to(TEST_DATA) if spec_path.is_relative_to(TEST_DATA) else spec_path} "
          f"(dataset_name={_SPEC_CONFIG['dataset_name']}, {len(EXPERIMENTS)} experiment(s))")

    if args.clean:
        target_dir = SAMPLES_DIR if args.samples else _GENERATED_DIR
        clean_target_dir(target_dir)
        return

    if args.validate:
        bin_dir = Path(args.us_bin_dir).resolve() if args.us_bin_dir else None
        ok = validate_config(bin_dir)
        sys.exit(0 if ok else 1)

    if not args.us_bin_dir:
        parser.error("--us-bin-dir is required (or set US_BIN_DIR)")
    bin_dir = Path(args.us_bin_dir).resolve()
    for tool in ("us_sim_inputs_gen", "us_astfem_sim", "us_mwl_species_sim"):
        if not (bin_dir / tool).exists():
            parser.error(f"{bin_dir / tool} not found in --us-bin-dir")
    for exp_id, entry in EXPERIMENTS.items():
        if not simparams_path(exp_id).exists():
            parser.error(f"{simparams_path(exp_id)} not found -- see config/README.md")
        for ch in entry["channels"]:
            for p in (model_path(ch), buffer_path(ch)):
                if not p.exists():
                    parser.error(f"{p} not found -- see config/README.md")

    target_dir = SAMPLES_DIR if args.samples else _GENERATED_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    # Rebuild metadata so renamed or removed experiments do not leave stale entries.
    for name in ("checksums.sha256", "README.md"):
        (target_dir / name).unlink(missing_ok=True)

    work_root = Path(tempfile.mkdtemp(prefix="synthetic-samples-" if args.samples else "synthetic-"))
    try:
        for exp_id in EXPERIMENTS:
            print(f"=== {exp_id} ({'samples' if args.samples else 'default'}) ===")
            build_experiment(bin_dir, exp_id, work_root, args.samples)
    finally:
        if args.keep_work_dir:
            print(f"Work directory kept at: {work_root}")
        else:
            shutil.rmtree(work_root, ignore_errors=True)

    write_readme(target_dir, args.samples)
    print(f"  -> {(target_dir / 'README.md').relative_to(TEST_DATA)}")


if __name__ == "__main__":
    main()
