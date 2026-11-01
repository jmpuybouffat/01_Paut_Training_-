# BYTE NDT — nozzle operator guide

## Start and choose the specimen

On Windows, extract the complete package and double-click LANCER_NOZZLE.bat. Keep the console open. Use the four tabs: 1 Nozzle 3D, 2 Specimen setup, 3 Manual scan, 4 User guide.

Choose **Training** and **Main-wall scan demo** for the ready-to-scan exercise. Five artificial targets are placed in the main wall. These are motion-training targets, not real weld-face locations. Choose **Custom specimen** to enter your own indication positions.

## Nozzle and probe setup

In the sidebar, set pipe diameters, thicknesses, angle, offset and lengths. Set bevel, gap, land and reinforcement. The geometry is approximate and is not a validated welded CAD solid.

In tab 2, select the single-element Krautkrämer MWB: 45°, 60° or 70°, at 2, 4 or 5 MHz. The current case defaults to 45° / 4 MHz. The supplied catalogue confirms the 2 MHz table, 8 × 9 mm aperture and N = 15 mm; do not reuse that near-field value as a verified 4/5 MHz specification.

## Access and scan limits

Define angular and Z bounds, available space, actual wedge footprint, travel and margins. Select **Assess footprint** to run the dimensional comparison. Record inaccessible zones and their reasons. An exclusion without valid bounds blocks motion. Unassessed means geometric exploration only, never verified access or full acoustic coverage.

Manual motion and raster playback use the same limits: entry-point bounds, pipe ends, excluded regions and an approximate centered wedge rectangle. The default body envelope is 24 × 14 mm plus the configured margin. Actual emergence-point offset, curved contact and complete CAD collision remain unverified.

The probe stops at its last admitted pose. Read the displayed stop reason. Use **Reverse scan** to return, or **Reset** to restart. **STOP/Pause**, **Space** or **Escape** stops motion in the active operator panel. Raster playback stops at the end of the plan and does not loop automatically. A probe rotation is rejected if the envelope would enter a blocked region.

## Indications

The project registry contains two lack-of-fusion indications (6 × 3 mm), an inclusion (2 mm diameter), and two thermal-shock cracks (4 × 2 mm). Dimensions and enabled state are editable. In Custom specimen, enter azimuth, longitudinal Z, radial depth from the outer surface and local orientation from +Z. Empty position fields are exported as undefined and produce no flaw response. Automatic placement on real bevel faces is not implemented.

## Blind manual scan

Open tab 3. Keep **Instructor** unchecked and **Field and rays** checked. Grab the MWB symbol on the 3D surface with the left mouse button and drag in a raster. **Raster** plays the configured path; **STOP/Pause** returns control to the operator. To rotate the specimen rather than move the probe, choose **Rotate specimen**. The unwrapped surface is a secondary aid.

Watch the A-scan while scanning. At a response, stop translation and adjust heading using ±1° or the wheel over the probe. **Rotate probe 180°** changes probe orientation; **Reverse scan** changes only playback direction.

Use A/B/C gates, time bounds in microseconds and the relative threshold. Record several samples around a response. The −6 dB result is the extent of sampled positions, not a certified flaw size. Grey skip markers are path references, not automatic echoes. Root/cap and flaw amplitudes are heuristic; specular wall pulses require a traced return to the receiver.

## Field display

**Reflected field — first teaching model** restores the coloured 0 to −40 dB map from the original twin. Its spreading, attenuation and reflection weights are illustrative. It follows the same probe pose and geometric ray paths as the section and 3D views.

**Computed 3D volume** and **Computed cut** use a harmonic scalar Green integral over a finite equivalent rectangular aperture. Phase and frequency are included, but only the direct homogeneous field is calculated. The wedge, elastic polarization, transmission, mode conversion and full weld propagation are not modeled. The A-scan is not physically derived from this field. This is not a validated CIVA solver. Born/Kirchhoff/GTD remain inactive future models.

## Faceted profiles and microstructure

Root/cap training profiles are repeatable faceted surfaces, controlled by irregularity, facet count and profile identifier. They are not measured weld profiles. Geometry responses include a heuristic incidence weight, not a complete reflection solution on these meshes.

Grain morphology, nominal size and preferred orientation are descriptive metadata only. They do not yet change propagation, attenuation or grain scattering.

## Save and share

Export the specimen configuration in tab 2 and the manual scan from the operator panel before reloading or changing Streamlit settings. Manual trajectories are held in the browser component and are not retained across reloads. **Export VR scene** provides the common coordinate system, probe poses, geometry and motion-stop events. Authoring exports include target reference data; they are not secure blind-exam files.

Use **Instructor** only to reveal the answers for explanation. **Real examination preparation** has no connected acquisition and does not show synthetic signals as real measurements. Localized labels do not change the canonical data keys used by the simulator and exported files.
