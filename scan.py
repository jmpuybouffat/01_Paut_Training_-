"""Geometric scan planning on the main cylinder. No acoustic solver."""
import math
import numpy as np
from scan_access import scan_status


def angular_contains(angle, start, end):
    if abs(end-start)>=360: return True
    return (angle-start)%360 <= (end-start)%360+1e-9


def plan_scan(radius, length, angle_start, angle_end, z_start, z_end, step_mm, zones):
    values=[radius,length,angle_start,angle_end,z_start,z_end,step_mm]
    if not all(math.isfinite(v) for v in values) or radius<=0 or step_mm<=0 or length<=0:
        raise ValueError('Invalid scan dimensions')
    if max(abs(z_start),abs(z_end))>length/2 or abs(angle_end-angle_start)>360:
        raise ValueError('Scan outside pipe bounds')
    na=max(1,int(math.ceil(abs(math.radians(angle_end-angle_start))*radius/step_mm)))
    nz=max(1,int(math.ceil(abs(z_end-z_start)/step_mm)))
    if (na+1)*(nz+1)>20000: raise ValueError('Scan exceeds 20000 points; increase step')
    angles=np.linspace(angle_start,angle_end,na+1) if angle_start!=angle_end else [angle_start]
    zs=np.linspace(z_start,z_end,nz+1) if z_start!=z_end else [z_start]
    records=[]
    for j,z in enumerate(zs):
        for angle in (angles if j%2==0 else angles[::-1]):
            matches=[]; unknown_block=False
            for zone in zones:
                status=scan_status(zone)
                keys=('azimuth_start_deg','azimuth_end_deg','z_start_mm','z_end_mm')
                try:
                    a,b,lo,hi=[float(zone[k]) for k in keys]
                    if not all(math.isfinite(v) for v in (a,b,lo,hi)) or lo>hi: raise ValueError()
                except (KeyError,TypeError,ValueError):
                    if status in ('INACCESSIBLE','INSUFFICIENT_CLEARANCE'): unknown_block=True
                    continue
                if angular_contains(angle,a,b) and lo<=z<=hi: matches.append(status)
            if unknown_block or any(s in ('INACCESSIBLE','INSUFFICIENT_CLEARANCE') for s in matches): state='BLOCKED'
            elif matches and all(s=='FOOTPRINT_FITS_ONLY' for s in matches): state='PLANNED'
            else: state='UNASSESSED'
            th=math.radians(angle)
            records.append(dict(index=len(records),azimuth_deg=float(angle),z_mm=float(z),X_mm=radius*math.cos(th),Y_mm=radius*math.sin(th),Z_mm=float(z),status=state))
    return records


def beam_segment(point, radius, thickness, refracted_deg, heading_deg):
    """First straight leg ending at inner cylinder or axial tangent limit."""
    th=math.atan2(point[1],point[0]); normal=np.array([math.cos(th),math.sin(th),0.])
    tangent=np.array([-math.sin(th),math.cos(th),0.]); axial=np.array([0.,0.,1.])
    beta=math.radians(refracted_deg); heading=math.radians(heading_deg)
    direction=-math.cos(beta)*normal+math.sin(beta)*(math.cos(heading)*axial+math.sin(heading)*tangent)
    p=np.array(point); A=float(direction[:2]@direction[:2]); B=2*float(p[:2]@direction[:2]); C=radius**2-(radius-thickness)**2
    disc=B*B-4*A*C
    if disc<0: return None
    distance=(-B-math.sqrt(disc))/(2*A)
    return p+distance*direction
