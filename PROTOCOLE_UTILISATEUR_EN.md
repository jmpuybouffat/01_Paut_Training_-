# User test protocol — single-element manual scanning

SCALAR BACKSCATTER build. Purpose: check manual motion, limits, synchronized views and the reduced scattering model. These tests do not qualify an industrial UT examination. Start the new field with **Load backscatter witness test** in Manual scan; see also RETRODIFFUSION_SCALAIRE_FR_EN.md, which includes an English explanation.

## 1. Common setup

Before changing specimen settings, export recorded points with **Export JSON**. Changing settings outside the operator panel may rebuild it and clear the current scan session. Do not change specimen settings while scanning.

In the sidebar:

| Setting | Value |
|---|---|
| Language | EN |
| Use | Training |
| Training specimen | Main-wall scan demo for motion tests |
| Main pipe OD | 400 mm |
| Main pipe thickness | 20 mm |
| Nozzle OD | 160 mm |
| Nozzle thickness | 12 mm |
| Axis angle | 63° |
| Transverse offset | 0 mm |
| Main pipe length | 800 mm |
| External nozzle length | 320 mm |
| Bevel angle / root gap / root land | 35° / 2 mm / 2 mm |
| Nominal weld width / reinforcement | 14 mm / 3 mm |
| Material | Carbon steel |
| VL / VT / density | 5920 m/s / 3240 m/s / 7850 kg/m³ |

In **2 · Specimen setup**, select MWB 45° / 4 MHz. Start with Zone 1 set to **Unassessed**, without excluded zones. Unassessed allows geometric exploration here; it does not establish actual physical accessibility.

The disabled future-model selector is not an active comparison of elastic Green/Born/Kirchhoff/GTD engines. The new backscattered field uses a separate scalar Kirchhoff approximation.

In **3 · Manual scan**:
- Press STOP / Pause, then Reset.
- Field and rays: checked. Instructor: unchecked. Teaching flaw return: unchecked.
- Path: Free; Local skew: 0°.
- Surface: Nozzle 3D — move probe; Action: Move probe.
- Gate A: start 0 µs, end 80 µs, relative threshold 0.01; gain 3.
- For motion tests, select **Reflected field — first teaching model**, with a −30 dB display threshold. Test 9 uses the new computed backscattered field instead.

**3D mouse / Orbit** in the sidebar controls the specimen camera. **Path / Free** in Manual scan controls probe movement. **Custom specimen** defines specimen/flaw data, not a free-motion mode.

## 2. Three scan plans

Enter these values in **2 · Specimen setup → Geometric scan — main pipe**. Use Scan step 10 mm, Wedge geometric margin 2 mm and Beam heading from +Z 0° throughout.

| Plan | Start azimuth | End azimuth | Start Z | End Z | Purpose |
|---|---:|---:|---:|---:|---|
| A | −60° | −40° | −180 mm | −120 mm | Free motion, raster and boundaries away from branch |
| B | −60° | +60° | −300 mm | +300 mm | Nozzle contour and approach to its footprint exclusion |
| C | −50° | −30° | −100 mm | −60 mm | Controlled custom witness target |

Return to Manual scan after each change and press Reset. The initial contact point uses Start azimuth and Start Z. Az, Z and θ in the status line report the current pose; they are not editable fields.

## 3. Test 1 — free motion and probe orientation

Settings: plan A; Path Free; Local skew 0°; Action Move probe.

Grab the MWB symbol and move it into the working area. Press +1° five times and −1° five times. Try the wheel over the probe, then Rotate probe 180°.

Expected: Az/Z change while moving; θ changes while turning; beam, section, field and A-scan update together. The nominal MWB refracted angle remains 45°. θ is the heading in the local tangent plane, not the refracted angle.

If the probe is on the hidden side, choose Action → Rotate specimen, rotate the camera, then return to Move probe. Camera movement alone must not change Az/Z/θ.

## 4. Test 2 — raster completion, reverse and reset

Settings: plan A; Free; Reset.

Press Raster and let it reach the end. Press Reverse scan, then Raster again. Try STOP / Pause while moving. Restart and try Escape while the scan panel has focus. Finally press Reset.

Expected: no infinite raster loop; stop at the end; return in the opposite direction; immediate pause; reset to Az −60°, Z −180 mm, θ 0°, clearing recorded points and the stored maximum. Export before resetting if those data are needed.

## 5. Test 3 — plan boundaries

Settings: plan A; Free; choose Surface → Unwrapped surface — secondary aid to read the boundaries more easily.

Drag toward each of the four boundaries and try to cross it. Grab the probe again and move back inside.

Expected: entry point remains between −60° and −40°, with Z between −180 and −120 mm. Attempting to cross a boundary stops the drag and displays the plan-boundary reason. Returning inside remains possible. These plan limits apply to the entry point; they do not prove that the entire wedge lies inside the plan rectangle.

## 6. Test 4 — main pipe axis

Settings: plan B; Reset; Path → Main pipe axis; Local skew 0°.

Note Z. Press Path + ten times, then Path − ten times. Try dragging the probe vertically in the surface view.

Expected: circumferential motion at constant Z. Az changes. Local skew remains adjustable. Vertical dragging does not change Z in this mode.

## 7. Test 5 — nozzle axis and local skew

Settings: plan B; Reset; Path → Nozzle axis; Weld stand-off 35 mm; Local skew 0°.

Press Path + to approach the contour. Continue around it using successive clicks. Watch Az, Z and θ together. Try Path −. Set Local skew to +10°, back to 0°, then −10°.

Expected: both Az and Z vary around the branch; θ follows the direction toward the weld. Manual skew adds to that direction. Contact stays on the main pipe. A full contour is only possible within the plan and footprint limits.

Next try a 50 mm stand-off and press Path + to approach the new contour. This changes the radius of a coaxial envelope; it is not a constant geodesic distance from the weld. A blocked approach must stop without crossing an excluded region.

Raster playback is reserved for Free mode. Axis-following modes use dragging and Path ±.

## 8. Test 6 — nozzle/weld footprint stop

Settings: plan B; Reset; Free; Local skew 0°; Unwrapped surface.

From the initial position, move at Z near −300 mm toward Az near 0°, then increase Z gradually toward the branch.

Expected: the approximate wedge footprint stops before crossing the nozzle/weld exclusion, with an explanatory stop reason. Moving back in the opposite direction must remain possible. The footprint is a centred 24 × 14 mm rectangle plus 2 mm margin: it is not a full CAD collision or curved-contact validation.

## 9. Test 7 — deliberately excluded zone

Settings: plan A. Add the following row to the zone table in tab 2:

| Column | Value |
|---|---|
| Zone | Test exclusion |
| Access | Inaccessible |
| Reason | Witness obstacle |
| Start / end azimuth | −52° / −48° |
| Start / end Z | −160 / −140 mm |

Commit the final cell, return to Manual scan, select Free and Reset. Approach this zone manually or using Raster.

Expected: excluded-zone stop before the footprint crosses it. The symbol may stop before the red boundary because the wedge has finite dimensions and margin. Do not leave exclusion bounds empty: an inaccessible zone without bounds blocks the entire plan.

After testing, remove the row or restore Access → Unassessed. Check that no exclusion remains before the following tests.

## 10. Test 8 — witness target and legacy heuristic A-scan

This optional comparison test uses an artificial target away from the branch to distinguish a flaw response from root/cap geometry signals.

Choose Custom specimen, retain the common geometry and use plan C. In Indication library and placement:

| Setting | Value |
|---|---|
| MF1 enabled | Yes |
| MF1 length / width | 6 / 3 mm |
| MF1 azimuth | −50° |
| MF1 Z position | −90 mm |
| MF1 depth | 10 mm |
| MF1 orientation | 0° |
| MF1 normal tilt | 45° |
| MF2, INC1, FCT1, FCT2 enabled | No |

Fill all MF1 pose cells, initially empty in Custom specimen. Location is descriptive; numerical coordinates position the target. This position is not a real weld-face location.

In Manual scan: Free, Reset, Local skew 0°. Verify Az −50°, Z −100 mm, MWB 45° / 4 MHz. For this legacy comparison, select Reflected field — first teaching model, then enable Instructor. Gate A: 0–20 µs, relative threshold 0.01, gain 3.

Expected: MF1 echo near 8.7 µs at VT 3240 m/s in the heuristic model. Do not treat it as calibrated instrument data. Small translations and rotations should change the current response. The stored maximum deliberately retains a previous peak; use the current waveform to compare poses.

## 11. Test 9 — computed backscattered field

Export personal data first. In Manual scan, press **Load backscatter witness test — MWB 45° / 4 MHz**. This replaces specimen geometry, plan, zones and flaws with the witness case and selects Computed backscattered field — scalar.

Wait for calculation to finish and press Focus computed flaw. Gate A 0–20 µs, threshold 0.01, gain 3; field display cutoff −40 dB. Expected: finite pink reflecting surface, coloured scattered-field lobes and aperture-integrated reception. MF1 centre-path time is about 8.73 µs; relative amplitude is about 0.062 for this reduced model. The dB reference stays fixed across poses.

Try changing probe heading, then MF1 normal tilt from 45° to 80° in tab 2, then frequency from 4 to 5 MHz. Field and reception must change. While a new pose is computed, the previous field is hidden and Record point is disabled.

Gate 30–40 µs excludes MF1's direct echo but does not change the monochromatic field. Disabling MF1 removes its response. Root/cap geometry signals are not mixed into this scalar A-scan.

This model computes phase-coherent scalar scattering on a finite surface, including transmitting and receiving apertures. **Full elastic scattering and wall-bounce scattering are not implemented.** See RETRODIFFUSION_SCALAIRE_FR_EN.md for formulas, settings and limits. The old magenta return remains an illustrative path in the legacy teaching mode.

## 12. Test 10 — section, field and camera controls

Settings: witness target, plan C, Free; Reset.

Drag horizontally by a few pixels in the section, then use its wheel. Repeat in the field map and observe the shared pose, field and A-scan. Select View → Nozzle 3D + rays, drag and zoom.

Expected: section and field control the same probe; wireframe 3D dragging/zoom controls the camera without moving the probe. The legacy Z/depth projection can compress circumferential paths; use 3D to interpret them. In scalar mode, the section passes through the selected flaw.

Switch Field to Computed cut or Computed 3D volume, if available. These show the direct scalar Green field, not the scattered field. Restoring the backscattered mode restores aperture-integrated scalar flaw responses. Switching field models also changes the signal model: do not compare a stored heuristic amplitude with a computed scalar amplitude as if they were calibrated measurements.

## 13. Test 11 — recording, export and language

At a response, press Record point; turn +1°, wait for the current calculation if active, then record again. Check the counter and Export JSON. Export VR scene for Fabien to evaluate poses, stop events and the scalar field data.

Export before changing language. Switch to FR and check titles, controls, types, table headings, the test protocol and coordinates. Dimensions and flaw data must persist. The scan panel may be rebuilt; its trace is not guaranteed to survive the language change. Return to EN and check that this English protocol is loaded.

Report untranslated labels separately from any change to numerical data.

## 14. Test 12 — separation from real examination

Export the scan, then choose Real examination preparation under Use. No acquisition instrument is connected.

Expected: no synthetic signal presented as real acquisition, and no synthetic flaw field/return. Restore Training for teaching tests.

## User feedback sheet

For each test: test number; passed / issue / not tried; plan A/B/C; probe; path mode; Az/Z/θ; observed result; stop reason; useful screenshot; build SCALAR BACKSCATTER.

Evaluate the reduced computed scalar field separately from the remaining need for full elastic scattering with wall bounces. An illustrative magenta path alone validates neither calculation. Industrial examination qualification remains outside this protocol.
