#!/usr/bin/env python3
"""
Register a subject's T1 and PET to MNI152NLin6Asym (2 mm) and spatially
regress the masked z-stat component maps onto the MNI-space PET image.

Pipeline:
  1. T1 -> MNI template (ANTs SyN, affine + nonlinear)
  2. PET -> T1 (ANTs rigid)
  3. PET -> MNI by composing both transforms in a single resampling step
  4. OLS regression of PET voxel values on all component maps simultaneously
     (with intercept), within a mask; coefficients written to CSV
"""
import argparse
import re
import sys
from pathlib import Path

import ants
import numpy as np
import pandas as pd

REPO_DIR = Path(__file__).resolve().parent
SPACE = "space-MNI152NLin6Asym_res-2"


def get_template(template_path=None):
    if template_path:
        return ants.image_read(str(template_path))
    from templateflow import api as tflow
    f = tflow.get("MNI152NLin6Asym", resolution=2, desc=None,
                  suffix="T1w", extension="nii.gz")
    if isinstance(f, (list, tuple)):
        f = f[0]
    return ants.image_read(str(f))


def load_components(components_dir, template):
    files = sorted(Path(components_dir).glob("*zstatmasked*.nii.gz"))
    if not files:
        sys.exit(f"No *zstatmasked*.nii.gz files found in {components_dir}")
    comps = {}
    for f in files:
        m = re.search(r"(?:component|label)-([A-Za-z0-9]+)", f.name)
        name = m.group(1) if m else f.name.split(".")[0]
        img = ants.image_read(str(f))
        if not ants.image_physical_space_consistency(img, template):
            sys.exit(f"{f.name} is not on the same 2 mm MNI152NLin6Asym grid "
                     "as the template.")
        comps[name] = img
    return comps


def estimate_transforms(t1, pet, template, prefix):
    """Return (T1->MNI transform list, PET->T1 transform list)."""
    t1_to_mni = ants.registration(
        fixed=template, moving=t1, type_of_transform="SyN",
        outprefix=f"{prefix}_t1-to-mni_")
    pet_to_t1 = ants.registration(
        fixed=t1, moving=pet, type_of_transform="Rigid",
        aff_metric="mattes", outprefix=f"{prefix}_pet-to-t1_")
    return t1_to_mni["fwdtransforms"], pet_to_t1["fwdtransforms"]


def to_mni(img, template, transforms):
    # ANTs applies the transform list last-to-first
    return ants.apply_transforms(fixed=template, moving=img,
                                 transformlist=transforms,
                                 interpolator="linear")


def spatial_regression(pet_mni, comps, mask_img=None):
    names = list(comps)
    maps = np.stack([comps[n].numpy() for n in names], axis=-1)
    y = pet_mni.numpy()

    if mask_img is not None:
        mask = mask_img.numpy() > 0
    else:
        mask = np.any(maps != 0, axis=-1)   # union of component maps
    mask &= np.isfinite(y) & (y != 0)

    X = np.column_stack([np.ones(mask.sum()), maps[mask]])
    beta, *_ = np.linalg.lstsq(X, y[mask], rcond=None)

    out = {"intercept": beta[0]}
    out.update({f"beta_{n}": b for n, b in zip(names, beta[1:])})
    out["n_voxels"] = int(mask.sum())
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--subject", required=True, help="Subject name/ID")
    p.add_argument("--t1", required=True, help="Subject-space T1 (.nii.gz)")
    p.add_argument("--pet", required=True,
                   help="Subject-space PET (.nii.gz); 4D input is time-averaged")
    p.add_argument("--output-dir", default=".",
                   help="Directory for all outputs (default: current directory)")
    p.add_argument("--output", default=None,
                   help="CSV filename, relative to --output-dir (an absolute path "
                        "overrides it). Default: <subject>_desc-components_betas.csv")
    p.add_argument("--append", action="store_true",
                   help="Append a row to an existing CSV (for batch runs)")
    p.add_argument("--save-mni", action="store_true",
                   help="Also save the MNI-space PET and T1 images")
    p.add_argument("--components-dir", default=REPO_DIR / "components")
    p.add_argument("--template", default=None,
                   help="MNI152NLin6Asym 2 mm T1w template; "
                        "default: fetched via TemplateFlow")
    p.add_argument("--mask", default=None,
                   help="Optional mask in MNI space; default: union of components")
    args = p.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    xfm_dir = out_dir / "transforms"
    xfm_dir.mkdir(exist_ok=True)

    csv_name = args.output or f"{args.subject}_desc-components_betas.csv"
    out_csv = out_dir / csv_name          # absolute csv_name overrides out_dir
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    template = get_template(args.template)
    comps = load_components(args.components_dir, template)

    t1 = ants.image_read(args.t1)
    pet = ants.image_read(args.pet)
    if pet.dimension == 4:
        print("4D PET detected: averaging over time.")
        pet = ants.get_average_of_timeseries(pet)

    t1_xfms, pet_xfms = estimate_transforms(
        t1, pet, template, str(xfm_dir / args.subject))

    pet_mni = to_mni(pet, template, t1_xfms + pet_xfms)

    if args.save_mni:
        t1_mni = to_mni(t1, template, t1_xfms)
        pet_out = out_dir / f"{args.subject}_{SPACE}_pet.nii.gz"
        t1_out = out_dir / f"{args.subject}_{SPACE}_T1w.nii.gz"
        ants.image_write(pet_mni, str(pet_out))
        ants.image_write(t1_mni, str(t1_out))
        print(f"Saved {pet_out}\nSaved {t1_out}")

    mask_img = ants.image_read(args.mask) if args.mask else None
    res = spatial_regression(pet_mni, comps, mask_img)

    row = pd.DataFrame([{"subject": args.subject, **res}])
    if args.append and out_csv.exists():
        row.to_csv(out_csv, mode="a", header=False, index=False)
    else:
        row.to_csv(out_csv, index=False)
    print(f"Saved {out_csv}")
    print(row.to_string(index=False))


if __name__ == "__main__":
    main()