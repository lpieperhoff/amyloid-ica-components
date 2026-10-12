# Components

Other amyloid-β PET components derived by probabilistic independent component analysis (ICA) in the AMYPAD Prognostic & Natural History Study. All maps are in MNI152NLin6Asym space at 2 mm resolution.

## File types

Each component is provided in three versions:

- `desc-probmap`: component probability map (Mixture Modeling, FSL MELODIC)
- `desc-zstat`: unthresholded Z-statistic map
- `desc-zstatmasked`: Z-statistic map thresholded at 80% component probability; used by `apply_components.py`

## Commissural component

<img src="../assets/component-commissural.png" alt="Commissural amyloid component" width="100%">

Files:

- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-commissural_desc-probmap_probseg.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-commissural_desc-zstat_statmap.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-commissural_desc-zstatmasked_statmap.nii.gz`

## Halo component

<img src="../assets/component-halo.png" alt="Halo amyloid component" width="100%">

Files:

- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-halo_desc-probmap_probseg.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-halo_desc-zstat_statmap.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-halo_desc-zstatmasked_statmap.nii.gz`

## Left-temporal component

<img src="../assets/component-lhtemporal.png" alt="Left-temporal amyloid component" width="100%">

Files:

- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-lhtemporal_desc-probmap_probseg.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-lhtemporal_desc-zstat_statmap.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-lhtemporal_desc-zstatmasked_statmap.nii.gz`

## Projection component

<img src="../assets/component-projection.png" alt="Projection amyloid component" width="100%">

Files:

- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-projection_desc-probmap_probseg.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-projection_desc-zstat_statmap.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-projection_desc-zstatmasked_statmap.nii.gz`

## Right-temporal component

<img src="../assets/component-rhtemporal.png" alt="Right-temporal amyloid component" width="100%">

Files:

- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-rhtemporal_desc-probmap_probseg.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-rhtemporal_desc-zstat_statmap.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-rhtemporal_desc-zstatmasked_statmap.nii.gz`

## Ventricular component

<img src="../assets/component-ventricular.png" alt="Ventricular amyloid component" width="100%">

Files:

- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-ventricular_desc-probmap_probseg.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-ventricular_desc-zstat_statmap.nii.gz`
- `atlas-AmyloidICA_space-MNI152NLin6Asym_res-2_label-ventricular_desc-zstatmasked_statmap.nii.gz`

## Usage

To quantify these components in a new PET scan, see `apply_components.py` and the instructions in the main [README](../../README.md). Please cite: _TO BE UPDATED_.