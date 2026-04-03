import{k as xa,l as be,m as v,n as H,p as De,q as Xe,s as _a,t as ka,v as Sa,d as na,j as _,x as Ca,V as za,y as Ra,z as Da,A as We,T as Ta,C as Na,D as sa,E as Aa,r as m,G as Va,H as qe,I as ra,J as Ge,K as Ea,i as B,L as Te,M as Ne,O as Ae,P as Ye,Q as Ha,o as Ma,h as le,w as r,u as o,R as $a,S as Ia,N as ye,a as n,g as y,U as A,B as k,W as we,X as Qe,c as Ze,Y as Ua,F as ea,b as Ba,e as ja,f as P}from"./index-B6ywSR35.js";import{a as Q}from"./applications-Btmv_8_S.js";import{c as Ve,s as xe}from"./recordings-DPDrmkoZ.js";import{f as Ee}from"./time-DBiNR5Lf.js";import{N as O,a as Fa}from"./DescriptionsItem-DbA1meYf.js";import{N as Pa}from"./DynamicTags-GvBFiDl2.js";import{N as Oa}from"./Alert-B-OjpZ2f.js";import{a as aa,N as Ka,b as La}from"./DataTable-C-vr6xbd.js";import{u as Ya}from"./use-message-CpgDv7T6.js";import{N as K,a as L}from"./Space-B3nMO6fs.js";import{N as ta}from"./client-CJ4wff5B.js";import{N as Je,a as M}from"./FormItem-BC7p258p.js";import{N as He}from"./InputNumber-6LzjK-Fb.js";import"./Add-BNseDRIA.js";const Ja={railHeight:"4px",railWidthVertical:"4px",handleSize:"18px",dotHeight:"8px",dotWidth:"8px",dotBorderRadius:"4px"};function Wa(d){const p="rgba(0, 0, 0, .85)",j="0 2px 8px 0 rgba(0, 0, 0, 0.12)",{railColor:u,primaryColor:g,baseColor:h,cardColor:c,modalColor:D,popoverColor:I,borderRadius:Y,fontSize:Z,opacityDisabled:S}=d;return Object.assign(Object.assign({},Ja),{fontSize:Z,markFontSize:Z,railColor:u,railColorHover:u,fillColor:g,fillColorHover:g,opacityDisabled:S,handleColor:"#FFF",dotColor:c,dotColorModal:D,dotColorPopover:I,handleBoxShadow:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",handleBoxShadowHover:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",handleBoxShadowActive:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",handleBoxShadowFocus:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",indicatorColor:p,indicatorBoxShadow:j,indicatorTextColor:h,indicatorBorderRadius:Y,dotBorder:`2px solid ${u}`,dotBorderActive:`2px solid ${g}`,dotBoxShadow:""})}const Xa={common:xa,self:Wa},qa=be([v("slider",`
 display: block;
 padding: calc((var(--n-handle-size) - var(--n-rail-height)) / 2) 0;
 position: relative;
 z-index: 0;
 width: 100%;
 cursor: pointer;
 user-select: none;
 -webkit-user-select: none;
 `,[H("reverse",[v("slider-handles",[v("slider-handle-wrapper",`
 transform: translate(50%, -50%);
 `)]),v("slider-dots",[v("slider-dot",`
 transform: translateX(50%, -50%);
 `)]),H("vertical",[v("slider-handles",[v("slider-handle-wrapper",`
 transform: translate(-50%, -50%);
 `)]),v("slider-marks",[v("slider-mark",`
 transform: translateY(calc(-50% + var(--n-dot-height) / 2));
 `)]),v("slider-dots",[v("slider-dot",`
 transform: translateX(-50%) translateY(0);
 `)])])]),H("vertical",`
 box-sizing: content-box;
 padding: 0 calc((var(--n-handle-size) - var(--n-rail-height)) / 2);
 width: var(--n-rail-width-vertical);
 height: 100%;
 `,[v("slider-handles",`
 top: calc(var(--n-handle-size) / 2);
 right: 0;
 bottom: calc(var(--n-handle-size) / 2);
 left: 0;
 `,[v("slider-handle-wrapper",`
 top: unset;
 left: 50%;
 transform: translate(-50%, 50%);
 `)]),v("slider-rail",`
 height: 100%;
 `,[De("fill",`
 top: unset;
 right: 0;
 bottom: unset;
 left: 0;
 `)]),H("with-mark",`
 width: var(--n-rail-width-vertical);
 margin: 0 32px 0 8px;
 `),v("slider-marks",`
 top: calc(var(--n-handle-size) / 2);
 right: unset;
 bottom: calc(var(--n-handle-size) / 2);
 left: 22px;
 font-size: var(--n-mark-font-size);
 `,[v("slider-mark",`
 transform: translateY(50%);
 white-space: nowrap;
 `)]),v("slider-dots",`
 top: calc(var(--n-handle-size) / 2);
 right: unset;
 bottom: calc(var(--n-handle-size) / 2);
 left: 50%;
 `,[v("slider-dot",`
 transform: translateX(-50%) translateY(50%);
 `)])]),H("disabled",`
 cursor: not-allowed;
 opacity: var(--n-opacity-disabled);
 `,[v("slider-handle",`
 cursor: not-allowed;
 `)]),H("with-mark",`
 width: 100%;
 margin: 8px 0 32px 0;
 `),be("&:hover",[v("slider-rail",{backgroundColor:"var(--n-rail-color-hover)"},[De("fill",{backgroundColor:"var(--n-fill-color-hover)"})]),v("slider-handle",{boxShadow:"var(--n-handle-box-shadow-hover)"})]),H("active",[v("slider-rail",{backgroundColor:"var(--n-rail-color-hover)"},[De("fill",{backgroundColor:"var(--n-fill-color-hover)"})]),v("slider-handle",{boxShadow:"var(--n-handle-box-shadow-hover)"})]),v("slider-marks",`
 position: absolute;
 top: 18px;
 left: calc(var(--n-handle-size) / 2);
 right: calc(var(--n-handle-size) / 2);
 `,[v("slider-mark",`
 position: absolute;
 transform: translateX(-50%);
 white-space: nowrap;
 `)]),v("slider-rail",`
 width: 100%;
 position: relative;
 height: var(--n-rail-height);
 background-color: var(--n-rail-color);
 transition: background-color .3s var(--n-bezier);
 border-radius: calc(var(--n-rail-height) / 2);
 `,[De("fill",`
 position: absolute;
 top: 0;
 bottom: 0;
 border-radius: calc(var(--n-rail-height) / 2);
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-fill-color);
 `)]),v("slider-handles",`
 position: absolute;
 top: 0;
 right: calc(var(--n-handle-size) / 2);
 bottom: 0;
 left: calc(var(--n-handle-size) / 2);
 `,[v("slider-handle-wrapper",`
 outline: none;
 position: absolute;
 top: 50%;
 transform: translate(-50%, -50%);
 cursor: pointer;
 display: flex;
 `,[v("slider-handle",`
 height: var(--n-handle-size);
 width: var(--n-handle-size);
 border-radius: 50%;
 overflow: hidden;
 transition: box-shadow .2s var(--n-bezier), background-color .3s var(--n-bezier);
 background-color: var(--n-handle-color);
 box-shadow: var(--n-handle-box-shadow);
 `,[be("&:hover",`
 box-shadow: var(--n-handle-box-shadow-hover);
 `)]),be("&:focus",[v("slider-handle",`
 box-shadow: var(--n-handle-box-shadow-focus);
 `,[be("&:hover",`
 box-shadow: var(--n-handle-box-shadow-active);
 `)])])])]),v("slider-dots",`
 position: absolute;
 top: 50%;
 left: calc(var(--n-handle-size) / 2);
 right: calc(var(--n-handle-size) / 2);
 `,[H("transition-disabled",[v("slider-dot","transition: none;")]),v("slider-dot",`
 transition:
 border-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 position: absolute;
 transform: translate(-50%, -50%);
 height: var(--n-dot-height);
 width: var(--n-dot-width);
 border-radius: var(--n-dot-border-radius);
 overflow: hidden;
 box-sizing: border-box;
 border: var(--n-dot-border);
 background-color: var(--n-dot-color);
 `,[H("active","border: var(--n-dot-border-active);")])])]),v("slider-handle-indicator",`
 font-size: var(--n-font-size);
 padding: 6px 10px;
 border-radius: var(--n-indicator-border-radius);
 color: var(--n-indicator-text-color);
 background-color: var(--n-indicator-color);
 box-shadow: var(--n-indicator-box-shadow);
 `,[Xe()]),v("slider-handle-indicator",`
 font-size: var(--n-font-size);
 padding: 6px 10px;
 border-radius: var(--n-indicator-border-radius);
 color: var(--n-indicator-text-color);
 background-color: var(--n-indicator-color);
 box-shadow: var(--n-indicator-box-shadow);
 `,[H("top",`
 margin-bottom: 12px;
 `),H("right",`
 margin-left: 12px;
 `),H("bottom",`
 margin-top: 12px;
 `),H("left",`
 margin-right: 12px;
 `),Xe()]),_a(v("slider",[v("slider-dot","background-color: var(--n-dot-color-modal);")])),ka(v("slider",[v("slider-dot","background-color: var(--n-dot-color-popover);")]))]);function la(d){return window.TouchEvent&&d instanceof window.TouchEvent}function oa(){const d=new Map,p=j=>u=>{d.set(j,u)};return Sa(()=>{d.clear()}),[d,p]}const Ga=0,Qa=Object.assign(Object.assign({},sa.props),{to:We.propTo,defaultValue:{type:[Number,Array],default:0},marks:Object,disabled:{type:Boolean,default:void 0},formatTooltip:Function,keyboard:{type:Boolean,default:!0},min:{type:Number,default:0},max:{type:Number,default:100},step:{type:[Number,String],default:1},range:Boolean,value:[Number,Array],placement:String,showTooltip:{type:Boolean,default:void 0},tooltip:{type:Boolean,default:!0},vertical:Boolean,reverse:Boolean,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onDragstart:[Function],onDragend:[Function]}),Za=na({name:"Slider",props:Qa,slots:Object,setup(d){const{mergedClsPrefixRef:p,namespaceRef:j,inlineThemeDisabled:u}=Na(d),g=sa("Slider","-slider",qa,Xa,d,p),h=m(null),[c,D]=oa(),[I,Y]=oa(),Z=m(new Set),S=Aa(d),{mergedDisabledRef:J}=S,oe=B(()=>{const{step:a}=d;if(Number(a)<=0||a==="mark")return 0;const t=a.toString();let i=0;return t.includes(".")&&(i=t.length-t.indexOf(".")-1),i}),ee=m(d.defaultValue),fe=Ha(d,"value"),ae=Va(fe,ee),T=B(()=>{const{value:a}=ae;return(d.range?a:[a]).map(Ce)}),ne=B(()=>T.value.length>2),te=B(()=>d.placement===void 0?d.vertical?"right":"top":d.placement),se=B(()=>{const{marks:a}=d;return a?Object.keys(a).map(Number.parseFloat):null}),C=m(-1),W=m(-1),V=m(-1),$=m(!1),X=m(!1),he=B(()=>{const{vertical:a,reverse:t}=d;return a?t?"top":"bottom":t?"right":"left"}),Me=B(()=>{if(ne.value)return;const a=T.value,t=re(d.range?Math.min(...a):d.min),i=re(d.range?Math.max(...a):a[0]),{value:f}=he;return d.vertical?{[f]:`${t}%`,height:`${i-t}%`}:{[f]:`${t}%`,width:`${i-t}%`}}),$e=B(()=>{const a=[],{marks:t}=d;if(t){const i=T.value.slice();i.sort((N,R)=>N-R);const{value:f}=he,{value:b}=ne,{range:z}=d,U=b?()=>!1:N=>z?N>=i[0]&&N<=i[i.length-1]:N<=i[0];for(const N of Object.keys(t)){const R=Number(N);a.push({active:U(R),key:R,label:t[N],style:{[f]:`${re(R)}%`}})}}return a});function Ie(a,t){const i=re(a),{value:f}=he;return{[f]:`${i}%`,zIndex:t===C.value?1:0}}function _e(a){return d.showTooltip||V.value===a||C.value===a&&$.value}function Ue(a){return $.value?!(C.value===a&&W.value===a):!0}function w(a){var t;~a&&(C.value=a,(t=c.get(a))===null||t===void 0||t.focus())}function Be(){I.forEach((a,t)=>{_e(t)&&a.syncPosition()})}function ke(a){const{"onUpdate:value":t,onUpdateValue:i}=d,{nTriggerFormInput:f,nTriggerFormChange:b}=S;i&&Te(i,a),t&&Te(t,a),ee.value=a,f(),b()}function Se(a){const{range:t}=d;if(t){if(Array.isArray(a)){const{value:i}=T;a.join()!==i.join()&&ke(a)}}else Array.isArray(a)||T.value[0]!==a&&ke(a)}function pe(a,t){if(d.range){const i=T.value.slice();i.splice(t,1,a),Se(i)}else Se(a)}function me(a,t,i){const f=i!==void 0;i||(i=a-t>0?1:-1);const b=se.value||[],{step:z}=d;if(z==="mark"){const R=de(a,b.concat(t),f?i:void 0);return R?R.value:t}if(z<=0)return t;const{value:U}=oe;let N;if(f){const R=Number((t/z).toFixed(U)),G=Math.floor(R),Ke=R>G?G:G-1,Le=R<G?G:G+1;N=de(t,[Number((Ke*z).toFixed(U)),Number((Le*z).toFixed(U)),...b],i)}else{const R=je(a);N=de(a,[...b,R])}return N?Ce(N.value):t}function Ce(a){return Math.min(d.max,Math.max(d.min,a))}function re(a){const{max:t,min:i}=d;return(a-i)/(t-i)*100}function ie(a){const{max:t,min:i}=d;return i+(t-i)*a}function je(a){const{step:t,min:i}=d;if(Number(t)<=0||t==="mark")return a;const f=Math.round((a-i)/t)*t+i;return Number(f.toFixed(oe.value))}function de(a,t=se.value,i){if(!(t!=null&&t.length))return null;let f=null,b=-1;for(;++b<t.length;){const z=t[b]-a,U=Math.abs(z);(i===void 0||z*i>0)&&(f===null||U<f.distance)&&(f={index:b,distance:U,value:t[b]})}return f}function ze(a){const t=h.value;if(!t)return;const i=la(a)?a.touches[0]:a,f=t.getBoundingClientRect();let b;return d.vertical?b=(f.bottom-i.clientY)/f.height:b=(i.clientX-f.left)/f.width,d.reverse&&(b=1-b),ie(b)}function Fe(a){if(J.value||!d.keyboard)return;const{vertical:t,reverse:i}=d;switch(a.key){case"ArrowUp":a.preventDefault(),ue(t&&i?-1:1);break;case"ArrowRight":a.preventDefault(),ue(!t&&i?-1:1);break;case"ArrowDown":a.preventDefault(),ue(t&&i?1:-1);break;case"ArrowLeft":a.preventDefault(),ue(!t&&i?1:-1);break}}function ue(a){const t=C.value;if(t===-1)return;const{step:i}=d,f=T.value[t],b=Number(i)<=0||i==="mark"?f:f+i*a;pe(me(b,f,a>0?1:-1),t)}function Pe(a){var t,i;if(J.value||!la(a)&&a.button!==Ga)return;const f=ze(a);if(f===void 0)return;const b=T.value.slice(),z=d.range?(i=(t=de(f,b))===null||t===void 0?void 0:t.index)!==null&&i!==void 0?i:-1:0;z!==-1&&(a.preventDefault(),w(z),Oe(),pe(me(f,T.value[z]),z))}function Oe(){$.value||($.value=!0,d.onDragstart&&Te(d.onDragstart),Ne("touchend",document,e),Ne("mouseup",document,e),Ne("touchmove",document,s),Ne("mousemove",document,s))}function ce(){$.value&&($.value=!1,d.onDragend&&Te(d.onDragend),Ae("touchend",document,e),Ae("mouseup",document,e),Ae("touchmove",document,s),Ae("mousemove",document,s))}function s(a){const{value:t}=C;if(!$.value||t===-1){ce();return}const i=ze(a);i!==void 0&&pe(me(i,T.value[t]),t)}function e(){ce()}function l(a){C.value=a,J.value||(V.value=a)}function x(a){C.value===a&&(C.value=-1,ce()),V.value===a&&(V.value=-1)}function E(a){V.value=a}function ge(a){V.value===a&&(V.value=-1)}qe(C,(a,t)=>void Ye(()=>W.value=t)),qe(ae,()=>{if(d.marks){if(X.value)return;X.value=!0,Ye(()=>{X.value=!1})}Ye(Be)}),ra(()=>{ce()});const q=B(()=>{const{self:{markFontSize:a,railColor:t,railColorHover:i,fillColor:f,fillColorHover:b,handleColor:z,opacityDisabled:U,dotColor:N,dotColorModal:R,handleBoxShadow:G,handleBoxShadowHover:Ke,handleBoxShadowActive:Le,handleBoxShadowFocus:ia,dotBorder:da,dotBoxShadow:ua,railHeight:ca,railWidthVertical:va,handleSize:fa,dotHeight:ha,dotWidth:pa,dotBorderRadius:ma,fontSize:ga,dotBorderActive:ba,dotColorPopover:ya},common:{cubicBezierEaseInOut:wa}}=g.value;return{"--n-bezier":wa,"--n-dot-border":da,"--n-dot-border-active":ba,"--n-dot-border-radius":ma,"--n-dot-box-shadow":ua,"--n-dot-color":N,"--n-dot-color-modal":R,"--n-dot-color-popover":ya,"--n-dot-height":ha,"--n-dot-width":pa,"--n-fill-color":f,"--n-fill-color-hover":b,"--n-font-size":ga,"--n-handle-box-shadow":G,"--n-handle-box-shadow-active":Le,"--n-handle-box-shadow-focus":ia,"--n-handle-box-shadow-hover":Ke,"--n-handle-color":z,"--n-handle-size":fa,"--n-opacity-disabled":U,"--n-rail-color":t,"--n-rail-color-hover":i,"--n-rail-height":ca,"--n-rail-width-vertical":va,"--n-mark-font-size":a}}),F=u?Ge("slider",void 0,q,d):void 0,Re=B(()=>{const{self:{fontSize:a,indicatorColor:t,indicatorBoxShadow:i,indicatorTextColor:f,indicatorBorderRadius:b}}=g.value;return{"--n-font-size":a,"--n-indicator-border-radius":b,"--n-indicator-box-shadow":i,"--n-indicator-color":t,"--n-indicator-text-color":f}}),ve=u?Ge("slider-indicator",void 0,Re,d):void 0;return{mergedClsPrefix:p,namespace:j,uncontrolledValue:ee,mergedValue:ae,mergedDisabled:J,mergedPlacement:te,isMounted:Ea(),adjustedTo:We(d),dotTransitionDisabled:X,markInfos:$e,isShowTooltip:_e,shouldKeepTooltipTransition:Ue,handleRailRef:h,setHandleRefs:D,setFollowerRefs:Y,fillStyle:Me,getHandleStyle:Ie,activeIndex:C,arrifiedValues:T,followerEnabledIndexSet:Z,handleRailMouseDown:Pe,handleHandleFocus:l,handleHandleBlur:x,handleHandleMouseEnter:E,handleHandleMouseLeave:ge,handleRailKeyDown:Fe,indicatorCssVars:u?void 0:Re,indicatorThemeClass:ve==null?void 0:ve.themeClass,indicatorOnRender:ve==null?void 0:ve.onRender,cssVars:u?void 0:q,themeClass:F==null?void 0:F.themeClass,onRender:F==null?void 0:F.onRender}},render(){var d;const{mergedClsPrefix:p,themeClass:j,formatTooltip:u}=this;return(d=this.onRender)===null||d===void 0||d.call(this),_("div",{class:[`${p}-slider`,j,{[`${p}-slider--disabled`]:this.mergedDisabled,[`${p}-slider--active`]:this.activeIndex!==-1,[`${p}-slider--with-mark`]:this.marks,[`${p}-slider--vertical`]:this.vertical,[`${p}-slider--reverse`]:this.reverse}],style:this.cssVars,onKeydown:this.handleRailKeyDown,onMousedown:this.handleRailMouseDown,onTouchstart:this.handleRailMouseDown},_("div",{class:`${p}-slider-rail`},_("div",{class:`${p}-slider-rail__fill`,style:this.fillStyle}),this.marks?_("div",{class:[`${p}-slider-dots`,this.dotTransitionDisabled&&`${p}-slider-dots--transition-disabled`]},this.markInfos.map(g=>_("div",{key:g.key,class:[`${p}-slider-dot`,{[`${p}-slider-dot--active`]:g.active}],style:g.style}))):null,_("div",{ref:"handleRailRef",class:`${p}-slider-handles`},this.arrifiedValues.map((g,h)=>{const c=this.isShowTooltip(h);return _(Ca,null,{default:()=>[_(za,null,{default:()=>_("div",{ref:this.setHandleRefs(h),class:`${p}-slider-handle-wrapper`,tabindex:this.mergedDisabled?-1:0,role:"slider","aria-valuenow":g,"aria-valuemin":this.min,"aria-valuemax":this.max,"aria-orientation":this.vertical?"vertical":"horizontal","aria-disabled":this.disabled,style:this.getHandleStyle(g,h),onFocus:()=>{this.handleHandleFocus(h)},onBlur:()=>{this.handleHandleBlur(h)},onMouseenter:()=>{this.handleHandleMouseEnter(h)},onMouseleave:()=>{this.handleHandleMouseLeave(h)}},Ra(this.$slots.thumb,()=>[_("div",{class:`${p}-slider-handle`})]))}),this.tooltip&&_(Da,{ref:this.setFollowerRefs(h),show:c,to:this.adjustedTo,enabled:this.showTooltip&&!this.range||this.followerEnabledIndexSet.has(h),teleportDisabled:this.adjustedTo===We.tdkey,placement:this.mergedPlacement,containerClass:this.namespace},{default:()=>_(Ta,{name:"fade-in-scale-up-transition",appear:this.isMounted,css:this.shouldKeepTooltipTransition(h),onEnter:()=>{this.followerEnabledIndexSet.add(h)},onAfterLeave:()=>{this.followerEnabledIndexSet.delete(h)}},{default:()=>{var D;return c?((D=this.indicatorOnRender)===null||D===void 0||D.call(this),_("div",{class:[`${p}-slider-handle-indicator`,this.indicatorThemeClass,`${p}-slider-handle-indicator--${this.mergedPlacement}`],style:this.indicatorCssVars},typeof u=="function"?u(g):g)):null}})})]})})),this.marks?_("div",{class:`${p}-slider-marks`},this.markInfos.map(g=>_("div",{key:g.key,class:`${p}-slider-mark`,style:g.style},typeof g.label=="function"?g.label():g.label))):null))}}),et={style:{"min-width":"40px"}},at={style:{"font-size":"13px",color:"#666"}},mt=na({__name:"ApplicationDetail",setup(d){const p=$a(),j=ja(),u=Ya(),g=new Set;ra(()=>{g.forEach(clearInterval),g.clear()});const h=p.params.id,c=m(null),D=m(""),I=m([]),Y=m(!1),Z=m(0),S=Ia({page:1,pageSize:20,itemCount:0}),J=m(!1),oe=m(!1),ee=m(!1),fe=m(!1),ae=m(!1),T=m(!1),ne=m(!1),te=m(!1),se=m(!1),C=m(100),W=m([]),V=m([]),$=m(void 0),X=m(!1),he=[{label:"删除字段 (remove)",value:"remove"},{label:"替换为*** (mask)",value:"mask"},{label:"部分遮盖 (partial)",value:"partial"},{label:"哈希摘要 (hash)",value:"hash"}];function Me(){W.value.push({field:"",action:"mask"})}function $e(s){W.value.splice(s,1)}async function Ie(){var s,e;X.value=!0;try{const l=await Q.update(h,{default_ignore_fields:V.value.length?V.value:void 0,default_perf_threshold_ms:$.value||void 0});c.value=l.data,u.success("回放默认配置已保存")}catch(l){u.error(((e=(s=l.response)==null?void 0:s.data)==null?void 0:e.detail)||"保存失败")}finally{X.value=!1}}async function _e(){var s,e;T.value=!0;try{const l=await Q.update(h,{sample_rate:C.value/100,desensitize_rules:W.value.filter(x=>x.field)});c.value=l.data,u.success("录制控制配置已保存")}catch(l){u.error(((e=(s=l.response)==null?void 0:s.data)==null?void 0:e.detail)||"保存失败")}finally{T.value=!1}}const Ue=[{label:"SSH Key",value:"KEY"},{label:"密码",value:"PASSWORD"}],w=m({ssh_host:"",ssh_user:"",ssh_auth_type:"KEY",ssh_key_path:"",ssh_password:"",java_jar_name:"",repeater_port:8080,sandbox_home:"",repeater_data_dir:""});function Be(){c.value&&(w.value={ssh_host:c.value.ssh_host,ssh_user:c.value.ssh_user,ssh_auth_type:c.value.ssh_auth_type||"KEY",ssh_key_path:c.value.ssh_key_path||"",ssh_password:c.value.ssh_password||"",java_jar_name:c.value.java_jar_name||"",repeater_port:c.value.repeater_port??9001,sandbox_home:c.value.sandbox_home||"/home/test/.sandbox",repeater_data_dir:c.value.repeater_data_dir||"/home/test/.sandbox-module/repeater-data/record"},te.value=!0)}async function ke(){var s,e;se.value=!0;try{const l={...w.value};l.ssh_key_path||delete l.ssh_key_path,l.ssh_password||delete l.ssh_password;const x=await Q.update(h,l);c.value=x.data,u.success("应用更新成功"),te.value=!1}catch(l){u.error(((e=(s=l.response)==null?void 0:s.data)==null?void 0:e.detail)||"更新失败")}finally{se.value=!1}}const Se={ATTACHED:"success",DETACHED:"warning",ERROR:"error",UNKNOWN:"default"},pe=[{title:"名称",key:"name",render:s=>s.name||Ee(s.started_at)},{title:"状态",key:"status",render:s=>_(ta,{type:s.status==="ACTIVE"?"success":s.status==="ERROR"?"error":"default",size:"small"},()=>s.status)},{title:"录制数",key:"record_count"},{title:"开始时间",key:"started_at",render:s=>Ee(s.started_at)},{title:"操作",key:"actions",render:s=>_(K,{size:"small"},()=>[s.status==="ACTIVE"?_(k,{size:"small",type:"warning",onClick:()=>me(s)},()=>"停止"):null,_(k,{size:"small",onClick:()=>j.push(`/recording?session_id=${s.id}&app_id=${h}`)},()=>"查看录制"),_(k,{size:"small",type:"error",onClick:()=>Ce(s)},()=>"删除")])}];async function me(s){var e,l;try{await xe.stop(s.id),u.success("录制已停止，正在收集数据...");let x=0;const E=150,ge=setInterval(async()=>{x++;const q=await xe.get(s.id),F=I.value.findIndex(Re=>Re.id===s.id);F!==-1&&(I.value[F]=q.data),(q.data.status==="DONE"||q.data.status==="ERROR"||x>=E)&&(clearInterval(ge),g.delete(ge),q.data.status==="DONE"?u.success(`数据收集完成，共 ${q.data.record_count} 条录制`):x>=E?u.warning("数据收集超时，请手动刷新页面查看结果"):u.error("数据收集失败，请检查 SSH 和录制目录配置"))},2e3);g.add(ge)}catch(x){u.error(((l=(e=x.response)==null?void 0:e.data)==null?void 0:l.detail)||"停止失败")}}async function Ce(s){var e,l;if(s.status==="ACTIVE"){u.warning("请先停止录制再删除");return}try{await xe.delete(s.id),I.value=I.value.filter(x=>x.id!==s.id),u.success("会话已删除")}catch(x){u.error(((l=(e=x.response)==null?void 0:e.data)==null?void 0:l.detail)||"删除失败")}}async function re(){const s=await Q.get(h);c.value=s.data,C.value=Math.round((s.data.sample_rate??1)*100),W.value=(s.data.desensitize_rules??[]).map(e=>({...e})),V.value=[...s.data.default_ignore_fields??[]],$.value=s.data.default_perf_threshold_ms??void 0;try{const e=await Ve.get(h);D.value=e.data.config_json}catch{}await ie()}async function ie(){Y.value=!0;try{const s=(S.page-1)*S.pageSize,e=await xe.list(h,S.pageSize,s);I.value=e.data.items,Z.value=e.data.total,S.itemCount=e.data.total}finally{Y.value=!1}}async function je(){const s=await Ve.getDefault(h);D.value=JSON.stringify(s.data.config,null,2)}async function de(){J.value=!0;try{const s=await Q.sshTest(h);s.data.success?u.success(`SSH 连通: ${s.data.message}`):u.error(`SSH 失败: ${s.data.message}`)}finally{J.value=!1}}async function ze(){oe.value=!0;try{const s=await Q.discoverPid(h);s.data.pid?(u.success(`PID: ${s.data.pid}`),c.value.java_pid=s.data.pid):u.warning("未找到 JVM 进程，请确认 java_jar_name 配置")}finally{oe.value=!1}}async function Fe(){var s,e;ee.value=!0;try{const l=await Q.attachAgent(h);u.success(`Agent ${l.data.agent_status}`),c.value.agent_status=l.data.agent_status}catch(l){u.error(((e=(s=l.response)==null?void 0:s.data)==null?void 0:e.detail)||"挂载失败")}finally{ee.value=!1}}async function ue(){fe.value=!0;try{await Q.detachAgent(h),u.success("Agent 已卸载"),c.value.agent_status="DETACHED"}finally{fe.value=!1}}async function Pe(){var s,e;if(!D.value.trim()){u.warning("配置内容为空，请先点击「加载默认」");return}try{JSON.parse(D.value)}catch{u.error("配置内容不是合法的 JSON，请检查格式");return}ae.value=!0;try{await Ve.upsert(h,{config_json:D.value}),u.success("配置已保存")}catch(l){u.error(((e=(s=l.response)==null?void 0:s.data)==null?void 0:e.detail)||"保存失败，请检查后端日志")}finally{ae.value=!1}}async function Oe(){var s,e;ne.value=!0;try{await Ve.push(h),u.success("配置已推送到目标主机")}catch(l){const x=((e=(s=l.response)==null?void 0:s.data)==null?void 0:e.detail)||"";x.includes("No config")?u.error("请先点击「保存」将配置存入数据库，再推送"):u.error(x||"推送失败，请检查后端日志")}finally{ne.value=!1}}async function ce(){var e;const s=await xe.create({app_id:h,name:`${((e=c.value)==null?void 0:e.name)??"录制"}_${new Date().toLocaleTimeString()}`});u.success(`录制会话已创建: ${s.data.name||Ee(s.data.started_at)}`),S.page=1,await ie()}return Ma(re),(s,e)=>(P(),le(o(K),{vertical:"",size:16},{default:r(()=>[c.value?(P(),le(o(ye),{key:0},{header:r(()=>[n(o(K),{align:"center"},{default:r(()=>[we("span",null,A(c.value.name),1),n(o(ta),{type:Se[c.value.agent_status]||"default",size:"small"},{default:r(()=>[y(A(c.value.agent_status),1)]),_:1},8,["type"])]),_:1})]),"header-extra":r(()=>[n(o(K),null,{default:r(()=>[n(o(k),{size:"small",onClick:Be},{default:r(()=>[...e[18]||(e[18]=[y("编辑应用",-1)])]),_:1}),n(o(k),{size:"small",onClick:de,loading:J.value},{default:r(()=>[...e[19]||(e[19]=[y("测试 SSH",-1)])]),_:1},8,["loading"]),n(o(k),{size:"small",onClick:ze,loading:oe.value},{default:r(()=>[...e[20]||(e[20]=[y("发现 PID",-1)])]),_:1},8,["loading"]),c.value.agent_status!=="ATTACHED"?(P(),le(o(k),{key:0,size:"small",type:"primary",onClick:Fe,loading:ee.value},{default:r(()=>[...e[21]||(e[21]=[y("挂载 Agent",-1)])]),_:1},8,["loading"])):(P(),le(o(k),{key:1,size:"small",type:"warning",onClick:ue,loading:fe.value},{default:r(()=>[...e[22]||(e[22]=[y("卸载 Agent",-1)])]),_:1},8,["loading"]))]),_:1})]),default:r(()=>[n(o(Fa),{bordered:"",column:2},{default:r(()=>[n(o(O),{label:"SSH Host"},{default:r(()=>[y(A(c.value.ssh_host)+":"+A(c.value.ssh_port),1)]),_:1}),n(o(O),{label:"SSH User"},{default:r(()=>[y(A(c.value.ssh_user),1)]),_:1}),n(o(O),{label:"JAR 名称"},{default:r(()=>[y(A(c.value.java_jar_name||"-"),1)]),_:1}),n(o(O),{label:"JVM PID"},{default:r(()=>[y(A(c.value.java_pid||"-"),1)]),_:1}),n(o(O),{label:"应用端口"},{default:r(()=>[y(A(c.value.repeater_port),1)]),_:1}),n(o(O),{label:"Sandbox 端口"},{default:r(()=>[y(A(c.value.sandbox_port),1)]),_:1}),n(o(O),{label:"Sandbox 路径",span:2},{default:r(()=>[y(A(c.value.sandbox_home),1)]),_:1}),n(o(O),{label:"录制数据目录",span:2},{default:r(()=>[y(A(c.value.repeater_data_dir),1)]),_:1}),n(o(O),{label:"最后心跳"},{default:r(()=>[y(A(o(Ee)(c.value.last_heartbeat)||"-"),1)]),_:1})]),_:1})]),_:1})):Qe("",!0),n(o(ye),{title:"录制控制"},{"header-extra":r(()=>[n(o(k),{size:"small",type:"primary",onClick:_e,loading:T.value},{default:r(()=>[...e[23]||(e[23]=[y("保存",-1)])]),_:1},8,["loading"])]),default:r(()=>[n(o(Je),{"label-placement":"left","label-width":"120px"},{default:r(()=>[n(o(M),{label:"采样率"},{feedback:r(()=>[...e[24]||(e[24]=[we("span",{style:{color:"#999","font-size":"12px"}},"录制时按比例随机采样，100% 表示全量录制",-1)])]),default:r(()=>[n(o(K),{align:"center"},{default:r(()=>[n(o(Za),{value:C.value,"onUpdate:value":e[0]||(e[0]=l=>C.value=l),min:1,max:100,step:1,style:{width:"200px"}},null,8,["value"]),we("span",et,A(C.value)+"%",1)]),_:1})]),_:1}),n(o(M),{label:"脱敏规则"},{default:r(()=>[n(o(K),{vertical:"",style:{width:"100%"}},{default:r(()=>[(P(!0),Ze(ea,null,Ua(W.value,(l,x)=>(P(),le(o(K),{key:x,align:"center",wrap:""},{default:r(()=>[n(o(L),{value:l.field,"onUpdate:value":E=>l.field=E,placeholder:"字段名",style:{width:"130px"}},null,8,["value","onUpdate:value"]),n(o(aa),{value:l.action,"onUpdate:value":E=>l.action=E,options:he,style:{width:"140px"}},null,8,["value","onUpdate:value"]),l.action==="partial"?(P(),Ze(ea,{key:0},[n(o(He),{value:l.keep_start,"onUpdate:value":E=>l.keep_start=E,min:0,placeholder:"保留前N位",style:{width:"100px"}},null,8,["value","onUpdate:value"]),n(o(He),{value:l.keep_end,"onUpdate:value":E=>l.keep_end=E,min:0,placeholder:"保留后N位",style:{width:"100px"}},null,8,["value","onUpdate:value"])],64)):Qe("",!0),n(o(k),{size:"small",type:"error",circle:"",onClick:E=>$e(x)},{default:r(()=>[...e[25]||(e[25]=[y("×",-1)])]),_:1},8,["onClick"])]),_:2},1024))),128)),n(o(k),{size:"small",dashed:"",onClick:Me},{default:r(()=>[...e[26]||(e[26]=[y("+ 添加脱敏规则",-1)])]),_:1}),e[27]||(e[27]=we("span",{style:{color:"#999","font-size":"12px"}}," remove=删除字段   mask=替换为***   partial=部分遮盖   hash=哈希摘要 ",-1))]),_:1})]),_:1})]),_:1})]),_:1}),n(o(ye),{title:"回放默认配置"},{"header-extra":r(()=>[n(o(k),{size:"small",type:"primary",onClick:Ie,loading:X.value},{default:r(()=>[...e[28]||(e[28]=[y("保存",-1)])]),_:1},8,["loading"])]),default:r(()=>[n(o(Je),{"label-placement":"left","label-width":"130px"},{default:r(()=>[n(o(M),{label:"默认忽略字段"},{default:r(()=>[n(o(Pa),{value:V.value,"onUpdate:value":e[1]||(e[1]=l=>V.value=l)},null,8,["value"])]),_:1}),n(o(M),{label:"默认性能阈值(ms)"},{default:r(()=>[n(o(He),{value:$.value,"onUpdate:value":e[2]||(e[2]=l=>$.value=l),min:0,clearable:"",placeholder:"留空不限制"},null,8,["value"])]),_:1})]),_:1}),n(o(Oa),{type:"info",style:{"margin-top":"8px","font-size":"12px"}},{default:r(()=>[...e[29]||(e[29]=[y(" 在回放中心点击「加载应用默认配置」时，会自动填入以上配置。 ",-1)])]),_:1})]),_:1}),n(o(ye),{title:"Repeater 配置"},{"header-extra":r(()=>[n(o(K),null,{default:r(()=>[n(o(k),{size:"small",onClick:je},{default:r(()=>[...e[30]||(e[30]=[y("加载默认",-1)])]),_:1}),n(o(k),{size:"small",type:"primary",onClick:Pe,loading:ae.value},{default:r(()=>[...e[31]||(e[31]=[y("保存",-1)])]),_:1},8,["loading"]),n(o(k),{size:"small",onClick:Oe,loading:ne.value},{default:r(()=>[...e[32]||(e[32]=[y("推送到主机",-1)])]),_:1},8,["loading"])]),_:1})]),default:r(()=>[n(o(L),{value:D.value,"onUpdate:value":e[3]||(e[3]=l=>D.value=l),type:"textarea",rows:14,style:{"font-family":"monospace","font-size":"13px"},placeholder:"repeater-config.json 内容"},null,8,["value"])]),_:1}),n(o(Ba),{show:te.value,"onUpdate:show":e[14]||(e[14]=l=>te.value=l),preset:"dialog",title:"编辑应用",style:{width:"560px"}},{action:r(()=>[n(o(k),{onClick:e[13]||(e[13]=l=>te.value=!1)},{default:r(()=>[...e[33]||(e[33]=[y("取消",-1)])]),_:1}),n(o(k),{type:"primary",loading:se.value,onClick:ke},{default:r(()=>[...e[34]||(e[34]=[y("保存",-1)])]),_:1},8,["loading"])]),default:r(()=>[n(o(Je),{model:w.value,"label-placement":"left","label-width":"120px"},{default:r(()=>[n(o(M),{label:"SSH Host",required:""},{default:r(()=>[n(o(L),{value:w.value.ssh_host,"onUpdate:value":e[4]||(e[4]=l=>w.value.ssh_host=l),placeholder:"192.168.1.100"},null,8,["value"])]),_:1}),n(o(M),{label:"SSH User",required:""},{default:r(()=>[n(o(L),{value:w.value.ssh_user,"onUpdate:value":e[5]||(e[5]=l=>w.value.ssh_user=l),placeholder:"root"},null,8,["value"])]),_:1}),n(o(M),{label:"认证方式"},{default:r(()=>[n(o(aa),{value:w.value.ssh_auth_type,"onUpdate:value":e[6]||(e[6]=l=>w.value.ssh_auth_type=l),options:Ue},null,8,["value"])]),_:1}),w.value.ssh_auth_type==="KEY"?(P(),le(o(M),{key:0,label:"私钥路径"},{default:r(()=>[n(o(L),{value:w.value.ssh_key_path,"onUpdate:value":e[7]||(e[7]=l=>w.value.ssh_key_path=l),placeholder:"/root/.ssh/id_rsa"},null,8,["value"])]),_:1})):(P(),le(o(M),{key:1,label:"SSH 密码"},{default:r(()=>[n(o(L),{value:w.value.ssh_password,"onUpdate:value":e[8]||(e[8]=l=>w.value.ssh_password=l),type:"password"},null,8,["value"])]),_:1})),n(o(M),{label:"JAR 名称"},{default:r(()=>[n(o(L),{value:w.value.java_jar_name,"onUpdate:value":e[9]||(e[9]=l=>w.value.java_jar_name=l),placeholder:"my-service.jar"},null,8,["value"])]),_:1}),n(o(M),{label:"应用端口"},{default:r(()=>[n(o(He),{value:w.value.repeater_port,"onUpdate:value":e[10]||(e[10]=l=>w.value.repeater_port=l)},null,8,["value"])]),_:1}),n(o(M),{label:"Sandbox 路径"},{default:r(()=>[n(o(L),{value:w.value.sandbox_home,"onUpdate:value":e[11]||(e[11]=l=>w.value.sandbox_home=l),placeholder:"/home/test/.sandbox"},null,8,["value"])]),_:1}),n(o(M),{label:"录制数据目录"},{default:r(()=>[n(o(L),{value:w.value.repeater_data_dir,"onUpdate:value":e[12]||(e[12]=l=>w.value.repeater_data_dir=l),placeholder:"/home/test/.sandbox-module/repeater-data/record"},null,8,["value"])]),_:1})]),_:1},8,["model"])]),_:1},8,["show"]),n(o(ye),{title:"录制会话"},{"header-extra":r(()=>[n(o(k),{size:"small",type:"primary",onClick:ce},{default:r(()=>[...e[35]||(e[35]=[y("+ 开始录制",-1)])]),_:1})]),default:r(()=>[n(o(Ka),{columns:pe,data:I.value,loading:Y.value},null,8,["data","loading"]),n(o(K),{justify:"end",align:"center",style:{"margin-top":"12px"}},{default:r(()=>[we("span",at,"共 "+A(Z.value)+" 条",1),n(o(La),{page:S.page,"onUpdate:page":[e[15]||(e[15]=l=>S.page=l),ie],"page-size":S.pageSize,"onUpdate:pageSize":[e[16]||(e[16]=l=>S.pageSize=l),e[17]||(e[17]=l=>{S.pageSize=l,S.page=1,ie()})],"page-sizes":[10,20,50],"item-count":S.itemCount,"show-size-picker":"","show-quick-jumper":!0,disabled:Y.value},null,8,["page","page-size","item-count","disabled"])]),_:1})]),_:1})]),_:1}))}});export{mt as default};
