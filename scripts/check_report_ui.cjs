const fs = require('fs'), vm = require('vm'), assert = require('assert');
const html = fs.readFileSync('index.html','utf8');
assert(html.startsWith('<!DOCTYPE html>'));
assert.strictEqual(html,fs.readFileSync('dist/index.html','utf8'));
class Element {
 constructor(){this.attrs={};this.children=[];this.events={};this.style={};this.clientWidth=900;this.parentElement=this;}
 setAttribute(k,v){this.attrs[k]=String(v);if(k==='id')this.id=String(v)}
 getAttribute(k){return this.attrs[k]}
 appendChild(n){this.children.push(n);return n}
 addEventListener(k,f){this.events[k]=f}
 getBoundingClientRect(){return {width:900,left:0,top:0}}
 set innerHTML(v){this.children=[];this.content=v}
 get innerHTML(){return this.content||''}
}
const nodes={};
for(const m of html.matchAll(/<[^>]*\bid="([^"]+)"[^>]*>/g)){
 assert(!nodes[m[1]],'duplicate id '+m[1]);const n=nodes[m[1]]=new Element;
 for(const a of m[0].matchAll(/([\w-]+)="([^"]*)"/g))n.setAttribute(a[1],a[2]);
 n.hidden=m[0].includes('hidden=');
}
for(const m of html.matchAll(/(?:href="#|aria-controls=")([^" ]+)/g))assert(nodes[m[1]],'missing target '+m[1]);
const document={getElementById:id=>{assert(nodes[id],id);return nodes[id]},createElementNS:()=>new Element,querySelectorAll:q=>Object.values(nodes).filter(n=>q==='.morph-nav button'?(n.attrs.id||'').startsWith('morph-tab-'):(n.attrs.class||'').split(' ').includes(q.slice(1)))};
const location={hash:''}, listeners={};
const context=vm.createContext({document,ResizeObserver:class {observe(){}},console,location,history:{replaceState(a,b,c){location.hash=c}},window:{addEventListener(n,f){listeners[n]=f}}});
const script=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).join('\n');
vm.runInContext(script,context);
const chart=nodes.priceChart;
const patterns=()=>chart.children.filter(x=>x.attrs.class==='pattern-layer').length;
assert(chart.children.length>30);assert.equal(patterns(),1);
for(const id of ['togglePattern','toggleVolume','toggleLevels']){
 nodes[id].events.click({currentTarget:nodes[id]});assert.equal(nodes[id].attrs['aria-pressed'],'false');
 if(id==='togglePattern')assert.equal(patterns(),0);
 nodes[id].events.click({currentTarget:nodes[id]});assert.equal(nodes[id].attrs['aria-pressed'],'true');
}
for(const id of ['tab-up','tab-down','tab-base']){
 nodes[id].events.click();assert.equal(nodes[id].attrs['aria-selected'],'true');assert.equal(nodes[nodes[id].attrs['aria-controls']].hidden,false);
}
for(const id of Object.keys(nodes).filter(id=>id.startsWith('morph-tab-'))){
 nodes[id].events.click();assert.equal(nodes[id].attrs['aria-selected'],'true');
 assert.equal(nodes[nodes[id].attrs['aria-controls']].hidden,false);
 assert.equal(document.querySelectorAll('.morph-panel').filter(n=>!n.hidden).length,1);
}
for(const id of Object.keys(nodes).filter(id=>id.startsWith('dash-tab-'))){
 nodes[id].events.click();assert.equal(nodes[id].attrs['aria-selected'],'true');
 assert.equal(nodes[nodes[id].attrs['aria-controls']].hidden,false);
 assert.equal(document.querySelectorAll('.dash-pane').filter(n=>!n.hidden).length,1);
 assert.equal(location.hash,'#'+nodes[id].attrs['aria-controls']);
}
function check(n){for(const v of Object.values(n.attrs))assert(!/NaN|undefined|Infinity/.test(v));n.children.forEach(check)}
check(chart);
console.log('PASS: HTML targets, identical dist, chart rendering/switches, scenario and wave tabs, dashboard views and share hashes, finite SVG coordinates. DOM simulation only; no browser layout assertion.');
