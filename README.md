# Amyloid-β ICA components

Cortical amyloid-β PET components (frontal, occipital, parietal) derived by probabilistic ICA in AMYPAD and A4-LEARN, with code to quantify them in new PET data.

Citation: <Brain paper reference + DOI; Zenodo DOI for this repo>

## Contents
- components/ : component maps in MNI152NLin6Asym, 2 mm. For each component: probmap (mixture-modeling derived probability of a voxel's component belonging), zstat, zstatmasked
- melodic/ : original outputs from 'melodic'
- apply_components.py : registers T1 and PET to MNI and spatially regresses the zstatmasked maps onto the PET

## Installation
pip install -r requirements.txt

## Usage
python apply_components.py --subject sub-001 --t1 sub-001_T1w.nii.gz --pet sub-001_pet-suvr.nii.gz --output sub-001_components.csv

Batch: add --append and a shared --output to build one CSV across subjects.

Input requirements: subject-space T1 and PET (.nii.gz); PET should be SUVR with <reference region>; 3D (4D is averaged).

## Output
CSV columns: subject, intercept, beta_frontal, beta_occipital, beta_parietal, n_voxels

## Method summary
Registration steps, regression design and mask (2-4 sentences).

## File naming
Explain the naming convention.

## License and citation