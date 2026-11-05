/* Finite linear array in the equivalent homogeneous steel medium.
   32 elements, complex focusing/steering and reciprocal aperture reception.
   Scalar Kirchhoff only: no wedge/refraction/contact or elastic conversion. */
const NozzleArray=(()=>{
 const pi=Math.PI,add=(a,b)=>a.map((x,i)=>x+b[i]),sub=(a,b)=>a.map((x,i)=>x-b[i]),mul=(a,s)=>a.map(x=>x*s),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),norm=a=>Math.hypot(...a),unit=a=>mul(a,1/norm(a)),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
 function source(center,outward,forward,profile,wavelength){
  if(profile.elements!==32||!(profile.pitch_mm>0)||!(profile.element_width_mm>0&&profile.element_width_mm<=profile.pitch_mm)||!(profile.elevation_mm>0)||!(wavelength>0))throw Error('Invalid 32-element array geometry');
  const n=unit(outward),f=unit(forward),side=unit(cross(n,f)),nx=Math.max(2,Math.ceil(profile.element_width_mm/(wavelength/2))),ny=Math.max(2,Math.ceil(profile.elevation_mm/(wavelength/2))),points=[],indices=[],centres=[];
  if(nx*ny*32>14000)throw Error('Array aperture quadrature too large');
  for(let e=0;e<32;e++){const ec=add(center,mul(f,(e-15.5)*profile.pitch_mm));centres.push(ec);for(let i=0;i<nx;i++)for(let j=0;j<ny;j++){points.push(add(ec,add(mul(f,((i+.5)/nx-.5)*profile.element_width_mm),mul(side,((j+.5)/ny-.5)*profile.elevation_mm))));indices.push(e);}}
  return {center,direction:mul(n,-1),outward:n,forward:f,side,points,indices,centres,wavelength,profile,normalization:'unit average over all active aperture points'};
 }
 function prepare(src,surface){const k=2*pi/src.wavelength,N=src.points.length,nodes=[];let area=0;
  for(const q of surface.points){let n=q.n;const incoming=unit(sub(src.center,q.p));if(q.twoSided&&dot(n,incoming)<0)n=mul(n,-1);if(dot(n,incoming)<=0)continue;const channels=Array.from({length:32},()=>[0,0,0,0]);
   for(let i=0;i<N;i++){const d=sub(q.p,src.points[i]),r=norm(d);if(r<src.wavelength/2)continue;const emit=Math.max(0,dot(src.direction,d)/r),mu=Math.max(0,-dot(n,d)/r);if(!emit||!mu)continue;const scale=emit/(r*N),re=scale*Math.cos(k*r),im=scale*Math.sin(k*r),v=channels[src.indices[i]];v[0]+=re;v[1]+=im;v[2]+=mu*re;v[3]+=mu*im;}
   nodes.push({p:q.p,n,area:q.area,channels});area+=q.area;
  }return {src,nodes,k,wavelength:src.wavelength,illuminated_area_mm2:area};
 }
 function phases(src,angleDeg,focusMm){const beta=angleDeg*pi/180,k=2*pi/src.wavelength,d=add(mul(src.outward,-Math.cos(beta)),mul(src.forward,Math.sin(beta))),focal=add(src.center,mul(d,focusMm));return src.centres.map(ec=>{const phase=focusMm>0?-k*(norm(sub(focal,ec))-focusMm):k*dot(sub(ec,src.center),src.forward)*Math.sin(beta);return [Math.cos(phase),Math.sin(phase)]});}
 function evaluate(base,angleDeg,focusMm){const w=phases(base.src,angleDeg,focusMm),nodes=[];let re=0,im=0;
  for(const q of base.nodes){let p=0,v=0,d=0,u=0;for(let e=0;e<32;e++){const a=q.channels[e],b=w[e];p+=a[0]*b[0]-a[1]*b[1];v+=a[0]*b[1]+a[1]*b[0];d+=a[2]*b[0]-a[3]*b[1];u+=a[2]*b[1]+a[3]*b[0];}nodes.push({p:q.p,n:q.n,area:q.area,re:p,im:v,mre:d,mim:u});
   // Reciprocity factors the full receiving-aperture integral exactly into 2*P*D.
   const scale=base.k*q.area/(2*pi);re-=scale*(p*u+v*d);im+=scale*(p*d-v*u);
  }
  return {prepared:{source:base.src,surface:null,nodes,k:base.k,wavelength:base.wavelength,illuminated_area_mm2:base.illuminated_area_mm2,visible:()=>true},received:{re,im,amplitude:Math.hypot(re,im),phase:Math.atan2(im,re),aperture_samples:base.src.points.length},weights:w};
 }
 function incident(src,w,p){let re=0,im=0;const k=2*pi/src.wavelength,N=src.points.length;for(let i=0;i<N;i++){const d=sub(p,src.points[i]),r=norm(d);if(r<src.wavelength/2)continue;const emit=Math.max(0,dot(src.direction,d)/r),a=emit/(r*N),co=a*Math.cos(k*r),si=a*Math.sin(k*r),q=w[src.indices[i]];re+=co*q[0]-si*q[1];im+=co*q[1]+si*q[0];}return {re,im,amplitude:Math.hypot(re,im)};}
 return {source,prepare,phases,evaluate,incident};
})();
if(typeof module!=='undefined')module.exports=NozzleArray;
