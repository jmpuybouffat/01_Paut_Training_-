"""Conservative footprint check; never an acoustic coverage certification."""
import math

def scan_status(zone):
    access=zone.get('access','UNASSESSED')
    if access=='INACCESSIBLE': return 'INACCESSIBLE'
    if access!='TO_ASSESS': return 'UNASSESSED'
    try:
        al,aw,pl,pw,tr,margin=[float(zone[k]) for k in ('available_length_mm','available_width_mm','probe_length_mm','probe_width_mm','travel_mm','margin_mm')]
        if not all(map(math.isfinite,(al,aw,pl,pw,tr,margin))) or min(al,aw,pl,pw)<=0 or min(tr,margin)<0:
            return 'UNASSESSED'
    except (KeyError,ValueError,TypeError): return 'UNASSESSED'
    return 'FOOTPRINT_FITS_ONLY' if pl+tr+2*margin<=al and pw+2*margin<=aw else 'INSUFFICIENT_CLEARANCE'
