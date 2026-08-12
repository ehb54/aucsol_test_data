# Configuration

The generator combines four independent configuration layers. A **spec** is the
assembly plan: it selects the model, buffer, and simulation parameters used for
each experiment.

```text
spec
├── experiment → simparams + rotor
└── channels   → model + buffer + output options
                         │
                         ▼
                 UltraScan simulators
                         │
                         ▼
              one archive per experiment
```

## Configuration layers

| Layer | Scope | Defines |
|---|---|---|
| [`specs/<name>.json`](specs/) | Dataset | Output name, experiments, channels, and input mappings |
| [`models/<name>/model.xml`](models/) | Channel | Substance properties such as molecular weight, `vbar20`, and `f_f0` |
| [`buffers/<name>/buffer.xml`](buffers/) | Channel | Solution density, viscosity, and pH |
| `simparams/<name>/simparams.xml` | Experiment | Speed, duration, scan count, geometry, noise, and solver settings |

Models, buffers, and simulation parameters are reusable. Their directory names
are stable identifiers referenced by a spec; they are not intrinsically tied to
a dataset or scan type.

## How a spec assembles an experiment

Each experiment represents one physical rotor run and produces one zip. Its
`simparams` and `rotor` apply to every channel. Each channel independently
selects a model and buffer and defines how its simulated output is packaged.

```json
{
  "id": "netrin1-ra",
  "dir": "ra",
  "simparams": "default",
  "rotor": "1",
  "description": "Netrin1 (protein, globular)",
  "channels": [
    {
      "channel": "1A",
      "model": "netrin1",
      "buffer": "tris-200mm-nacl",
      "data_type": "RA"
    }
  ]
}
```

This resolves to:

| Spec value | Input or output |
|---|---|
| `simparams: "default"` | `config/simparams/default/simparams.xml` |
| `model: "netrin1"` | `config/models/netrin1/model.xml` |
| `buffer: "tris-200mm-nacl"` | `config/buffers/tris-200mm-nacl/buffer.xml` |
| `dir: "ra"` | `datasets/generated/<dataset_name>/ra/` |
| `id: "netrin1-ra"` | `netrin1-ra_synthetic.zip` |

For multi-channel experiments, the generator simulates each channel separately
and packages all channel outputs in the experiment's single archive.

## Reuse and overrides

- Multiple channels or experiments can reference the same model, buffer, or
  simulation-parameter directory.
- A channel can reuse a model with a different buffer, or a buffer with a
  different model.
- Noise, baseline, and signal can be set for an individual channel in the spec.
  The generator applies them to temporary copies of the selected XML files, so
  the files under `config/` remain unchanged.
- `data_type` controls the `.auc` tag. `RI/IP` simulates once and packages both
  relabeled forms.
- `wavelengths` selects multi-wavelength simulation and requires `mwl_run_id`.
  The generator derives temporary per-wavelength models from the selected model.

The `--samples` option uses the same chemistry and geometry. It only reduces
scan count and duration according to `sample_defaults` and any experiment-level
`samples` override in the spec.

## Geometry must agree

`centerpiece` is a **zero-based list index** into UltraScan's
`etc/abstractCenterpieces.xml`, not the XML `id`. `centerpiece_channel` is the
zero-based radial row within that centerpiece. Channels sharing one physical
sample/reference pair use the same values.

The selected row's bottom must match the experiment's `simparams.xml`. Validate
against the same UltraScan installation used for generation:

```bash
python3 scripts/generate_synthetic_data.py \
  --validate \
  --us-bin-dir /path/to/ultrascan/bin
```

Passing the executable directory enables checks against its associated
centerpiece and rotor reference files.

## Specs and output directories

[`base.json`](specs/base.json) is the default dataset spec.
[`examples.json`](specs/examples.json) contains worked schema examples. Select
another spec by name or path:

```bash
python3 scripts/generate_synthetic_data.py \
  --spec examples \
  --us-bin-dir /path/to/ultrascan/bin
```

The spec's `dataset_name` sets the output directory:
`datasets/generated/<dataset_name>/`. See the `_comment` block in
[`base.json`](specs/base.json) for the complete field reference.

## Add or change configuration

1. Reuse existing model, buffer, and simulation parameters where possible.
2. Add a new XML definition only when the required physics or run conditions
   differ.
3. Add or update the experiment and channel mappings in a spec.
4. Run `--validate` with the target UltraScan executable directory.
5. Regenerate the affected standard and samples datasets.

See [Models](models/README.md) and [Buffers](buffers/README.md) for values,
references, assumptions, and XML-generation commands.
