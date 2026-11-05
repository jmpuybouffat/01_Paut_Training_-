/* Reduced harmonic scalar plate model, mm / us / MHz.
   Finite-aperture quadrature; surface physical optics and weak-volume Born.
   One opposite-wall image per transmit/receive leg. No elastic mode conversion,
   wedge propagation, cap scattering or GTD. Never a hardware qualification. */
const PlatePhysics=(()=>{
 const PI=Math.PI,rad=x=>x*PI/180,clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
 const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),mul=(a,s)=>a.map(v=>v*s),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),norm=a=>Math.hypot(...a),unit=a=>mul(a,1/norm(a)),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
 const cmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],cadd=(a,b)=>[a[0]+b[0],a[1]+b[1]],abs=z=>Math.hypot(...z);
 function rotation(rx,ry,rz){const [a,b,c]=[rx,ry,rz].map(rad),ca=Math.cos(a),sa=Math.sin(a),cb=Math.cos(b),sb=Math.sin(b),cc=Math.cos(c),sc=Math.sin(c);return [[cc*cb,cc*sb*sa-sc*ca,cc*sb*ca+sc*sa],[sc*cb,sc*sb*sa+cc*ca,sc*sb*ca-cc*sa],[-sb,cb*sa,cb*ca]]}
 const rot=(R,v)=>R.map(r=>dot(r,v));
 function bounds(c,pose,profile){const h=rad(pose.heading),f=[Math.cos(h),Math.sin(h)],s=[-f[1],f[0]],margin=c.scan.margin_mm,center=[pose.x-profile.exit_offset_mm*f[0],pose.y-profile.exit_offset_mm*f[1]],corners=[];for(const a of [-.5,.5])for(const b of [-.5,.5])corners.push([center[0]+a*(profile.body_length_mm+2*margin)*f[0]+b*(profile.body_width_mm+2*margin)*s[0],center[1]+a*(profile.body_length_mm+2*margin)*f[1]+b*(profile.body_width_mm+2*margin)*s[1]]);if(corners.some(q=>q[0]<0||q[0]>c.geometry.length_x||q[1]<0||q[1]>c.geometry.width_y))return {ok:false,reason:'PLATE_EDGE',corners};const min=Math.min(...corners.map(q=>q[1])),max=Math.max(...corners.map(q=>q[1]));if(min<c.geometry.weld_axis_y+c.caps.width/2&&max>c.geometry.weld_axis_y-c.caps.width/2)return {ok:false,reason:'WELD_TOE',corners};return {ok:true,reason:'CONTACT',corners}}
 function ray(c,pose,beta,length=80){const top=pose.face!=='BOTTOM',z0=top?c.geometry.thickness_z:0,h=rad(pose.heading),b=rad(beta);let p=[pose.x,pose.y,z0],d=[Math.cos(h)*Math.sin(b),Math.sin(h)*Math.sin(b),(top?-1:1)*Math.cos(b)],left=length,out=[];for(let leg=0;leg<2;leg++){let end=top?0:c.geometry.thickness_z;if(leg)end=top?c.geometry.thickness_z:0;let t=Math.abs((end-p[2])/d[2]);let stop='WALL';for(let i=0;i<2;i++)if(Math.abs(d[i])>1e-9){const edge=d[i]>0?(i===0?c.geometry.length_x:c.geometry.width_y):0,te=(edge-p[i])/d[i];if(te>=0&&te<t){t=te;stop='EDGE'}}if(t>left){t=left;stop='LENGTH'}const q=add(p,mul(d,t));out.push({a:p,b:q,length:t,leg,stop});if(stop!=='WALL')break;left-=t;p=q;d=[d[0],d[1],-d[2]]}return out}
 function sampleSurface(row,lambda){const center=[row.x_mm,row.y_mm,row.z_mm],R=rotation(row.rx_deg,row.ry_deg,row.rz_deg),n=rot(R,[0,0,1]);if(row.type==='SPHERICAL_INCLUSION_REFERENCE'){const radius=row.diameter_mm/2,N=40,V=4*PI*radius**3/3;return Array.from({length:N},(_,i)=>{const z=1-2*(i+.5)/N,a=i*PI*(3-Math.sqrt(5)),r=radius*Math.cbrt((i+.5)/N),s=Math.sqrt(1-z*z);return {p:add(center,[r*s*Math.cos(a),r*s*Math.sin(a),r*z]),weight:V/N,born:true}})}
  const L=row.length_mm,W=row.width_mm,nx=Math.max(3,Math.ceil(L/(lambda/2.5))),ny=Math.max(2,Math.ceil(W/(lambda/2.5))),out=[];
  if(nx*ny>2400)throw Error('SURFACE_TOO_LARGE');
  for(let i=0;i<nx;i++)for(let j=0;j<ny;j++){const x=-L/2+(i+.5)/nx*L;let y=-W/2+(j+.5)/ny*W,weight=L*W/(nx*ny);if(row.type==='SAWTOOTH_CRACK_REFERENCE'){const u=((x+L/2)/(L/8))%2,wave=.05-(u<1?u:2-u)*.1;y=y*(W-.1)/W+wave;weight=L*(W-.1)/(nx*ny)}out.push({p:add(center,rot(R,[x,y,0])),n,weight,born:false})}return out;
 }
 function buildSource(c,pose,profile,rx=false){const T=c.geometry.thickness_z,top=pose.face!=='BOTTOM',z=top?T:0,into=top?-1:1,h=rad(pose.heading),f=[Math.cos(h),Math.sin(h),0],side=[-f[1],f[0],0],center=[pose.x,pose.y,z],speed=(profile.mode==='L'?c.material.VL_m_s:c.material.VT_m_s)/1000,lambda=speed/profile.frequency_MHz,points=[],N=profile.kind==='PA'?32:1;
  let base=center,direction;
  if(profile.kind==='SE'){const offset=(rx?1:-1)*profile.separation_mm/2;base=add(center,mul(f,offset));direction=unit(sub(add(center,[0,0,into*profile.cross_depth_mm]),base))}else{const beta=rad(profile.angle_deg);direction=add(mul(f,Math.sin(beta)),[0,0,into*Math.cos(beta)])}
  const width=profile.kind==='PA'?profile.element_width_mm:profile.active_width_mm,height=profile.active_height_mm;
  const ny=Math.max(2,Math.ceil(width/(lambda/2))),nx=Math.max(2,Math.ceil(height/(lambda/2))),up=profile.kind==='PA'?f:unit(cross(side,direction));
  for(let e=0;e<N;e++){const s=N===1?0:(e-(N-1)/2)*profile.pitch_mm,ec=add(base,mul(f,s));for(let i=0;i<nx;i++)for(let j=0;j<ny;j++)points.push({p:add(ec,add(mul(side,((i+.5)/nx-.5)*height),mul(up,((j+.5)/ny-.5)*width))),d:profile.kind==='PA'?[0,0,into]:direction,e,w:1/(nx*ny*N)})}
  if(points.length>7000)throw Error('APERTURE_TOO_LARGE');return {points,center:base,direction,N,speed,lambda,k:2*PI/lambda,f,top,into,profile};
 }
 function images(c,source,path){const back=source.top?0:c.geometry.thickness_z;return source.points.map(a=>path?{...a,p:[a.p[0],a.p[1],2*back-a.p[2]],d:[a.d[0],a.d[1],-a.d[2]],w:-a.w}:a)}
 function channel(c,source,point,normal,path){const out=Array.from({length:source.N},()=>[0,0,0,0]),back=source.top?0:c.geometry.thickness_z,center=path?[source.center[0],source.center[1],2*back-source.center[2]]:source.center;
  if(path){const t=(back-center[2])/(point[2]-center[2]),bx=center[0]+t*(point[0]-center[0]),by=center[1]+t*(point[1]-center[1]);if(bx<0||bx>c.geometry.length_x||by<0||by>c.geometry.width_y)return out}
  for(const a of source.imagePoints[path]){const dx=point[0]-a.p[0],dy=point[1]-a.p[1],dz=point[2]-a.p[2],r=Math.hypot(dx,dy,dz);if(r<source.lambda/3)continue;const emit=Math.max(0,(a.d[0]*dx+a.d[1]*dy+a.d[2]*dz)/r),mu=normal?-(normal[0]*dx+normal[1]*dy+normal[2]*dz)/r:1;if(mu<=0||emit<=0)continue;const w=a.w*emit/r,co=w*Math.cos(source.k*r),si=w*Math.sin(source.k*r),v=out[a.e];v[0]+=co;v[1]+=si;v[2]+=mu*co;v[3]+=mu*si}return out;
 }
 function weights(source,pose,beta){if(source.N===1)return [[1,0]];const b=rad(beta),focus=source.profile.focus_mm,point=add([pose.x,pose.y,source.center[2]],add(mul(source.f,Math.sin(b)*focus),[0,0,source.into*Math.cos(b)*focus]));return Array.from({length:source.N},(_,e)=>{const s=(e-(source.N-1)/2)*source.profile.pitch_mm,ec=add(source.center,mul(source.f,s)),phase=focus>0?-source.k*(norm(sub(point,ec))-focus):source.k*s*Math.sin(b);return [Math.cos(phase),Math.sin(phase)]})}
 function weighted(values,w){let a=0,b=0,c=0,d=0;for(let i=0;i<values.length;i++){const v=values[i],q=w[i];a+=v[0]*q[0]-v[1]*q[1];b+=v[0]*q[1]+v[1]*q[0];c+=v[2]*q[0]-v[3]*q[1];d+=v[2]*q[1]+v[3]*q[0]}return {p:[a,b],d:[c,d]}}
 function prepare(c,pose,profile){const tx=buildSource(c,pose,profile),rx=profile.kind==='SE'?buildSource(c,pose,profile,true):tx;tx.imagePoints=[images(c,tx,0),images(c,tx,1)];if(rx!==tx)rx.imagePoints=[images(c,rx,0),images(c,rx,1)];const targets=[];
  for(const row of c.indications.filter(r=>r.enabled)){const nodes=sampleSurface(row,tx.lambda).filter(q=>q.p[0]>=0&&q.p[0]<=c.geometry.length_x&&q.p[1]>=0&&q.p[1]<=c.geometry.width_y&&q.p[2]>=0&&q.p[2]<=c.geometry.thickness_z),hemispheres=[];
   for(const sign of (row.type==='SPHERICAL_INCLUSION_REFERENCE'?[1]:[1,-1])){const list=[];for(const q of nodes){const n=q.n?mul(q.n,sign):null,tc=[channel(c,tx,q.p,n,0),c.reflections?channel(c,tx,q.p,n,1):Array.from({length:tx.N},()=>[0,0,0,0])],rc=rx===tx?tc:[channel(c,rx,q.p,n,0),c.reflections?channel(c,rx,q.p,n,1):Array.from({length:rx.N},()=>[0,0,0,0])];list.push({...q,n,tc,rc})}hemispheres.push(list)}targets.push({row,hemispheres})}
  return {tx,rx,targets,c,pose,profile};
 }
 function evaluate(prep,beta){const {tx,rx,c,pose}=prep,w=weights(tx,pose,beta),wr=weights(rx,pose,beta),events=[],selected=[];
  for(const target of prep.targets){const sums=[[0,0],[0,0],[0,0]],fieldNodes=[];
   for(const hemi of target.hemispheres)for(const q of hemi){const tc=q.tc.map(v=>weighted(v,w)),rc=q.rc.map(v=>weighted(v,wr));fieldNodes.push({...q,excitation:tc.map(t=>t.p),derivative:tc.map(t=>t.d)});
    for(let i=0;i<2;i++)for(let j=0;j<2;j++){const n=i+j;let z;if(q.born){z=mul(cmul(tc[i].p,rc[j].p),tx.k*tx.k*q.weight*c.inclusion_contrast/(4*PI))}else{const v=cadd(cmul(tc[i].d,rc[j].p),cmul(tc[i].p,rc[j].d)),scale=tx.k*q.weight/(4*PI);z=[-v[1]*scale,v[0]*scale]}sums[n]=cadd(sums[n],z)}
   }
   const p=[target.row.x_mm,target.row.y_mm,target.row.z_mm],back=tx.top?0:c.geometry.thickness_z,direct=norm(sub(p,tx.center)),reflected=norm(sub(p,[tx.center[0],tx.center[1],2*back-tx.center[2]])),rdirect=norm(sub(p,rx.center)),rreflected=norm(sub(p,[rx.center[0],rx.center[1],2*back-rx.center[2]]));
   const lengths=[direct+rdirect,((direct+rreflected)+(reflected+rdirect))/2,reflected+rreflected];
   sums.forEach((z,path)=>{const amp=abs(z)/c.amplitude_reference;if(amp>1e-12)events.push({id:target.row.id,kind:'flaw',path:['DD','DR_RD','RR'][path],time_us:lengths[path]/tx.speed,amplitude:amp,phase_rad:Math.atan2(z[1],z[0]),complex:z,angle_deg:beta,model:qModel(target.row),position_from_truth_not_reconstruction:p})});
   selected.push({id:target.row.id,nodes:fieldNodes,amplitude:Math.max(...sums.map(z=>abs(z)/c.amplitude_reference))});
  }
  return {events,targets:selected,beta,w,wr};
 }
 function qModel(r){return r.type==='SPHERICAL_INCLUSION_REFERENCE'?'SCALAR_WEAK_VOLUME_BORN':'SCALAR_SURFACE_PHYSICAL_OPTICS'}
 function backwall(prep,beta){const {tx,rx,c,pose}=prep,w=weights(tx,pose,beta),wr=weights(rx,pose,beta);let value=[0,0];const txImages=tx.imagePoints[1];
  // Finite-aperture reciprocal reflection; cached by UI worker across poses.
  for(const b of rx.points){let p=[0,0];for(const a of txImages){const d=sub(b.p,a.p),r=norm(d);if(r<tx.lambda/3)continue;const u=mul(d,1/r),emit=Math.max(0,dot(a.d,u)),receive=Math.max(0,-dot(b.d,u));if(!emit||!receive)continue;const f=a.w*b.w*emit*receive/r,phase=tx.k*r,term=cmul([f*Math.cos(phase),f*Math.sin(phase)],cmul(w[a.e],wr[b.e]));p=cadd(p,term)}value=cadd(value,p)}
  const back=tx.top?0:c.geometry.thickness_z,path=norm(sub(rx.center,[tx.center[0],tx.center[1],2*back-tx.center[2]]));return {id:'BACKWALL',kind:'geometry',path:'BACKWALL_RECEIVED',time_us:path/tx.speed,amplitude:abs(value)/c.amplitude_reference,phase_rad:Math.atan2(value[1],value[0]),complex:value,angle_deg:beta,model:'FINITE_APERTURE_SCALAR_IMAGE'};
 }
 function field(prep,evaluation,point,targetId){const target=evaluation.targets.find(t=>t.id===targetId);if(!target)return {incident:0,scattered:0};const {tx,c}=prep;let p=[0,0];for(const q of target.nodes){for(let i=0;i<2;i++){const inc=q.excitation[i],der=q.derivative[i];for(let j=0;j<(c.reflections?2:1);j++){const back=tx.top?0:c.geometry.thickness_z,pos=j?[point[0],point[1],2*back-point[2]]:point,d=sub(pos,q.p),r=norm(d);if(r<tx.lambda/2)continue;const mu=q.n?dot(q.n,mul(d,1/r)):1;if(mu<=0)continue;const phase=tx.k*r,g=[(j?-1:1)*Math.cos(phase)/r,(j?-1:1)*Math.sin(phase)/r];let v;if(q.born)v=mul(cmul(inc,g),tx.k*tx.k*q.weight*c.inclusion_contrast/(4*PI));else{const z=cmul(cadd(der,mul(inc,mu)),g),s=tx.k*q.weight/(4*PI);v=[-z[1]*s,z[0]*s]}p=cadd(p,v)}}}return {scattered:abs(p)/c.amplitude_reference,complex:p}}
 function incident(prep,evaluation,point){const q=channel(prep.c,prep.tx,point,null,0),p=weighted(q,evaluation.w).p;return abs(p)}
 function envelope(events,t,frequency){const sigma=.65/frequency;return events.reduce((s,e)=>s+e.amplitude*Math.exp(-.5*((t-e.time_us)/sigma)**2),0)}
 function project(c,pose,beta,time,profile){const speed=(profile.mode==='L'?c.material.VL_m_s:c.material.VT_m_s)/1000,l0=time*speed/2,l=profile.kind==='SE'?Math.sqrt(Math.max(0,l0*l0-(profile.separation_mm/2)**2)):l0,b=rad(beta),h=rad(pose.heading),T=c.geometry.thickness_z,travel=l*Math.cos(b);let depth=((travel%(2*T))+2*T)%(2*T);if(depth>T)depth=2*T-depth;const z=pose.face==='BOTTOM'?depth:T-depth;return [pose.x+l*Math.sin(b)*Math.cos(h),pose.y+l*Math.sin(b)*Math.sin(h),z]}
 return {rotation,bounds,ray,prepare,evaluate,backwall,field,incident,envelope,project,buildSource,sampleSurface,weights};
})();
if(typeof module!=='undefined')module.exports=PlatePhysics;
