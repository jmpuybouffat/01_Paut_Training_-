# BYTE NDT — Welded plate P01 🇬🇧

1. Extract the entire ZIP.
2. Open **OUVRIR_APPLICATION.html** in Chrome or Edge. No installation or Internet connection is required.
3. Choose a language and SE, MWB or PA. Use **Witness pose**, then **Calculate** to record a response.
4. Click in the X–Y plan or edit X/Y/heading to scan freely. The wedge footprint includes a clearance margin. Leaving the plate or touching a weld cap suspends acquisition.
5. Raster scanning uses 2 mm X increments and configurable Y indexing. Stop, reset and reverse-heading controls are available. Examine from both weld sides.
6. Exam preparation hides flaw truth and witness poses. Fill in operator, procedure and report, then export. This local exercise is not a secure or officially approved certification examination.

The initial calculation is not recorded. Each Calculate, plan click or raster pose adds a record. Switching languages preserves acquisitions. Switching training/exam modes clears acquisitions.

## Included

245 × 250 × 10 mm plate CAD; symmetric 45° double-V, caps and HAZ; five proposed flaws; dual-crystal SE, MWB 45/60/70° and 32-element 5 MHz PA; 35–70° sector; synthetic A-scan envelope, Y–Z axis section, scalar incident/scattered field, backprojected S-scan, scan-sequence B-scan and accumulated 3D responses. The B-scan uses the first sector ray; all sector rays are retained in exported records.

Nominal carbon steel type A42: VL 5,920 m/s, VT 3,240 m/s, density 7,850 kg/m³. Base plate, weld and HAZ initially share these values: no artificial HAZ-interface echoes. E7018 is an illustrative filler family, not a qualified welding procedure.

Selected PA concept: Imasonic, 32 elements, 5 MHz, 0.5 mm pitch, 12 mm elevation; provisional element width 0.45 mm and 30 mm acoustic-path focus in steel. Nominal wedge refracted angle 55° shear in steel. Exact wedge geometry/reference remain unavailable: calculations start at the steel interface. SE/MWB apertures and mechanical footprints are demonstration values.

## Reading the views

A-scan: synthetic envelope, relative amplitude, fixed 0–1 vertical scale after gain. Reduce gain for off-scale peaks; increase gain to explore weak responses. S-scan/map colours are dB relative to the model reference, not a calibrated regulatory reference.

Incident field is dB relative to the scalar propagator unit; contours show scattering from the strongest reflector, not all reflectors combined. These are not calibrated pressure maps. Displayed flaw positions are scenario truth. S-scan and 3D accumulation are time-angle backprojections with path ambiguities, not exact flaw reconstructions.

## Limits

Central-frequency scalar model, finite aperture, planar surface physical optics and weak-volume Born inclusions. One opposite-face image per transmit/receive path; synthetic pulse envelopes rather than a full broadband solver. No wedge propagation, mode conversion, GTD, cap scattering or full elastic calculation. Received backwall echoes are included for SE/MWB, not PA in P01.

An instructor must validate scenarios, coverage, sensitivity settings and certification requirements. This release supports review of gestures and displays; it does not establish detection performance or acceptance criteria.

## Fabien: camera-based interface, no headset

**FABIEN_CAMERA** contains the data contract and an example calibrated pose. Video detection and image-to-plate calibration must be connected to Fabien’s system; they are not implemented here. The camera panel tests already-calibrated JSON poses. Students do not need programming skills.
