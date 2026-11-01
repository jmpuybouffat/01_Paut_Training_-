"""Analytical cylindrical intersections and illustrative joint preparation (mm)."""
import numpy as np


def validate_dimensions(D, t, d, tn, offset, land):
    errors = []
    if 2*t >= D: errors.append(('Épaisseur principale excessive', 'Main thickness exceeds radius'))
    if 2*tn >= d: errors.append(('Épaisseur nozzle excessive', 'Nozzle thickness exceeds radius'))
    if abs(offset)+d/2 >= D/2-t:
        errors.append(('Le nozzle doit rester dans l’enveloppe intérieure pour une racine fermée', 'Nozzle must fit inside the inner envelope for a closed root'))
    if land > t: errors.append(('Le talon dépasse l’épaisseur principale', 'Land exceeds main thickness'))
    return errors


def preparation(theta, root_radius, outer_radius, nozzle_radius, offset, axis, basis, lateral, bevel, gap, land, reinforcement):
    """Radial bevel approximation: axial nozzle cylinder vs radial main preparation.

    Gap and land measured radially from the nozzle OD; bevel angle measured
    from the radial direction of the main pipe. Not an exact solid Boolean.
    """
    depth = np.linspace(0., outer_radius-root_radius, 35)
    spread = gap + np.maximum(depth-land, 0.)*np.tan(np.deg2rad(bevel))
    radii = nozzle_radius+spread[:, None]
    directions = np.cos(theta)[None,:,None]*basis+np.sin(theta)[None,:,None]*lateral
    q = np.array([0.,offset,0.])+radii[...,None]*directions
    A = axis[0]**2+axis[1]**2
    B = 2*(q[...,0]*axis[0]+q[...,1]*axis[1])
    C = q[...,0]**2+q[...,1]**2-(root_radius+depth[:,None])**2
    disc = B*B-4*A*C
    s = (-B+np.sqrt(np.maximum(disc,0.)))/(2*A)
    face = q+s[...,None]*axis
    face[disc<0] = np.nan
    # Illustrative weld cap spanning nozzle OD to prepared outer edge.
    f = np.linspace(0.,1.,16)[:,None]
    cap_r = nozzle_radius+f*spread[-1]
    cap_q = np.array([0.,offset,0.])+cap_r[...,None]*directions
    cap_target = outer_radius+reinforcement*np.sin(np.pi*f)
    B = 2*(cap_q[...,0]*axis[0]+cap_q[...,1]*axis[1])
    C = cap_q[...,0]**2+cap_q[...,1]**2-cap_target**2
    disc = B*B-4*A*C
    s = (-B+np.sqrt(np.maximum(disc,0.)))/(2*A)
    cap = cap_q+s[...,None]*axis
    cap[disc<0] = np.nan
    return face, cap
