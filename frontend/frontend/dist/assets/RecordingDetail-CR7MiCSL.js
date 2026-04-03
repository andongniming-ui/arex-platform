import{ad as ae,i as S,aF as ce,d as L,j as b,k as le,l as P,m as j,n as R,p as x,C as X,o as ne,H as J,D as W,J as oe,r as D,Q as M,as as ue,a6 as me,G as fe,aA as se,a4 as he,ai as pe,L as H,au as ge,a9 as ve,ab as xe,aG as be,aH as Z,a7 as Ce,aI as we,aJ as ye,ah as $e,ax as Ne,aj as je,aK as ee,h as B,w as h,u as m,N as _e,X as F,R as Re,a as g,g as $,U as I,c as Se,Y as ze,F as Ee,B as te,e as Pe,f as k}from"./index-B6ywSR35.js";import{r as K}from"./recordings-DPDrmkoZ.js";import{f as Te}from"./time-DBiNR5Lf.js";import{N as G}from"./Divider-B05FVJWz.js";import{u as Ie}from"./use-message-CpgDv7T6.js";import{N as E,a as ke}from"./DescriptionsItem-DbA1meYf.js";import{N as re}from"./Space-B3nMO6fs.js";import{N as De}from"./DynamicTags-GvBFiDl2.js";import{N as Le}from"./client-CJ4wff5B.js";import"./Add-BNseDRIA.js";function Ae(t,e){const o=ae(ce,null);return S(()=>t.hljs||(o==null?void 0:o.mergedHljsRef.value))}const Be=L({name:"ChevronLeft",render(){return b("svg",{viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg"},b("path",{d:"M10.3536 3.14645C10.5488 3.34171 10.5488 3.65829 10.3536 3.85355L6.20711 8L10.3536 12.1464C10.5488 12.3417 10.5488 12.6583 10.3536 12.8536C10.1583 13.0488 9.84171 13.0488 9.64645 12.8536L5.14645 8.35355C4.95118 8.15829 4.95118 7.84171 5.14645 7.64645L9.64645 3.14645C9.84171 2.95118 10.1583 2.95118 10.3536 3.14645Z",fill:"currentColor"}))}});function He(t){const{textColor2:e,fontSize:o,fontWeightStrong:s,textColor3:r}=t;return{textColor:e,fontSize:o,fontWeightStrong:s,"mono-3":"#a0a1a7","hue-1":"#0184bb","hue-2":"#4078f2","hue-3":"#a626a4","hue-4":"#50a14f","hue-5":"#e45649","hue-5-2":"#c91243","hue-6":"#986801","hue-6-2":"#c18401",lineNumberTextColor:r}}const Fe={common:le,self:He},Me=P([j("code",`
 font-size: var(--n-font-size);
 font-family: var(--n-font-family);
 `,[R("show-line-numbers",`
 display: flex;
 `),x("line-numbers",`
 user-select: none;
 padding-right: 12px;
 text-align: right;
 transition: color .3s var(--n-bezier);
 color: var(--n-line-number-text-color);
 `),R("word-wrap",[P("pre",`
 white-space: pre-wrap;
 word-break: break-all;
 `)]),P("pre",`
 margin: 0;
 line-height: inherit;
 font-size: inherit;
 font-family: inherit;
 `),P("[class^=hljs]",`
 color: var(--n-text-color);
 transition: 
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `)]),({props:t})=>{const e=`${t.bPrefix}code`;return[`${e} .hljs-comment,
 ${e} .hljs-quote {
 color: var(--n-mono-3);
 font-style: italic;
 }`,`${e} .hljs-doctag,
 ${e} .hljs-keyword,
 ${e} .hljs-formula {
 color: var(--n-hue-3);
 }`,`${e} .hljs-section,
 ${e} .hljs-name,
 ${e} .hljs-selector-tag,
 ${e} .hljs-deletion,
 ${e} .hljs-subst {
 color: var(--n-hue-5);
 }`,`${e} .hljs-literal {
 color: var(--n-hue-1);
 }`,`${e} .hljs-string,
 ${e} .hljs-regexp,
 ${e} .hljs-addition,
 ${e} .hljs-attribute,
 ${e} .hljs-meta-string {
 color: var(--n-hue-4);
 }`,`${e} .hljs-built_in,
 ${e} .hljs-class .hljs-title {
 color: var(--n-hue-6-2);
 }`,`${e} .hljs-attr,
 ${e} .hljs-variable,
 ${e} .hljs-template-variable,
 ${e} .hljs-type,
 ${e} .hljs-selector-class,
 ${e} .hljs-selector-attr,
 ${e} .hljs-selector-pseudo,
 ${e} .hljs-number {
 color: var(--n-hue-6);
 }`,`${e} .hljs-symbol,
 ${e} .hljs-bullet,
 ${e} .hljs-link,
 ${e} .hljs-meta,
 ${e} .hljs-selector-id,
 ${e} .hljs-title {
 color: var(--n-hue-2);
 }`,`${e} .hljs-emphasis {
 font-style: italic;
 }`,`${e} .hljs-strong {
 font-weight: var(--n-font-weight-strong);
 }`,`${e} .hljs-link {
 text-decoration: underline;
 }`]}]),We=Object.assign(Object.assign({},W.props),{language:String,code:{type:String,default:""},trim:{type:Boolean,default:!0},hljs:Object,uri:Boolean,inline:Boolean,wordWrap:Boolean,showLineNumbers:Boolean,internalFontSize:Number,internalNoHighlight:Boolean}),Q=L({name:"Code",props:We,setup(t,{slots:e}){const{internalNoHighlight:o}=t,{mergedClsPrefixRef:s,inlineThemeDisabled:r}=X(),n=D(null),p=o?{value:void 0}:Ae(t),w=(d,f,c)=>{const{value:i}=p;return!i||!(d&&i.getLanguage(d))?null:i.highlight(c?f.trim():f,{language:d}).value},N=S(()=>t.inline||t.wordWrap?!1:t.showLineNumbers),v=()=>{if(e.default)return;const{value:d}=n;if(!d)return;const{language:f}=t,c=t.uri?window.decodeURIComponent(t.code):t.code;if(f){const u=w(f,c,t.trim);if(u!==null){if(t.inline)d.innerHTML=u;else{const C=d.querySelector(".__code__");C&&d.removeChild(C);const _=document.createElement("pre");_.className="__code__",_.innerHTML=u,d.appendChild(_)}return}}if(t.inline){d.textContent=c;return}const i=d.querySelector(".__code__");if(i)i.textContent=c;else{const u=document.createElement("pre");u.className="__code__",u.textContent=c,d.innerHTML="",d.appendChild(u)}};ne(v),J(M(t,"language"),v),J(M(t,"code"),v),o||J(p,v);const y=W("Code","-code",Me,Fe,t,s),l=S(()=>{const{common:{cubicBezierEaseInOut:d,fontFamilyMono:f},self:{textColor:c,fontSize:i,fontWeightStrong:u,lineNumberTextColor:C,"mono-3":_,"hue-1":z,"hue-2":T,"hue-3":A,"hue-4":O,"hue-5":U,"hue-5-2":V,"hue-6":q,"hue-6-2":de}}=y.value,{internalFontSize:Y}=t;return{"--n-font-size":Y?`${Y}px`:i,"--n-font-family":f,"--n-font-weight-strong":u,"--n-bezier":d,"--n-text-color":c,"--n-mono-3":_,"--n-hue-1":z,"--n-hue-2":T,"--n-hue-3":A,"--n-hue-4":O,"--n-hue-5":U,"--n-hue-5-2":V,"--n-hue-6":q,"--n-hue-6-2":de,"--n-line-number-text-color":C}}),a=r?oe("code",S(()=>`${t.internalFontSize||"a"}`),l,t):void 0;return{mergedClsPrefix:s,codeRef:n,mergedShowLineNumbers:N,lineNumbers:S(()=>{let d=1;const f=[];let c=!1;for(const i of t.code)i===`
`?(c=!0,f.push(d++)):c=!1;return c||f.push(d++),f.join(`
`)}),cssVars:r?void 0:l,themeClass:a==null?void 0:a.themeClass,onRender:a==null?void 0:a.onRender}},render(){var t,e;const{mergedClsPrefix:o,wordWrap:s,mergedShowLineNumbers:r,onRender:n}=this;return n==null||n(),b("code",{class:[`${o}-code`,this.themeClass,s&&`${o}-code--word-wrap`,r&&`${o}-code--show-line-numbers`],style:this.cssVars,ref:"codeRef"},r?b("pre",{class:`${o}-code__line-numbers`},this.lineNumbers):null,(e=(t=this.$slots).default)===null||e===void 0?void 0:e.call(t))}});function Oe(t){const{fontWeight:e,textColor1:o,textColor2:s,textColorDisabled:r,dividerColor:n,fontSize:p}=t;return{titleFontSize:p,titleFontWeight:e,dividerColor:n,titleTextColor:o,titleTextColorDisabled:r,fontSize:p,textColor:s,arrowColor:s,arrowColorDisabled:r,itemMargin:"16px 0 0 0",titlePadding:"16px 0 0 0"}}const Ue={common:le,self:Oe},Ve=j("collapse","width: 100%;",[j("collapse-item",`
 font-size: var(--n-font-size);
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 margin: var(--n-item-margin);
 `,[R("disabled",[x("header","cursor: not-allowed;",[x("header-main",`
 color: var(--n-title-text-color-disabled);
 `),j("collapse-item-arrow",`
 color: var(--n-arrow-color-disabled);
 `)])]),j("collapse-item","margin-left: 32px;"),P("&:first-child","margin-top: 0;"),P("&:first-child >",[x("header","padding-top: 0;")]),R("left-arrow-placement",[x("header",[j("collapse-item-arrow","margin-right: 4px;")])]),R("right-arrow-placement",[x("header",[j("collapse-item-arrow","margin-left: 4px;")])]),x("content-wrapper",[x("content-inner","padding-top: 16px;"),ue({duration:"0.15s"})]),R("active",[x("header",[R("active",[j("collapse-item-arrow","transform: rotate(90deg);")])])]),P("&:not(:first-child)","border-top: 1px solid var(--n-divider-color);"),me("disabled",[R("trigger-area-main",[x("header",[x("header-main","cursor: pointer;"),j("collapse-item-arrow","cursor: default;")])]),R("trigger-area-arrow",[x("header",[j("collapse-item-arrow","cursor: pointer;")])]),R("trigger-area-extra",[x("header",[x("header-extra","cursor: pointer;")])])]),x("header",`
 font-size: var(--n-title-font-size);
 display: flex;
 flex-wrap: nowrap;
 align-items: center;
 transition: color .3s var(--n-bezier);
 position: relative;
 padding: var(--n-title-padding);
 color: var(--n-title-text-color);
 `,[x("header-main",`
 display: flex;
 flex-wrap: nowrap;
 align-items: center;
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 flex: 1;
 color: var(--n-title-text-color);
 `),x("header-extra",`
 display: flex;
 align-items: center;
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 `),j("collapse-item-arrow",`
 display: flex;
 transition:
 transform .15s var(--n-bezier),
 color .3s var(--n-bezier);
 font-size: 18px;
 color: var(--n-arrow-color);
 `)])])]),qe=Object.assign(Object.assign({},W.props),{defaultExpandedNames:{type:[Array,String],default:null},expandedNames:[Array,String],arrowPlacement:{type:String,default:"left"},accordion:{type:Boolean,default:!1},displayDirective:{type:String,default:"if"},triggerAreas:{type:Array,default:()=>["main","extra","arrow"]},onItemHeaderClick:[Function,Array],"onUpdate:expandedNames":[Function,Array],onUpdateExpandedNames:[Function,Array],onExpandedNamesChange:{type:[Function,Array],validator:()=>!0,default:void 0}}),ie=he("n-collapse"),Je=L({name:"Collapse",props:qe,slots:Object,setup(t,{slots:e}){const{mergedClsPrefixRef:o,inlineThemeDisabled:s,mergedRtlRef:r}=X(t),n=D(t.defaultExpandedNames),p=S(()=>t.expandedNames),w=fe(p,n),N=W("Collapse","-collapse",Ve,Ue,t,o);function v(c){const{"onUpdate:expandedNames":i,onUpdateExpandedNames:u,onExpandedNamesChange:C}=t;u&&H(u,c),i&&H(i,c),C&&H(C,c),n.value=c}function y(c){const{onItemHeaderClick:i}=t;i&&H(i,c)}function l(c,i,u){const{accordion:C}=t,{value:_}=w;if(C)c?(v([i]),y({name:i,expanded:!0,event:u})):(v([]),y({name:i,expanded:!1,event:u}));else if(!Array.isArray(_))v([i]),y({name:i,expanded:!0,event:u});else{const z=_.slice(),T=z.findIndex(A=>i===A);~T?(z.splice(T,1),v(z),y({name:i,expanded:!1,event:u})):(z.push(i),v(z),y({name:i,expanded:!0,event:u}))}}pe(ie,{props:t,mergedClsPrefixRef:o,expandedNamesRef:w,slots:e,toggleItem:l});const a=se("Collapse",r,o),d=S(()=>{const{common:{cubicBezierEaseInOut:c},self:{titleFontWeight:i,dividerColor:u,titlePadding:C,titleTextColor:_,titleTextColorDisabled:z,textColor:T,arrowColor:A,fontSize:O,titleFontSize:U,arrowColorDisabled:V,itemMargin:q}}=N.value;return{"--n-font-size":O,"--n-bezier":c,"--n-text-color":T,"--n-divider-color":u,"--n-title-padding":C,"--n-title-font-size":U,"--n-title-text-color":_,"--n-title-text-color-disabled":z,"--n-title-font-weight":i,"--n-arrow-color":A,"--n-arrow-color-disabled":V,"--n-item-margin":q}}),f=s?oe("collapse",void 0,d,t):void 0;return{rtlEnabled:a,mergedTheme:N,mergedClsPrefix:o,cssVars:s?void 0:d,themeClass:f==null?void 0:f.themeClass,onRender:f==null?void 0:f.onRender}},render(){var t;return(t=this.onRender)===null||t===void 0||t.call(this),b("div",{class:[`${this.mergedClsPrefix}-collapse`,this.rtlEnabled&&`${this.mergedClsPrefix}-collapse--rtl`,this.themeClass],style:this.cssVars},this.$slots)}}),Ke=L({name:"CollapseItemContent",props:{displayDirective:{type:String,required:!0},show:Boolean,clsPrefix:{type:String,required:!0}},setup(t){return{onceTrue:be(M(t,"show"))}},render(){return b(ge,null,{default:()=>{const{show:t,displayDirective:e,onceTrue:o,clsPrefix:s}=this,r=e==="show"&&o,n=b("div",{class:`${s}-collapse-item__content-wrapper`},b("div",{class:`${s}-collapse-item__content-inner`},this.$slots));return r?ve(n,[[xe,t]]):t?n:null}})}}),Ge={title:String,name:[String,Number],disabled:Boolean,displayDirective:String},Qe=L({name:"CollapseItem",props:Ge,setup(t){const{mergedRtlRef:e}=X(t),o=$e(),s=Ne(()=>{var l;return(l=t.name)!==null&&l!==void 0?l:o}),r=ae(ie);r||je("collapse-item","`n-collapse-item` must be placed inside `n-collapse`.");const{expandedNamesRef:n,props:p,mergedClsPrefixRef:w,slots:N}=r,v=S(()=>{const{value:l}=n;if(Array.isArray(l)){const{value:a}=s;return!~l.findIndex(d=>d===a)}else if(l){const{value:a}=s;return a!==l}return!0});return{rtlEnabled:se("Collapse",e,w),collapseSlots:N,randomName:o,mergedClsPrefix:w,collapsed:v,triggerAreas:M(p,"triggerAreas"),mergedDisplayDirective:S(()=>{const{displayDirective:l}=t;return l||p.displayDirective}),arrowPlacement:S(()=>p.arrowPlacement),handleClick(l){let a="main";ee(l,"arrow")&&(a="arrow"),ee(l,"extra")&&(a="extra"),p.triggerAreas.includes(a)&&r&&!t.disabled&&r.toggleItem(v.value,s.value,l)}}},render(){const{collapseSlots:t,$slots:e,arrowPlacement:o,collapsed:s,mergedDisplayDirective:r,mergedClsPrefix:n,disabled:p,triggerAreas:w}=this,N=Z(e.header,{collapsed:s},()=>[this.title]),v=e["header-extra"]||t["header-extra"],y=e.arrow||t.arrow;return b("div",{class:[`${n}-collapse-item`,`${n}-collapse-item--${o}-arrow-placement`,p&&`${n}-collapse-item--disabled`,!s&&`${n}-collapse-item--active`,w.map(l=>`${n}-collapse-item--trigger-area-${l}`)]},b("div",{class:[`${n}-collapse-item__header`,!s&&`${n}-collapse-item__header--active`]},b("div",{class:`${n}-collapse-item__header-main`,onClick:this.handleClick},o==="right"&&N,b("div",{class:`${n}-collapse-item-arrow`,key:this.rtlEnabled?0:1,"data-arrow":!0},Z(y,{collapsed:s},()=>[b(Ce,{clsPrefix:n},{default:()=>this.rtlEnabled?b(Be,null):b(we,null)})])),o==="left"&&N),ye(v,{collapsed:s},l=>b("div",{class:`${n}-collapse-item__header-extra`,onClick:this.handleClick,"data-extra":!0},l))),b(Ke,{clsPrefix:n,displayDirective:r,show:!s},e))}}),st=L({__name:"RecordingDetail",setup(t){const e=Re(),o=Pe(),s=Ie(),r=D(null),n=D(!1),p=D(!1),w=D([]);async function N(l){if(r.value){p.value=!0;try{const a=await K.updateTags(r.value.id,l);r.value=a.data,s.success("标签已保存")}catch{s.error("保存失败")}finally{p.value=!1}}}async function v(){var l,a;n.value=!0;try{const d=await K.recapture(e.params.id);r.value=d.data,s.success("基线响应已更新")}catch(d){s.error(((a=(l=d.response)==null?void 0:l.data)==null?void 0:a.detail)||"捕获失败")}finally{n.value=!1}}function y(l){if(!l)return"";try{return JSON.stringify(JSON.parse(l),null,2)}catch{return l}}return ne(async()=>{const l=await K.get(e.params.id);r.value=l.data,w.value=l.data.tags||[]}),(l,a)=>{var d,f;return r.value?(k(),B(m(_e),{key:0,title:`录制详情 — ${((d=r.value)==null?void 0:d.entry_type)||""} ${((f=r.value)==null?void 0:f.path)||""}`},{"header-extra":h(()=>[g(m(re),null,{default:h(()=>[g(m(te),{size:"small",loading:n.value,onClick:v},{default:h(()=>[...a[2]||(a[2]=[$("重新捕获基线",-1)])]),_:1},8,["loading"]),g(m(te),{size:"small",onClick:a[0]||(a[0]=c=>m(o).back())},{default:h(()=>[...a[3]||(a[3]=[$("返回",-1)])]),_:1})]),_:1})]),default:h(()=>{var c,i;return[g(m(ke),{bordered:"",column:2},{default:h(()=>[g(m(E),{label:"TraceId"},{default:h(()=>[$(I(r.value.trace_id||"-"),1)]),_:1}),g(m(E),{label:"应用"},{default:h(()=>[$(I(r.value.entry_app||"-"),1)]),_:1}),g(m(E),{label:"Host"},{default:h(()=>[$(I(r.value.host||"-"),1)]),_:1}),g(m(E),{label:"耗时"},{default:h(()=>[$(I(r.value.duration_ms?r.value.duration_ms+"ms":"-"),1)]),_:1}),g(m(E),{label:"时间"},{default:h(()=>[$(I(m(Te)(r.value.timestamp||r.value.created_at)),1)]),_:1}),g(m(E),{label:"状态"},{default:h(()=>[$(I(r.value.status),1)]),_:1}),g(m(E),{label:"标签",span:2},{default:h(()=>[g(m(re),{align:"center"},{default:h(()=>[g(m(De),{value:w.value,"onUpdate:value":[a[1]||(a[1]=u=>w.value=u),N]},null,8,["value"]),p.value?(k(),B(m(Le),{key:0,size:"small",type:"info"},{default:h(()=>[...a[4]||(a[4]=[$("保存中…",-1)])]),_:1})):F("",!0)]),_:1})]),_:1})]),_:1}),g(m(G),null,{default:h(()=>[...a[5]||(a[5]=[$("请求报文",-1)])]),_:1}),g(m(Q),{code:y(r.value.request_body),language:"json","show-line-numbers":""},null,8,["code"]),g(m(G),null,{default:h(()=>[...a[6]||(a[6]=[$("响应报文",-1)])]),_:1}),g(m(Q),{code:y(r.value.response_body),language:"json","show-line-numbers":""},null,8,["code"]),(c=r.value.sub_invocations)!=null&&c.length?(k(),B(m(G),{key:0},{default:h(()=>[...a[7]||(a[7]=[$("子调用 (Mock)",-1)])]),_:1})):F("",!0),(i=r.value.sub_invocations)!=null&&i.length?(k(),B(m(Je),{key:1},{default:h(()=>[(k(!0),Se(Ee,null,ze(r.value.sub_invocations,(u,C)=>(k(),B(m(Qe),{key:C,title:`Sub #${C+1} — ${u.type||u.invokeType||"UNKNOWN"}`},{default:h(()=>[g(m(Q),{code:JSON.stringify(u,null,2),language:"json","show-line-numbers":""},null,8,["code"])]),_:2},1032,["title"]))),128))]),_:1})):F("",!0)]}),_:1},8,["title"])):F("",!0)}}});export{st as default};
