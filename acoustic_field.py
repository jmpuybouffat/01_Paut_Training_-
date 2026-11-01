"""Scalar equivalent aperture field, not an elastic or CIVA solver.

Uniform rectangular source in a homogeneous medium, harmonic scalar Green
kernel exp(ikr)/(4*pi*r). Source plane is normal to the equivalent beam axis.
No wedge, refraction, elastic polarization, reflections, mode conversion or
flaw scattering is represented by this module.
"""
import numpy as np


def scalar_aperture_cut(frequency_mhz, speed_m_s, width_mm=8., height_mm=9.,
                        s_max_mm=90., transverse_max_mm=18., ns=150, nt=73, include_volume=False):
    values=[frequency_mhz,speed_m_s,width_mm,height_mm,s_max_mm,transverse_max_mm]
    if not np.isfinite(values).all() or min(values)<=0 or ns<2 or nt<3:
        raise ValueError('Positive finite source and field parameters required')
    wavelength=speed_m_s/(frequency_mhz*1000.)
    # Midpoint quadrature with source spacing <= lambda/3.
    nx=max(8,int(np.ceil(width_mm/(wavelength/3))))
    ny=max(8,int(np.ceil(height_mm/(wavelength/3))))
    if nx*ny>12000 or ns*nt>60000:
        raise ValueError('Field grid too large')
    x=(np.arange(nx)+.5)*width_mm/nx-width_mm/2
    y=(np.arange(ny)+.5)*height_mm/ny-height_mm/2
    xx,yy=np.meshgrid(x,y,indexing='ij')
    sources_x=xx.ravel();sources_y=yy.ravel()
    s=np.linspace(max(.5,wavelength),s_max_mm,ns)
    t=np.linspace(-transverse_max_mm,transverse_max_mm,nt)
    ss,tt=np.meshgrid(s,t,indexing='ij')
    distances_s=ss.ravel();distances_t=tt.ravel()
    field=np.empty(distances_s.size,dtype=np.complex128)
    k=2*np.pi/wavelength
    for start in range(0,len(field),192):
        stop=min(start+192,len(field))
        rr=np.sqrt(distances_s[start:stop,None]**2+
                   (distances_t[start:stop,None]-sources_x)**2+sources_y**2)
        field[start:stop]=(np.exp(1j*k*rr)/(4*np.pi*rr)).sum(axis=1)*width_mm*height_mm/(nx*ny)
    amplitude=np.abs(field.reshape(ns,nt))
    peak=float(amplitude.max())
    db=20*np.log10(np.maximum(amplitude/max(peak,1e-30),1e-8))
    volume=None
    if include_volume:
        vs=np.linspace(s[0],s_max_mm,65)
        vt=np.linspace(-transverse_max_mm,transverse_max_mm,25)
        vu=np.linspace(-transverse_max_mm,transverse_max_mm,25)
        s3,t3,u3=np.meshgrid(vs,vt,vu,indexing='ij')
        flat_s,flat_t,flat_u=s3.ravel(),t3.ravel(),u3.ravel()
        amplitudes=np.empty(flat_s.size)
        for start in range(0,len(amplitudes),192):
            stop=min(start+192,len(amplitudes))
            rr=np.sqrt(flat_s[start:stop,None]**2+
                       (flat_t[start:stop,None]-sources_x)**2+
                       (flat_u[start:stop,None]-sources_y)**2)
            amplitudes[start:stop]=np.abs((np.exp(1j*k*rr)/(4*np.pi*rr)).sum(axis=1)*width_mm*height_mm/(nx*ny))
        peak=max(peak,float(amplitudes.max()))
        db=20*np.log10(np.maximum(amplitude/peak,1e-8))
        volume_db=20*np.log10(np.maximum(amplitudes.reshape(s3.shape)/peak,1e-8))
        volume=dict(s_mm=vs.tolist(),t_mm=vt.tolist(),u_mm=vu.tolist(),
                    amplitude_db=np.round(np.maximum(volume_db,-60),2).tolist(),
                    description='Computed 3D scalar aperture field; not a rotated 2D profile')
    return dict(volume=volume,model='HARMONIC_SCALAR_GREEN_RECTANGULAR_APERTURE',
                validated_elastic=False,source_plane='NORMAL_TO_EQUIVALENT_BEAM_AXIS',
                frequency_MHz=float(frequency_mhz),speed_m_s=float(speed_m_s),
                aperture_width_mm=float(width_mm),aperture_height_mm=float(height_mm),
                wavelength_mm=float(wavelength),s_mm=s.tolist(),transverse_mm=t.tolist(),
                amplitude_db=np.round(np.maximum(db,-60),2).tolist(),
                normalization='20log10 amplitude / maximum of this field grid',
                source_quadrature=[nx,ny],scope='DIRECT_HOMOGENEOUS_SCALAR_FIELD_ONLY')
