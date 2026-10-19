/* ADHD2Quant v4 fx: falling tablets + 3D tilt (drafted with Claude Opus 5.5, reviewed) */
(function(){
var d=document,w=window,M=Math,mq=w.matchMedia('(prefers-reduced-motion: reduce)'),cp=w.matchMedia('(pointer: coarse)');
var L=[{s:[6,9],v:[12,18],o:[.10,.16],b:1},{s:[9,13],v:[18,28],o:[.16,.25]},{s:[13,18],v:[28,40],o:[.25,.35]}];
var c,x,R=0,W,H,S=[],P=[],raf=0,last=0;
function rn(a){return a[0]+M.random()*(a[1]-a[0])}
function mk(sz,ov,bl){
  var p=bl?7:3,wv=ov?sz*1.55:sz,h=sz,o=d.createElement('canvas'),g=o.getContext('2d'),T=M.PI*2;
  o.width=M.ceil((wv+p*2)*R);o.height=M.ceil((h+p*2)*R);
  g.scale(R,R);g.translate(p+wv/2,p+h/2);
  function e(k){g.beginPath();g.ellipse(0,0,wv/2*k,h/2*k,0,0,T)}
  e(1);
  if(bl){g.shadowBlur=5;g.shadowColor='rgba(255,165,110,.9)'}
  var r=g.createRadialGradient(-wv*.22,-h*.28,0,0,0,wv*.62);
  r.addColorStop(0,'#FFE4CC');r.addColorStop(.45,'#FFB07E');r.addColorStop(1,'#D9703C');
  g.fillStyle=r;g.fill();g.shadowBlur=0;
  var l=g.createLinearGradient(0,-h/2,0,h/2);
  l.addColorStop(0,'rgba(255,240,225,.75)');l.addColorStop(.5,'rgba(255,200,160,.1)');l.addColorStop(1,'rgba(120,45,15,.55)');
  g.lineWidth=M.max(.6,sz*.09);g.strokeStyle=l;e(.93);g.stroke();
  if(!bl){
    g.lineWidth=.7;g.strokeStyle='rgba(120,50,20,.35)';
    g.beginPath();g.moveTo(-wv*.3,0);g.lineTo(wv*.3,0);g.stroke();
    g.strokeStyle='rgba(255,235,215,.3)';
    g.beginPath();g.moveTo(-wv*.3,.7);g.lineTo(wv*.3,.7);g.stroke();
  }
  return{c:o,w:o.width/R,h:o.height/R};
}
function sprites(){S=L.map(function(l){return[mk(l.s[1],0,l.b),mk(l.s[1],1,l.b)]})}
function part(i){
  var li=i%3,l=L[li],t=M.random(),s=l.s[0]+t*(l.s[1]-l.s[0]);
  return{li:li,k:s/l.s[1],ov:M.random()<.5?1:0,v:l.v[0]+t*(l.v[1]-l.v[0]),o:l.o[0]+t*(l.o[1]-l.o[0]),
    x:M.random()*W,y:M.random()*(H+60)-30,r:M.random()*6.3,vr:(M.random()-.5)*.6,
    a:3+M.random()*10,f:.2+M.random()*.4,ph:M.random()*6.3};
}
function count(){var n=W<600?28:30;while(P.length<n)P.push(part(P.length));P.length=n;P.sort(function(a,b){return a.li-b.li})}
function size(){
  var nr=M.min(w.devicePixelRatio||1,2),ow=W||innerWidth;
  W=innerWidth;H=innerHeight;c.width=M.round(W*nr);c.height=M.round(H*nr);
  if(nr!==R){R=nr;sprites()}
  P.forEach(function(p){p.x*=W/ow});count();
}
function draw(t){
  x.setTransform(1,0,0,1,0,0);x.clearRect(0,0,c.width,c.height);
  for(var i=0;i<P.length;i++){
    var p=P[i],sp=S[p.li][p.ov],k=p.k*R,co=M.cos(p.r)*k,si=M.sin(p.r)*k;
    x.globalAlpha=p.o;
    x.setTransform(co,si,-si,co,(p.x+M.sin(t*p.f+p.ph)*p.a)*R,p.y*R);
    x.drawImage(sp.c,-sp.w/2,-sp.h/2,sp.w,sp.h);
  }
}
function step(n){
  var dt=last?M.min((n-last)/1e3,.05):0;last=n;
  for(var i=0;i<P.length;i++){var p=P[i];p.y+=p.v*dt;p.r+=p.vr*dt;if(p.y>H+30){p.y=-30;p.x=M.random()*W}}
  draw(n/1e3);raf=requestAnimationFrame(step);
}
function stop(){cancelAnimationFrame(raf);raf=0;last=0}
function go(){stop();if(mq.matches||d.hidden){draw(0)}else raf=requestAnimationFrame(step)}
var rz=0;
function init(){
  c=d.createElement('canvas');x=c.getContext('2d');c.setAttribute('aria-hidden','true');
  c.style.cssText='position:fixed;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none';
  d.body.insertBefore(c,d.body.firstChild);size();go();
  w.addEventListener('resize',function(){cancelAnimationFrame(rz);rz=requestAnimationFrame(function(){size();if(!raf)draw(0)})});
  d.addEventListener('visibilitychange',go);
  mq.addEventListener?mq.addEventListener('change',go):mq.addListener(go);
}
d.readyState==='loading'?d.addEventListener('DOMContentLoaded',init):init();

/* tilt */
var SEL='.card,.btn',cur=null;
function set(el,e,m){
  var b=el.getBoundingClientRect(),nx=(e.clientX-b.left)/b.width-.5,ny=(e.clientY-b.top)/b.height-.5;
  nx=M.max(-.5,M.min(.5,nx));ny=M.max(-.5,M.min(.5,ny));
  el.style.setProperty('--ry',(nx*m*2).toFixed(2)+'deg');
  el.style.setProperty('--rx',(-ny*m*2).toFixed(2)+'deg');
}
function reset(){if(cur){cur.style.removeProperty('--rx');cur.style.removeProperty('--ry');cur=null}}
function tgt(e){return e.target&&e.target.closest?e.target.closest(SEL):null}
d.addEventListener('pointermove',function(e){
  if(mq.matches||cp.matches||e.pointerType==='touch')return;
  var el=tgt(e);if(el!==cur)reset();if(el){cur=el;set(el,e,4)}
},{passive:true});
d.addEventListener('pointerout',function(e){if(cur&&e.pointerType!=='touch'&&!cur.contains(e.relatedTarget))reset()},{passive:true});
d.addEventListener('pointerdown',function(e){
  if(mq.matches||e.pointerType!=='touch')return;
  var el=tgt(e);reset();if(el){cur=el;set(el,e,3)}
},{passive:true});
['pointerup','pointercancel'].forEach(function(t){d.addEventListener(t,function(e){if(e.pointerType==='touch')reset()},{passive:true})});
w.addEventListener('hashchange',reset);
})();
