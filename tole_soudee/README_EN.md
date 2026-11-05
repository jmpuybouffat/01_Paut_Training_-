# Reference CAD — double-V welded plate

## Open the files

- **CAD_TOLE_X_FR_EN.html**: standalone browser viewer; extract the ZIP and open this file. No Python or server required. 🇫🇷/🇬🇧 buttons, 3D model, nominal Y–Z section, weld focus and region/flaw visibility controls.
- **TOLE_X_245_250_10_ASSEMBLAGE.step**: detailed named assembly for Fusion, including curved reinforcement grooves.
- **WELDED_PLATE_X_245_250_10_ASSEMBLY_EN.step**: the same assembly with English component names.
- **TOLE_X_ENVELOPPE_LISSE.step**: lighter smooth-envelope model.
- **INDICATIONS_REFERENCES_NON_COUPANTES.step**: separate teaching references: two lack-of-fusion faces, two spheres and a sawtooth crack face. No arbitrary air-gap opening is cut into the metal.
- **PIECES/**: separate STEP files for the nine solid regions.
- **variations_indications.csv**: canonical numeric initial-parameter table.
- **variations_domaines.csv**: nominal parameters and empty variation bounds to define before generating variants.
- **table_indications_FR.csv / table_indications_EN.csv**: human-readable French/English tables.
- **geometrie_pour_rv.json**: mesh triangles, labels, colours and coordinates in mm for graphics/VR integration; no acoustic simulation is included.
- **SOURCE/**: generator, parameters and geometry checks.

## Agreed geometry

Plate 245 × 250 × 10 mm. Longitudinal X, transverse Y, upward Z; origin at a corner on the nominal bottom face. Weld centreline Y = 125 mm. Four straight 45° bevel faces, 1.25 mm central land and 1 mm preparation gap. Land may vary from 1 to 1.5 mm.

Each V is 4.375 mm deep, with a 9.75 mm opening at the plate surface. Land extends from Z = 4.375 to 5.625 mm. The preparation gap is filled by weld metal in the welded model.

Top and bottom reinforcements: 18 mm width, 2.5 mm maximum height, nominal circular radius 17.45 mm. Toes Y = 116 and 134 mm; top maximum Z = 12.5 mm, bottom minimum Z = −2.5 mm.

HAZ regions are 10 mm bands beyond the toes: Y = 106–116 and 134–144 mm. They are geometric regions; different acoustic properties have not been assigned.

Nine solids partition the material without volume overlap: outer plate, HAZ and weld-side plate region on each side, weld metal and two reinforcements. Shared interfaces do not represent air gaps.

## Proposed details requiring review

Illustrative grooves: pitch 3 mm, width 0.12 mm, maximum depth 0.08 mm, arc bow 1 mm. These are not measured surface parameters. Each reinforcement contains 81 shallow curved CAD grooves below the nominal circular envelope.

MF1/MF2 use lengths 2/4 mm and provisional in-plane width 0.5 mm; the reference faces lie on the actual bevels. Normal air opening is undefined. INC1/INC2 use diameter 0.5 mm and proposed HAZ positions. FIS1 is a proposed sawtooth reference face, 2 mm long and 0.5 mm overall transverse extent.

These positions/orientations are proposed teaching examples, not measured or approved flaw locations. Reference faces remain separate from the physical assembly. The meaning of the 0.5 mm width and crack/air opening must be confirmed before final acoustic representation.

## Orientation and next stage

Angles in degrees, R = Rz × Ry × Rx; local reference face lies in XY with normal +Z. Piece, references and VR meshes share the same frame.

Planned acquisition: dual-crystal SE 0°, MWB 45/60/70°, then 32-element 5 MHz 1D PA with 35–70° sector. S-scan lies in Y–Z, movement and accumulated sections follow X, initial spatial step 2 mm. Angular step is a separate pending parameter.

**This delivery is CAD and its viewer, not the ultrasonic operator application, PA focal laws or computed beam fields.** Material, acoustic properties and exact probe/wedge references remain pending.

## Regenerate

Development team: install requirements-cad.txt, edit parameters.json, run `python cad_model.py` then `python make_viewer.py`. The generator is parametric; STEP exchange does not create a native Fusion parametric timeline.

Geometry checks include solid validity, non-overlapping volume partition, analytic profile and STEP re-import. See BILAN_CONTROLES_FR_EN.md.
