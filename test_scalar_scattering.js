'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),S=require('./scalar_scattering');
const wavelength=.81;
const source=(center=[0,0,0],direction=[0,0,1],size=8,res=3)=>S.aperture(center,direction,[1,0,0],[0,1,0],size,size,wavelength,res);
const plane=(normal=[0,0,-1],res=3)=>S.rectangle([0,0,20],normal,[1,0,0],6,3,wavelength,res);
// Embedded browser solver must be byte-identical to the independently tested kernel.
assert(fs.readFileSync('nozzle_operator.html','utf8').includes(fs.readFileSync('scalar_scattering.js','utf8')));
const p=S.prepare(source(),plane(),wavelength),r=S.receive(p);
assert(Number.isFinite(r.amplitude)&&r.amplitude>0);
assert(Math.abs(plane().points.reduce((a,n)=>a+n.area,0)-18)<1e-10);
const fine=S.receive(S.prepare(source([0,0,0],[0,0,1],8,4),plane([0,0,-1],4),wavelength));
assert(Math.abs(fine.amplitude/r.amplitude-1)<.04,'Quadrature does not converge');
// Coherent cancellation: reverse all complex surface amplitudes -> reverse field.
const observation=[2,0,0],a=S.at(p,observation),opposite={...p,nodes:p.nodes.map(n=>({...n,re:-n.re,im:-n.im,mre:-n.mre,mim:-n.mim}))},b=S.at(opposite,observation);
assert(Math.hypot(a.re+b.re,a.im+b.im)<1e-12);
const half1={...p,nodes:p.nodes.slice(0,100)},half2={...p,nodes:p.nodes.slice(100)},v1=S.at(half1,observation),v2=S.at(half2,observation);
assert(Math.hypot(a.re-v1.re-v2.re,a.im-v1.im-v2.im)<1e-12);
// Reciprocity, including finite transmitting and receiving apertures.
const tx=source([-2,0,0]),rx=source([2,0,0]);
const ab=S.receive(S.prepare(tx,plane(),wavelength),rx),ba=S.receive(S.prepare(rx,plane(),wavelength),tx);
assert(Math.hypot(ab.re-ba.re,ab.im-ba.im)/ab.amplitude<1e-10,'Tx/Rx reciprocity violated');
// A tilted finite face must change the monostatic return without per-pose normalization.
const tilted=S.receive(S.prepare(source(),plane([0,Math.sin(Math.PI/3),-Math.cos(Math.PI/3)]),wavelength));
assert(tilted.amplitude<r.amplitude*.25,'Tilt does not suppress specular reception');
assert(Math.abs(S.db(2*r.amplitude)-S.db(r.amplitude)-6.020599913)<1e-8);
// Analytic Fraunhofer rectangular-surface null in the scattered field.
const distant=S.prepare(source([0,0,0],[0,0,1],1),S.rectangle([0,0,1000],[0,0,-1],[1,0,0],6,3,wavelength),wavelength);
const sine=wavelength/6,x=1000*sine/Math.sqrt(1-sine*sine),on=S.at(distant,[0,0,0]),off=S.at(distant,[x,0,0]);
assert(20*Math.log10(off.amplitude/on.amplitude)<-35,'Rectangular diffraction null missing');
// Sphere has its own outward normals and illuminated hemisphere (not a planar patch).
const sphere=S.sphere([0,0,20],2,wavelength),sp=S.prepare(source(),sphere,wavelength);
assert(sp.nodes.length>0&&sp.nodes.length<sphere.points.length);
assert(S.receive(sp).amplitude>0);
assert.equal(S.at({...p,nodes:[]},[0,0,0]).amplitude,0);
assert.throws(()=>source([0,0,0],[0,0,1],0));
console.log('Scalar scattering: finite surface, quadrature convergence, complex superposition/cancellation, Tx/Rx reciprocity, tilt response, fixed dB, analytic diffraction null and sphere illumination: OK');
