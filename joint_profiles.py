"""Faceted training weld profiles, not measured geometry or an elastic solver."""
import numpy as np


def faceted_joint_profiles(R, Ri, nozzle_radius, alpha_deg, offset, length,
                           gap, land, bevel_deg, reinforcement,
                           root_amplitude=.8, cap_amplitude=1., facets=24, seed=17):
    alpha=np.deg2rad(alpha_deg);u=np.array([np.sin(alpha),0.,np.cos(alpha)])
    b=np.array([np.cos(alpha),0.,-np.sin(alpha)])
    origin=np.array([0.,offset,0.]);rng=np.random.default_rng(int(seed))
    facets=int(facets)
    if facets<8 or facets>96 or min(root_amplitude,cap_amplitude)<0:
        raise ValueError('Invalid training profile settings')
    meshes={};references={}
    for name,amplitude in [('root',root_amplitude),('cap',cap_amplitude)]:
        heights=rng.uniform(-1.,1.,facets);heights=np.r_[heights,heights[0]]
        vertices=[]
        for i in range(facets+1):
            theta=2*np.pi*i/facets;direction=np.cos(theta)*b+np.sin(theta)*np.array([0.,1.,0.])
            for j,f in enumerate(np.linspace(0,1,5)):
                if name=='root':
                    rad=nozzle_radius+max(gap,1.)*f
                    target=Ri-amplitude*(.5+.5*heights[i])*np.sin(np.pi*f)
                else:
                    rad=nozzle_radius+(gap+max(R-Ri-land,0)*np.tan(np.deg2rad(bevel_deg)))*f
                    target=R+(reinforcement+amplitude*heights[i])*np.sin(np.pi*f)
                q=origin+rad*direction;A=u[0]**2;B=2*q[0]*u[0]
                disc=B*B-4*A*(q[0]**2+q[1]**2-target**2)
                if disc<0:
                    raise ValueError('Faceted profile outside cylindrical intersection envelope')
                point=q+(-B+np.sqrt(disc))/(2*A)*u
                vertices.append(point)
        vertices=np.asarray(vertices);triangles=[]
        for i in range(facets):
            for j in range(4):
                a=i*5+j;bb=(i+1)*5+j
                triangles.extend([[a,bb,a+1],[a+1,bb,bb+1]])
        points=[];normals=[]
        for i in range(facets):
            p=vertices[i*5+2];q=vertices[(i+1)*5+2]
            n=np.cross(q-p,vertices[i*5+3]-p);m=np.linalg.norm(n)
            n=n/m if m>1e-12 else np.array([0.,0.,1.])
            for f in np.linspace(0,1,8,endpoint=False):
                candidate=p+(q-p)*f
                if abs(candidate[2])<=length/2:
                    points.append(candidate.tolist());normals.append(n.tolist())
        meshes[name]=dict(vertices_mm=vertices.tolist(),triangles=triangles,
                          model='FACETED_TRAINING_GEOMETRY',measured=False)
        references[name]=dict(points_mm=points,normals=normals)
    return dict(meshes=meshes,references=references,seed=int(seed),facets=facets,
                root_amplitude_mm=float(root_amplitude),cap_amplitude_mm=float(cap_amplitude),
                measured=False)
