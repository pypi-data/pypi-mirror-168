var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,a,o,u,i,l,s,d,f,p,c,h,v,y,m,b,g,j,w={299:(e,r,t)=>{var n={"./index":()=>t.e(163).then((()=>()=>t(163))),"./extension":()=>t.e(163).then((()=>()=>t(163))),"./style":()=>t.e(747).then((()=>()=>t(747)))},a=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var n="default",a=t.S[n];if(a&&a!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[n]=e,t.I(n,r)}};t.d(r,{get:()=>a,init:()=>o})}},_={};function S(e){var r=_[e];if(void 0!==r)return r.exports;var t=_[e]={id:e,exports:{}};return w[e](t,t.exports,S),t.exports}S.m=w,S.c=_,S.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return S.d(r,{a:r}),r},S.d=(e,r)=>{for(var t in r)S.o(r,t)&&!S.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},S.f={},S.e=e=>Promise.all(Object.keys(S.f).reduce(((r,t)=>(S.f[t](e,r),r)),[])),S.u=e=>e+"."+{163:"ed570805beddccbf0bc5",747:"1e835994703b0b9315be"}[e]+".js?v="+{163:"ed570805beddccbf0bc5",747:"1e835994703b0b9315be"}[e],S.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),S.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="jupyter_app_launcher:",S.l=(t,n,a,o)=>{if(e[t])e[t].push(n);else{var u,i;if(void 0!==a)for(var l=document.getElementsByTagName("script"),s=0;s<l.length;s++){var d=l[s];if(d.getAttribute("src")==t||d.getAttribute("data-webpack")==r+a){u=d;break}}u||(i=!0,(u=document.createElement("script")).charset="utf-8",u.timeout=120,S.nc&&u.setAttribute("nonce",S.nc),u.setAttribute("data-webpack",r+a),u.src=t),e[t]=[n];var f=(r,n)=>{u.onerror=u.onload=null,clearTimeout(p);var a=e[t];if(delete e[t],u.parentNode&&u.parentNode.removeChild(u),a&&a.forEach((e=>e(n))),r)return r(n)},p=setTimeout(f.bind(null,void 0,{type:"timeout",target:u}),12e4);u.onerror=f.bind(null,u.onerror),u.onload=f.bind(null,u.onload),i&&document.head.appendChild(u)}},S.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{S.S={};var e={},r={};S.I=(t,n)=>{n||(n=[]);var a=r[t];if(a||(a=r[t]={}),!(n.indexOf(a)>=0)){if(n.push(a),e[t])return e[t];S.o(S.S,t)||(S.S[t]={});var o=S.S[t],u="jupyter_app_launcher",i=[];return"default"===t&&((e,r,t,n)=>{var a=o[e]=o[e]||{},i=a[r];(!i||!i.loaded&&(1!=!i.eager?n:u>i.from))&&(a[r]={get:()=>S.e(163).then((()=>()=>S(163))),from:u,eager:!1})})("jupyter_app_launcher","0.1.1"),e[t]=i.length?Promise.all(i).then((()=>e[t]=1)):1}}})(),(()=>{var e;S.g.importScripts&&(e=S.g.location+"");var r=S.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),S.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var a=e[n],o=(typeof a)[0];if(n>=r.length)return"u"==o;var u=r[n],i=(typeof u)[0];if(o!=i)return"o"==o&&"n"==i||"s"==i||"u"==o;if("o"!=o&&"u"!=o&&a!=u)return a<u;n++}},a=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,o=1;o<e.length;o++)n--,t+="u"==(typeof(i=e[o]))[0]?"-":(n>0?".":"")+(n=2,i);return t}var u=[];for(o=1;o<e.length;o++){var i=e[o];u.push(0===i?"not("+l()+")":1===i?"("+l()+" || "+l()+")":2===i?u.pop()+" "+u.pop():a(i))}return l();function l(){return u.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var n=e[0],a=n<0;a&&(n=-n-1);for(var u=0,i=1,l=!0;;i++,u++){var s,d,f=i<e.length?(typeof e[i])[0]:"";if(u>=r.length||"o"==(d=(typeof(s=r[u]))[0]))return!l||("u"==f?i>n&&!a:""==f!=a);if("u"==d){if(!l||"u"!=f)return!1}else if(l)if(f==d)if(i<=n){if(s!=e[i])return!1}else{if(a?s>e[i]:s<e[i])return!1;s!=e[i]&&(l=!1)}else if("s"!=f&&"n"!=f){if(a||i<=n)return!1;l=!1,i--}else{if(i<=n||d<f!=a)return!1;l=!1}else"s"!=f&&"n"!=f&&(l=!1,i--)}}var p=[],c=p.pop.bind(p);for(u=1;u<e.length;u++){var h=e[u];p.push(1==h?c()|c():2==h?c()&c():h?o(h,r):!c())}return!!c()},u=(e,r)=>{var t=S.S[e];if(!t||!S.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},i=(e,r)=>{var t=e[r];return(r=Object.keys(t).reduce(((e,r)=>!e||n(e,r)?r:e),0))&&t[r]},l=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&n(e,r)?r:e),0)},s=(e,r,t,n)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+a(n)+")",d=(e,r,t,n)=>{var a=l(e,t);return o(n,a)||"undefined"!=typeof console&&console.warn&&console.warn(s(e,t,a,n)),h(e[t][a])},f=(e,r,t)=>{var a=e[r];return(r=Object.keys(a).reduce(((e,r)=>!o(t,r)||e&&!n(e,r)?e:r),0))&&a[r]},p=(e,r,t,n)=>{var o=e[t];return"No satisfying version ("+a(n)+") of shared module "+t+" found in shared scope "+r+".\nAvailable versions: "+Object.keys(o).map((e=>e+" from "+o[e].from)).join(", ")},c=(e,r,t,n)=>{"undefined"!=typeof console&&console.warn&&console.warn(p(e,r,t,n))},h=e=>(e.loaded=1,e.get()),y=(v=e=>function(r,t,n,a){var o=S.I(r);return o&&o.then?o.then(e.bind(e,r,S.S[r],t,n,a)):e(r,S.S[r],t,n,a)})(((e,r,t,n)=>(u(e,t),h(f(r,t,n)||c(r,e,t,n)||i(r,t))))),m=v(((e,r,t,n)=>(u(e,t),d(r,0,t,n)))),b={},g={62:()=>y("default","@jupyterlab/running",[1,3,4,7]),144:()=>y("default","@jupyterlab/cells",[1,3,4,7]),450:()=>m("default","@jupyterlab/codeeditor",[1,3,4,7]),504:()=>m("default","@jupyterlab/rendermime",[1,3,4,7]),524:()=>m("default","@jupyterlab/coreutils",[1,5,4,7]),526:()=>m("default","@lumino/coreutils",[1,1,11,0]),559:()=>m("default","@jupyterlab/markdownviewer",[1,3,4,7]),588:()=>m("default","@jupyterlab/codemirror",[1,3,4,7]),591:()=>m("default","gridstack",[,[1,6,0,0],[1,5,0,0],1]),608:()=>m("default","@jupyterlab/services",[1,6,4,7]),720:()=>m("default","@lumino/messaging",[1,1,10,0]),807:()=>y("default","@jupyterlab/docregistry",[1,3,4,7]),815:()=>y("default","@jupyterlab/outputarea",[1,3,4,7]),822:()=>m("default","@jupyterlab/ui-components",[1,3,4,7]),840:()=>m("default","@lumino/signaling",[1,1,10,0]),854:()=>m("default","@jupyterlab/apputils",[1,3,4,7]),918:()=>m("default","@lumino/algorithm",[1,1,9,0]),931:()=>m("default","@jupyterlab/notebook",[1,3,4,7]),944:()=>m("default","@jupyterlab/launcher",[1,3,4,7]),992:()=>m("default","@lumino/widgets",[1,1,33,0])},j={163:[62,144,450,504,524,526,559,588,591,608,720,807,815,822,840,854,918,931,944,992]},S.f.consumes=(e,r)=>{S.o(j,e)&&j[e].forEach((e=>{if(S.o(b,e))return r.push(b[e]);var t=r=>{b[e]=0,S.m[e]=t=>{delete S.c[e],t.exports=r()}},n=r=>{delete b[e],S.m[e]=t=>{throw delete S.c[e],r}};try{var a=g[e]();a.then?r.push(b[e]=a.then(t).catch(n)):t(a)}catch(e){n(e)}}))},(()=>{var e={176:0};S.f.j=(r,t)=>{var n=S.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else{var a=new Promise(((t,a)=>n=e[r]=[t,a]));t.push(n[2]=a);var o=S.p+S.u(r),u=new Error;S.l(o,(t=>{if(S.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var a=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;u.message="Loading chunk "+r+" failed.\n("+a+": "+o+")",u.name="ChunkLoadError",u.type=a,u.request=o,n[1](u)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,a,[o,u,i]=t,l=0;if(o.some((r=>0!==e[r]))){for(n in u)S.o(u,n)&&(S.m[n]=u[n]);i&&i(S)}for(r&&r(t);l<o.length;l++)a=o[l],S.o(e,a)&&e[a]&&e[a][0](),e[a]=0},t=self.webpackChunkjupyter_app_launcher=self.webpackChunkjupyter_app_launcher||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})(),S.nc=void 0;var k=S(299);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB).jupyter_app_launcher=k})();