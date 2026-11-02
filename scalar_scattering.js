/* Finite-aperture scalar single scattering, equivalent homogeneous medium.
 * Kirchhoff physical-optics surface integral; no elastic modes or wall bounces.
 * All lengths are mm, harmonic convention exp(+ikr). Not an industrial solver.
 */
const ScalarScattering = (()=>{
 const pi=Math.PI,sub=(a,b)=>a.map((x,i)=>x-b[i]),dot=(a,b)=>a.reduce((v,x,i)=>v+x*b[i],0),norm=a=>Math.hypot(...a),scale=(a,s)=>a.map(x=>x*s),add=(a,b)=>a.map((x,i)=>x+b[i]),unit=a=>scale(a,1/norm(a));
 function positive(x,name){if(!Number.isFinite(x)||x<=0)throw Error(name+' must be positive and finite')}
 function aperture(center,direction,side,up,width,height,wavelength,resolution=3){
  [width,height,wavelength,resolution].forEach(x=>positive(x,'aperture parameter'));
  const nx=Math.ceil(width*resolution/wavelength),ny=Math.ceil(height*resolution/wavelength);
  if(nx*ny>18000)throw Error('Aperture quadrature exceeds supported size');
  const points=[];for(let i=0;i<nx;i++)for(let j=0;j<ny;j++)points.push(add(center,add(scale(side,((i+.5)/nx-.5)*width),scale(up,((j+.5)/ny-.5)*height))));
  return {center,direction:unit(direction),points,width,height,quadrature:[nx,ny],normalization:'unit average source aperture pressure'};
 }
 function rectangle(center,normal,u,length,width,wavelength,resolution=3){
  [length,width,wavelength,resolution].forEach(x=>positive(x,'surface parameter'));
  const n=unit(normal),v=unit([n[1]*u[2]-n[2]*u[1],n[2]*u[0]-n[0]*u[2],n[0]*u[1]-n[1]*u[0]]),uu=unit(u),nx=Math.ceil(length*resolution/wavelength),ny=Math.ceil(width*resolution/wavelength);
  if(nx*ny>8000)throw Error('Surface quadrature exceeds supported size');
  const points=[];for(let i=0;i<nx;i++)for(let j=0;j<ny;j++)points.push({p:add(center,add(scale(uu,((i+.5)/nx-.5)*length),scale(v,((j+.5)/ny-.5)*width))),n,area:length*width/(nx*ny),twoSided:true});
  return {points,center,normal:n,area:length*width,quadrature:[nx,ny],shape:'FINITE_PLANAR_RECTANGLE'};
 }
 function sphere(center,diameter,wavelength,resolution=3){
  [diameter,wavelength,resolution].forEach(x=>positive(x,'sphere parameter'));
  const radius=diameter/2,area=4*pi*radius*radius,count=Math.max(80,Math.ceil(area/(wavelength/resolution)**2));if(count>8000)throw Error('Sphere quadrature exceeds supported size');
  const points=[];for(let i=0;i<count;i++){const z=1-2*(i+.5)/count,r=Math.sqrt(1-z*z),a=i*pi*(3-Math.sqrt(5)),n=[r*Math.cos(a),r*Math.sin(a),z];points.push({p:add(center,scale(n,radius)),n,area:area/count,twoSided:false})}
  return {points,center,area,quadrature:[count],shape:'ILLUMINATED_SPHERE_PHYSICAL_OPTICS'};
 }
 function prepare(source,surface,wavelength,visible=()=>true){
  positive(wavelength,'wavelength');const k=2*pi/wavelength,nodes=[],N=source.points.length;let keptArea=0;
  for(const q of surface.points){if(!visible(source.center,q.p))continue;let n=q.n;const incoming=unit(sub(source.center,q.p));if(q.twoSided&&dot(n,incoming)<0)n=scale(n,-1);if(dot(n,incoming)<=0)continue;
   let re=0,im=0,mre=0,mim=0;
   for(const a of source.points){const dx=q.p[0]-a[0],dy=q.p[1]-a[1],dz=q.p[2]-a[2],r=Math.hypot(dx,dy,dz);if(r<wavelength/2)continue;const emit=Math.max(0,(source.direction[0]*dx+source.direction[1]*dy+source.direction[2]*dz)/r),mu=Math.max(0,-(n[0]*dx+n[1]*dy+n[2]*dz)/r);if(!emit||!mu)continue;const f=emit/(r*N),c=f*Math.cos(k*r),s=f*Math.sin(k*r);re+=c;im+=s;mre+=mu*c;mim+=mu*s}
   nodes.push({p:q.p,n,area:q.area,re,im,mre,mim});keptArea+=q.area;
  }
  return {source,surface,nodes,k,wavelength,illuminated_area_mm2:keptArea,visible,model:'FINITE_SURFACE_SCALAR_KIRCHHOFF_SINGLE_SCATTERING',validated_elastic:false};
 }
 function at(prepared,p,receiveDirection=null){
  let re=0,im=0;const {k,wavelength,visible}=prepared;
  for(const q of prepared.nodes){const dx=p[0]-q.p[0],dy=p[1]-q.p[1],dz=p[2]-q.p[2],r=Math.hypot(dx,dy,dz);if(r<wavelength/2||!visible(q.p,p))continue;const mu=(q.n[0]*dx+q.n[1]*dy+q.n[2]*dz)/r;if(mu<=0)continue;const rx=receiveDirection?Math.max(0,-(receiveDirection[0]*dx+receiveDirection[1]*dy+receiveDirection[2]*dz)/r):1;if(rx===0)continue;
   // i*k/(4*pi) * integral [(mu_in + mu_out) p_inc G] dS.
   const a=q.mre+mu*q.re,b=q.mim+mu*q.im,f=q.area*k*rx/(4*pi*r),c=Math.cos(k*r),s=Math.sin(k*r);
   re+=f*(-b*c-a*s);im+=f*(a*c-b*s);
  }
  return {re,im,amplitude:Math.hypot(re,im),phase:Math.atan2(im,re)};
 }
 function receive(prepared,receiver=prepared.source){
  let re=0,im=0;for(const p of receiver.points){const v=at(prepared,p,receiver.direction);re+=v.re;im+=v.im}re/=receiver.points.length;im/=receiver.points.length;
  return {re,im,amplitude:Math.hypot(re,im),phase:Math.atan2(im,re),aperture_samples:receiver.points.length};
 }
 function db(amplitude,reference=.05){positive(reference,'fixed amplitude reference');return 20*Math.log10(Math.max(amplitude/reference,1e-12))}
 return {aperture,rectangle,sphere,prepare,at,receive,db};
})();
if(typeof module!=='undefined')module.exports=ScalarScattering;
