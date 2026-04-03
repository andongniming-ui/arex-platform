import{d as pe,j as m,ba as Nt,r as P,bb as Mt,bc as Fe,bd as Vt,be as Se,bf as Ht,k as Ft,a4 as Ot,aj as Gt,ad as at,aM as Dt,F as rt,a7 as Ut,bg as Xt,aN as Yt,i as de,bh as qt,m as i,n as v,l as E,p as V,a6 as Kt,bi as Re,aO as Oe,bj as $e,C as Jt,D as nt,G as Qt,H as Le,o as lt,bk as Zt,ak as ea,J as ta,b4 as Ge,b9 as aa,a9 as ra,ab as na,bl as la,bm as oa,P as ke,ar as X,aP as he,ai as ia,Q as Y,L as xe,h as Be,w as y,u,a as b,B as J,g as Q,N as De,W as sa,c as da,Y as ua,X as ca,b as ba,S as Ue,e as fa,f as ye,U as pa}from"./index-B6ywSR35.js";import{c as Z,N as va}from"./client-CJ4wff5B.js";import{a as ga}from"./applications-Btmv_8_S.js";import{t as ma}from"./testCases-D6mN_U1f.js";import{f as Xe}from"./time-DBiNR5Lf.js";import{A as ha}from"./Add-BNseDRIA.js";import{u as xa}from"./use-message-CpgDv7T6.js";import{N as Ce,a as se}from"./Space-B3nMO6fs.js";import{N as Ye,a as We}from"./DataTable-C-vr6xbd.js";import{N as qe,a as F}from"./FormItem-BC7p258p.js";import{N as fe}from"./InputNumber-6LzjK-Fb.js";import{N as ya}from"./Divider-B05FVJWz.js";import{N as Ca}from"./Popconfirm-Bv2cP_gw.js";const Sa=Fe(".v-x-scroll",{overflow:"auto",scrollbarWidth:"none"},[Fe("&::-webkit-scrollbar",{width:0,height:0})]),_a=pe({name:"XScroll",props:{disabled:Boolean,onScroll:Function},setup(){const e=P(null);function o(p){!(p.currentTarget.offsetWidth<p.currentTarget.scrollWidth)||p.deltaY===0||(p.currentTarget.scrollLeft+=p.deltaY+p.deltaX,p.preventDefault())}const s=Mt();return Sa.mount({id:"vueuc/x-scroll",head:!0,anchorMetaName:Nt,ssr:s}),Object.assign({selfRef:e,handleWheel:o},{scrollTo(...p){var c;(c=e.value)===null||c===void 0||c.scrollTo(...p)}})},render(){return m("div",{ref:"selfRef",onScroll:this.onScroll,onWheel:this.disabled?void 0:this.handleWheel,class:"v-x-scroll"},this.$slots)}});var wa=/\s/;function Ta(e){for(var o=e.length;o--&&wa.test(e.charAt(o)););return o}var za=/^\s+/;function Pa(e){return e&&e.slice(0,Ta(e)+1).replace(za,"")}var Ke=NaN,Ra=/^[-+]0x[0-9a-f]+$/i,$a=/^0b[01]+$/i,La=/^0o[0-7]+$/i,ka=parseInt;function Je(e){if(typeof e=="number")return e;if(Vt(e))return Ke;if(Se(e)){var o=typeof e.valueOf=="function"?e.valueOf():e;e=Se(o)?o+"":o}if(typeof e!="string")return e===0?e:+e;e=Pa(e);var s=$a.test(e);return s||La.test(e)?ka(e.slice(2),s?2:8):Ra.test(e)?Ke:+e}var Ae=function(){return Ht.Date.now()},Ba="Expected a function",Wa=Math.max,Aa=Math.min;function Ea(e,o,s){var f,p,c,w,S,T,R=0,z=!1,L=!1,A=!0;if(typeof e!="function")throw new TypeError(Ba);o=Je(o)||0,Se(s)&&(z=!!s.leading,L="maxWait"in s,c=L?Wa(Je(s.maxWait)||0,o):c,A="trailing"in s?!!s.trailing:A);function $(g){var N=f,q=p;return f=p=void 0,R=g,w=e.apply(q,N),w}function k(g){return R=g,S=setTimeout(C,o),z?$(g):w}function B(g){var N=g-T,q=g-R,K=o-N;return L?Aa(K,c-q):K}function h(g){var N=g-T,q=g-R;return T===void 0||N>=o||N<0||L&&q>=c}function C(){var g=Ae();if(h(g))return I(g);S=setTimeout(C,B(g))}function I(g){return S=void 0,A&&f?$(g):(f=p=void 0,w)}function D(){S!==void 0&&clearTimeout(S),R=0,f=T=p=S=void 0}function H(){return S===void 0?w:I(Ae())}function _(){var g=Ae(),N=h(g);if(f=arguments,p=this,T=g,N){if(S===void 0)return k(T);if(L)return clearTimeout(S),S=setTimeout(C,o),$(T)}return S===void 0&&(S=setTimeout(C,o)),w}return _.cancel=D,_.flush=H,_}var Ia="Expected a function";function ja(e,o,s){var f=!0,p=!0;if(typeof e!="function")throw new TypeError(Ia);return Se(s)&&(f="leading"in s?!!s.leading:f,p="trailing"in s?!!s.trailing:p),Ea(e,o,{leading:f,maxWait:o,trailing:p})}const Na={tabFontSizeSmall:"14px",tabFontSizeMedium:"14px",tabFontSizeLarge:"16px",tabGapSmallLine:"36px",tabGapMediumLine:"36px",tabGapLargeLine:"36px",tabGapSmallLineVertical:"8px",tabGapMediumLineVertical:"8px",tabGapLargeLineVertical:"8px",tabPaddingSmallLine:"6px 0",tabPaddingMediumLine:"10px 0",tabPaddingLargeLine:"14px 0",tabPaddingVerticalSmallLine:"6px 12px",tabPaddingVerticalMediumLine:"8px 16px",tabPaddingVerticalLargeLine:"10px 20px",tabGapSmallBar:"36px",tabGapMediumBar:"36px",tabGapLargeBar:"36px",tabGapSmallBarVertical:"8px",tabGapMediumBarVertical:"8px",tabGapLargeBarVertical:"8px",tabPaddingSmallBar:"4px 0",tabPaddingMediumBar:"6px 0",tabPaddingLargeBar:"10px 0",tabPaddingVerticalSmallBar:"6px 12px",tabPaddingVerticalMediumBar:"8px 16px",tabPaddingVerticalLargeBar:"10px 20px",tabGapSmallCard:"4px",tabGapMediumCard:"4px",tabGapLargeCard:"4px",tabGapSmallCardVertical:"4px",tabGapMediumCardVertical:"4px",tabGapLargeCardVertical:"4px",tabPaddingSmallCard:"8px 16px",tabPaddingMediumCard:"10px 20px",tabPaddingLargeCard:"12px 24px",tabPaddingSmallSegment:"4px 0",tabPaddingMediumSegment:"6px 0",tabPaddingLargeSegment:"8px 0",tabPaddingVerticalLargeSegment:"0 8px",tabPaddingVerticalSmallCard:"8px 12px",tabPaddingVerticalMediumCard:"10px 16px",tabPaddingVerticalLargeCard:"12px 20px",tabPaddingVerticalSmallSegment:"0 4px",tabPaddingVerticalMediumSegment:"0 6px",tabGapSmallSegment:"0",tabGapMediumSegment:"0",tabGapLargeSegment:"0",tabGapSmallSegmentVertical:"0",tabGapMediumSegmentVertical:"0",tabGapLargeSegmentVertical:"0",panePaddingSmall:"8px 0 0 0",panePaddingMedium:"12px 0 0 0",panePaddingLarge:"16px 0 0 0",closeSize:"18px",closeIconSize:"14px"};function Ma(e){const{textColor2:o,primaryColor:s,textColorDisabled:f,closeIconColor:p,closeIconColorHover:c,closeIconColorPressed:w,closeColorHover:S,closeColorPressed:T,tabColor:R,baseColor:z,dividerColor:L,fontWeight:A,textColor1:$,borderRadius:k,fontSize:B,fontWeightStrong:h}=e;return Object.assign(Object.assign({},Na),{colorSegment:R,tabFontSizeCard:B,tabTextColorLine:$,tabTextColorActiveLine:s,tabTextColorHoverLine:s,tabTextColorDisabledLine:f,tabTextColorSegment:$,tabTextColorActiveSegment:o,tabTextColorHoverSegment:o,tabTextColorDisabledSegment:f,tabTextColorBar:$,tabTextColorActiveBar:s,tabTextColorHoverBar:s,tabTextColorDisabledBar:f,tabTextColorCard:$,tabTextColorHoverCard:$,tabTextColorActiveCard:s,tabTextColorDisabledCard:f,barColor:s,closeIconColor:p,closeIconColorHover:c,closeIconColorPressed:w,closeColorHover:S,closeColorPressed:T,closeBorderRadius:k,tabColor:R,tabColorSegment:z,tabBorderColor:L,tabFontWeightActive:A,tabFontWeight:A,tabBorderRadius:k,paneTextColor:o,fontWeightStrong:h})}const Va={common:Ft,self:Ma},Ne=Ot("n-tabs"),ot={tab:[String,Number,Object,Function],name:{type:[String,Number],required:!0},disabled:Boolean,displayDirective:{type:String,default:"if"},closable:{type:Boolean,default:void 0},tabProps:Object,label:[String,Number,Object,Function]},Qe=pe({__TAB_PANE__:!0,name:"TabPane",alias:["TabPanel"],props:ot,slots:Object,setup(e){const o=at(Ne,null);return o||Gt("tab-pane","`n-tab-pane` must be placed inside `n-tabs`."),{style:o.paneStyleRef,class:o.paneClassRef,mergedClsPrefix:o.mergedClsPrefixRef}},render(){return m("div",{class:[`${this.mergedClsPrefix}-tab-pane`,this.class],style:this.style},this.$slots)}}),Ha=Object.assign({internalLeftPadded:Boolean,internalAddable:Boolean,internalCreatedByPane:Boolean},qt(ot,["displayDirective"])),je=pe({__TAB__:!0,inheritAttrs:!1,name:"Tab",props:Ha,setup(e){const{mergedClsPrefixRef:o,valueRef:s,typeRef:f,closableRef:p,tabStyleRef:c,addTabStyleRef:w,tabClassRef:S,addTabClassRef:T,tabChangeIdRef:R,onBeforeLeaveRef:z,triggerRef:L,handleAdd:A,activateTab:$,handleClose:k}=at(Ne);return{trigger:L,mergedClosable:de(()=>{if(e.internalAddable)return!1;const{closable:B}=e;return B===void 0?p.value:B}),style:c,addStyle:w,tabClass:S,addTabClass:T,clsPrefix:o,value:s,type:f,handleClose(B){B.stopPropagation(),!e.disabled&&k(e.name)},activateTab(){if(e.disabled)return;if(e.internalAddable){A();return}const{name:B}=e,h=++R.id;if(B!==s.value){const{value:C}=z;C?Promise.resolve(C(e.name,s.value)).then(I=>{I&&R.id===h&&$(B)}):$(B)}}}},render(){const{internalAddable:e,clsPrefix:o,name:s,disabled:f,label:p,tab:c,value:w,mergedClosable:S,trigger:T,$slots:{default:R}}=this,z=p??c;return m("div",{class:`${o}-tabs-tab-wrapper`},this.internalLeftPadded?m("div",{class:`${o}-tabs-tab-pad`}):null,m("div",Object.assign({key:s,"data-name":s,"data-disabled":f?!0:void 0},Dt({class:[`${o}-tabs-tab`,w===s&&`${o}-tabs-tab--active`,f&&`${o}-tabs-tab--disabled`,S&&`${o}-tabs-tab--closable`,e&&`${o}-tabs-tab--addable`,e?this.addTabClass:this.tabClass],onClick:T==="click"?this.activateTab:void 0,onMouseenter:T==="hover"?this.activateTab:void 0,style:e?this.addStyle:this.style},this.internalCreatedByPane?this.tabProps||{}:this.$attrs)),m("span",{class:`${o}-tabs-tab__label`},e?m(rt,null,m("div",{class:`${o}-tabs-tab__height-placeholder`}," "),m(Ut,{clsPrefix:o},{default:()=>m(ha,null)})):R?R():typeof z=="object"?z:Xt(z??s)),S&&this.type==="card"?m(Yt,{clsPrefix:o,class:`${o}-tabs-tab__close`,onClick:this.handleClose,disabled:f}):null))}}),Fa=i("tabs",`
 box-sizing: border-box;
 width: 100%;
 display: flex;
 flex-direction: column;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
`,[v("segment-type",[i("tabs-rail",[E("&.transition-disabled",[i("tabs-capsule",`
 transition: none;
 `)])])]),v("top",[i("tab-pane",`
 padding: var(--n-pane-padding-top) var(--n-pane-padding-right) var(--n-pane-padding-bottom) var(--n-pane-padding-left);
 `)]),v("left",[i("tab-pane",`
 padding: var(--n-pane-padding-right) var(--n-pane-padding-bottom) var(--n-pane-padding-left) var(--n-pane-padding-top);
 `)]),v("left, right",`
 flex-direction: row;
 `,[i("tabs-bar",`
 width: 2px;
 right: 0;
 transition:
 top .2s var(--n-bezier),
 max-height .2s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `),i("tabs-tab",`
 padding: var(--n-tab-padding-vertical); 
 `)]),v("right",`
 flex-direction: row-reverse;
 `,[i("tab-pane",`
 padding: var(--n-pane-padding-left) var(--n-pane-padding-top) var(--n-pane-padding-right) var(--n-pane-padding-bottom);
 `),i("tabs-bar",`
 left: 0;
 `)]),v("bottom",`
 flex-direction: column-reverse;
 justify-content: flex-end;
 `,[i("tab-pane",`
 padding: var(--n-pane-padding-bottom) var(--n-pane-padding-right) var(--n-pane-padding-top) var(--n-pane-padding-left);
 `),i("tabs-bar",`
 top: 0;
 `)]),i("tabs-rail",`
 position: relative;
 padding: 3px;
 border-radius: var(--n-tab-border-radius);
 width: 100%;
 background-color: var(--n-color-segment);
 transition: background-color .3s var(--n-bezier);
 display: flex;
 align-items: center;
 `,[i("tabs-capsule",`
 border-radius: var(--n-tab-border-radius);
 position: absolute;
 pointer-events: none;
 background-color: var(--n-tab-color-segment);
 box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .08);
 transition: transform 0.3s var(--n-bezier);
 `),i("tabs-tab-wrapper",`
 flex-basis: 0;
 flex-grow: 1;
 display: flex;
 align-items: center;
 justify-content: center;
 `,[i("tabs-tab",`
 overflow: hidden;
 border-radius: var(--n-tab-border-radius);
 width: 100%;
 display: flex;
 align-items: center;
 justify-content: center;
 `,[v("active",`
 font-weight: var(--n-font-weight-strong);
 color: var(--n-tab-text-color-active);
 `),E("&:hover",`
 color: var(--n-tab-text-color-hover);
 `)])])]),v("flex",[i("tabs-nav",`
 width: 100%;
 position: relative;
 `,[i("tabs-wrapper",`
 width: 100%;
 `,[i("tabs-tab",`
 margin-right: 0;
 `)])])]),i("tabs-nav",`
 box-sizing: border-box;
 line-height: 1.5;
 display: flex;
 transition: border-color .3s var(--n-bezier);
 `,[V("prefix, suffix",`
 display: flex;
 align-items: center;
 `),V("prefix","padding-right: 16px;"),V("suffix","padding-left: 16px;")]),v("top, bottom",[E(">",[i("tabs-nav",[i("tabs-nav-scroll-wrapper",[E("&::before",`
 top: 0;
 bottom: 0;
 left: 0;
 width: 20px;
 `),E("&::after",`
 top: 0;
 bottom: 0;
 right: 0;
 width: 20px;
 `),v("shadow-start",[E("&::before",`
 box-shadow: inset 10px 0 8px -8px rgba(0, 0, 0, .12);
 `)]),v("shadow-end",[E("&::after",`
 box-shadow: inset -10px 0 8px -8px rgba(0, 0, 0, .12);
 `)])])])])]),v("left, right",[i("tabs-nav-scroll-content",`
 flex-direction: column;
 `),E(">",[i("tabs-nav",[i("tabs-nav-scroll-wrapper",[E("&::before",`
 top: 0;
 left: 0;
 right: 0;
 height: 20px;
 `),E("&::after",`
 bottom: 0;
 left: 0;
 right: 0;
 height: 20px;
 `),v("shadow-start",[E("&::before",`
 box-shadow: inset 0 10px 8px -8px rgba(0, 0, 0, .12);
 `)]),v("shadow-end",[E("&::after",`
 box-shadow: inset 0 -10px 8px -8px rgba(0, 0, 0, .12);
 `)])])])])]),i("tabs-nav-scroll-wrapper",`
 flex: 1;
 position: relative;
 overflow: hidden;
 `,[i("tabs-nav-y-scroll",`
 height: 100%;
 width: 100%;
 overflow-y: auto; 
 scrollbar-width: none;
 `,[E("&::-webkit-scrollbar, &::-webkit-scrollbar-track-piece, &::-webkit-scrollbar-thumb",`
 width: 0;
 height: 0;
 display: none;
 `)]),E("&::before, &::after",`
 transition: box-shadow .3s var(--n-bezier);
 pointer-events: none;
 content: "";
 position: absolute;
 z-index: 1;
 `)]),i("tabs-nav-scroll-content",`
 display: flex;
 position: relative;
 min-width: 100%;
 min-height: 100%;
 width: fit-content;
 box-sizing: border-box;
 `),i("tabs-wrapper",`
 display: inline-flex;
 flex-wrap: nowrap;
 position: relative;
 `),i("tabs-tab-wrapper",`
 display: flex;
 flex-wrap: nowrap;
 flex-shrink: 0;
 flex-grow: 0;
 `),i("tabs-tab",`
 cursor: pointer;
 white-space: nowrap;
 flex-wrap: nowrap;
 display: inline-flex;
 align-items: center;
 color: var(--n-tab-text-color);
 font-size: var(--n-tab-font-size);
 background-clip: padding-box;
 padding: var(--n-tab-padding);
 transition:
 box-shadow .3s var(--n-bezier),
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[v("disabled",{cursor:"not-allowed"}),V("close",`
 margin-left: 6px;
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `),V("label",`
 display: flex;
 align-items: center;
 z-index: 1;
 `)]),i("tabs-bar",`
 position: absolute;
 bottom: 0;
 height: 2px;
 border-radius: 1px;
 background-color: var(--n-bar-color);
 transition:
 left .2s var(--n-bezier),
 max-width .2s var(--n-bezier),
 opacity .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 `,[E("&.transition-disabled",`
 transition: none;
 `),v("disabled",`
 background-color: var(--n-tab-text-color-disabled)
 `)]),i("tabs-pane-wrapper",`
 position: relative;
 overflow: hidden;
 transition: max-height .2s var(--n-bezier);
 `),i("tab-pane",`
 color: var(--n-pane-text-color);
 width: 100%;
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 opacity .2s var(--n-bezier);
 left: 0;
 right: 0;
 top: 0;
 `,[E("&.next-transition-leave-active, &.prev-transition-leave-active, &.next-transition-enter-active, &.prev-transition-enter-active",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 transform .2s var(--n-bezier),
 opacity .2s var(--n-bezier);
 `),E("&.next-transition-leave-active, &.prev-transition-leave-active",`
 position: absolute;
 `),E("&.next-transition-enter-from, &.prev-transition-leave-to",`
 transform: translateX(32px);
 opacity: 0;
 `),E("&.next-transition-leave-to, &.prev-transition-enter-from",`
 transform: translateX(-32px);
 opacity: 0;
 `),E("&.next-transition-leave-from, &.next-transition-enter-to, &.prev-transition-leave-from, &.prev-transition-enter-to",`
 transform: translateX(0);
 opacity: 1;
 `)]),i("tabs-tab-pad",`
 box-sizing: border-box;
 width: var(--n-tab-gap);
 flex-grow: 0;
 flex-shrink: 0;
 `),v("line-type, bar-type",[i("tabs-tab",`
 font-weight: var(--n-tab-font-weight);
 box-sizing: border-box;
 vertical-align: bottom;
 `,[E("&:hover",{color:"var(--n-tab-text-color-hover)"}),v("active",`
 color: var(--n-tab-text-color-active);
 font-weight: var(--n-tab-font-weight-active);
 `),v("disabled",{color:"var(--n-tab-text-color-disabled)"})])]),i("tabs-nav",[v("line-type",[v("top",[V("prefix, suffix",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),i("tabs-nav-scroll-content",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),i("tabs-bar",`
 bottom: -1px;
 `)]),v("left",[V("prefix, suffix",`
 border-right: 1px solid var(--n-tab-border-color);
 `),i("tabs-nav-scroll-content",`
 border-right: 1px solid var(--n-tab-border-color);
 `),i("tabs-bar",`
 right: -1px;
 `)]),v("right",[V("prefix, suffix",`
 border-left: 1px solid var(--n-tab-border-color);
 `),i("tabs-nav-scroll-content",`
 border-left: 1px solid var(--n-tab-border-color);
 `),i("tabs-bar",`
 left: -1px;
 `)]),v("bottom",[V("prefix, suffix",`
 border-top: 1px solid var(--n-tab-border-color);
 `),i("tabs-nav-scroll-content",`
 border-top: 1px solid var(--n-tab-border-color);
 `),i("tabs-bar",`
 top: -1px;
 `)]),V("prefix, suffix",`
 transition: border-color .3s var(--n-bezier);
 `),i("tabs-nav-scroll-content",`
 transition: border-color .3s var(--n-bezier);
 `),i("tabs-bar",`
 border-radius: 0;
 `)]),v("card-type",[V("prefix, suffix",`
 transition: border-color .3s var(--n-bezier);
 `),i("tabs-pad",`
 flex-grow: 1;
 transition: border-color .3s var(--n-bezier);
 `),i("tabs-tab-pad",`
 transition: border-color .3s var(--n-bezier);
 `),i("tabs-tab",`
 font-weight: var(--n-tab-font-weight);
 border: 1px solid var(--n-tab-border-color);
 background-color: var(--n-tab-color);
 box-sizing: border-box;
 position: relative;
 vertical-align: bottom;
 display: flex;
 justify-content: space-between;
 font-size: var(--n-tab-font-size);
 color: var(--n-tab-text-color);
 `,[v("addable",`
 padding-left: 8px;
 padding-right: 8px;
 font-size: 16px;
 justify-content: center;
 `,[V("height-placeholder",`
 width: 0;
 font-size: var(--n-tab-font-size);
 `),Kt("disabled",[E("&:hover",`
 color: var(--n-tab-text-color-hover);
 `)])]),v("closable","padding-right: 8px;"),v("active",`
 background-color: #0000;
 font-weight: var(--n-tab-font-weight-active);
 color: var(--n-tab-text-color-active);
 `),v("disabled","color: var(--n-tab-text-color-disabled);")])]),v("left, right",`
 flex-direction: column; 
 `,[V("prefix, suffix",`
 padding: var(--n-tab-padding-vertical);
 `),i("tabs-wrapper",`
 flex-direction: column;
 `),i("tabs-tab-wrapper",`
 flex-direction: column;
 `,[i("tabs-tab-pad",`
 height: var(--n-tab-gap-vertical);
 width: 100%;
 `)])]),v("top",[v("card-type",[i("tabs-scroll-padding","border-bottom: 1px solid var(--n-tab-border-color);"),V("prefix, suffix",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),i("tabs-tab",`
 border-top-left-radius: var(--n-tab-border-radius);
 border-top-right-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-bottom: 1px solid #0000;
 `)]),i("tabs-tab-pad",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `),i("tabs-pad",`
 border-bottom: 1px solid var(--n-tab-border-color);
 `)])]),v("left",[v("card-type",[i("tabs-scroll-padding","border-right: 1px solid var(--n-tab-border-color);"),V("prefix, suffix",`
 border-right: 1px solid var(--n-tab-border-color);
 `),i("tabs-tab",`
 border-top-left-radius: var(--n-tab-border-radius);
 border-bottom-left-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-right: 1px solid #0000;
 `)]),i("tabs-tab-pad",`
 border-right: 1px solid var(--n-tab-border-color);
 `),i("tabs-pad",`
 border-right: 1px solid var(--n-tab-border-color);
 `)])]),v("right",[v("card-type",[i("tabs-scroll-padding","border-left: 1px solid var(--n-tab-border-color);"),V("prefix, suffix",`
 border-left: 1px solid var(--n-tab-border-color);
 `),i("tabs-tab",`
 border-top-right-radius: var(--n-tab-border-radius);
 border-bottom-right-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-left: 1px solid #0000;
 `)]),i("tabs-tab-pad",`
 border-left: 1px solid var(--n-tab-border-color);
 `),i("tabs-pad",`
 border-left: 1px solid var(--n-tab-border-color);
 `)])]),v("bottom",[v("card-type",[i("tabs-scroll-padding","border-top: 1px solid var(--n-tab-border-color);"),V("prefix, suffix",`
 border-top: 1px solid var(--n-tab-border-color);
 `),i("tabs-tab",`
 border-bottom-left-radius: var(--n-tab-border-radius);
 border-bottom-right-radius: var(--n-tab-border-radius);
 `,[v("active",`
 border-top: 1px solid #0000;
 `)]),i("tabs-tab-pad",`
 border-top: 1px solid var(--n-tab-border-color);
 `),i("tabs-pad",`
 border-top: 1px solid var(--n-tab-border-color);
 `)])])])]),Ee=ja,Oa=Object.assign(Object.assign({},nt.props),{value:[String,Number],defaultValue:[String,Number],trigger:{type:String,default:"click"},type:{type:String,default:"bar"},closable:Boolean,justifyContent:String,size:String,placement:{type:String,default:"top"},tabStyle:[String,Object],tabClass:String,addTabStyle:[String,Object],addTabClass:String,barWidth:Number,paneClass:String,paneStyle:[String,Object],paneWrapperClass:String,paneWrapperStyle:[String,Object],addable:[Boolean,Object],tabsPadding:{type:Number,default:0},animated:Boolean,onBeforeLeave:Function,onAdd:Function,"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],onClose:[Function,Array],labelSize:String,activeName:[String,Number],onActiveNameChange:[Function,Array]}),Ga=pe({name:"Tabs",props:Oa,slots:Object,setup(e,{slots:o}){var s,f,p,c;const{mergedClsPrefixRef:w,inlineThemeDisabled:S,mergedComponentPropsRef:T}=Jt(e),R=nt("Tabs","-tabs",Fa,Va,e,w),z=P(null),L=P(null),A=P(null),$=P(null),k=P(null),B=P(null),h=P(!0),C=P(!0),I=Ge(e,["labelSize","size"]),D=de(()=>{var t,a;if(I.value)return I.value;const d=(a=(t=T==null?void 0:T.value)===null||t===void 0?void 0:t.Tabs)===null||a===void 0?void 0:a.size;return d||"medium"}),H=Ge(e,["activeName","value"]),_=P((f=(s=H.value)!==null&&s!==void 0?s:e.defaultValue)!==null&&f!==void 0?f:o.default?(c=(p=Re(o.default())[0])===null||p===void 0?void 0:p.props)===null||c===void 0?void 0:c.name:null),g=Qt(H,_),N={id:0},q=de(()=>{if(!(!e.justifyContent||e.type==="card"))return{display:"flex",justifyContent:e.justifyContent}});Le(g,()=>{N.id=0,te(),ge()});function K(){var t;const{value:a}=g;return a===null?null:(t=z.value)===null||t===void 0?void 0:t.querySelector(`[data-name="${a}"]`)}function ue(t){if(e.type==="card")return;const{value:a}=L;if(!a)return;const d=a.style.opacity==="0";if(t){const x=`${w.value}-tabs-bar--disabled`,{barWidth:j,placement:O}=e;if(t.dataset.disabled==="true"?a.classList.add(x):a.classList.remove(x),["top","bottom"].includes(O)){if(ve(["top","maxHeight","height"]),typeof j=="number"&&t.offsetWidth>=j){const G=Math.floor((t.offsetWidth-j)/2)+t.offsetLeft;a.style.left=`${G}px`,a.style.maxWidth=`${j}px`}else a.style.left=`${t.offsetLeft}px`,a.style.maxWidth=`${t.offsetWidth}px`;a.style.width="8192px",d&&(a.style.transition="none"),a.offsetWidth,d&&(a.style.transition="",a.style.opacity="1")}else{if(ve(["left","maxWidth","width"]),typeof j=="number"&&t.offsetHeight>=j){const G=Math.floor((t.offsetHeight-j)/2)+t.offsetTop;a.style.top=`${G}px`,a.style.maxHeight=`${j}px`}else a.style.top=`${t.offsetTop}px`,a.style.maxHeight=`${t.offsetHeight}px`;a.style.height="8192px",d&&(a.style.transition="none"),a.offsetHeight,d&&(a.style.transition="",a.style.opacity="1")}}}function _e(){if(e.type==="card")return;const{value:t}=L;t&&(t.style.opacity="0")}function ve(t){const{value:a}=L;if(a)for(const d of t)a.style[d]=""}function te(){if(e.type==="card")return;const t=K();t?ue(t):_e()}function ge(){var t;const a=(t=k.value)===null||t===void 0?void 0:t.$el;if(!a)return;const d=K();if(!d)return;const{scrollLeft:x,offsetWidth:j}=a,{offsetLeft:O,offsetWidth:G}=d;x>O?a.scrollTo({top:0,left:O,behavior:"smooth"}):O+G>x+j&&a.scrollTo({top:0,left:O+G-j,behavior:"smooth"})}const ae=P(null);let ce=0,U=null;function we(t){const a=ae.value;if(a){ce=t.getBoundingClientRect().height;const d=`${ce}px`,x=()=>{a.style.height=d,a.style.maxHeight=d};U?(x(),U(),U=null):U=x}}function n(t){const a=ae.value;if(a){const d=t.getBoundingClientRect().height,x=()=>{document.body.offsetHeight,a.style.maxHeight=`${d}px`,a.style.height=`${Math.max(ce,d)}px`};U?(U(),U=null,x()):U=x}}function r(){const t=ae.value;if(t){t.style.maxHeight="",t.style.height="";const{paneWrapperStyle:a}=e;if(typeof a=="string")t.style.cssText=a;else if(a){const{maxHeight:d,height:x}=a;d!==void 0&&(t.style.maxHeight=d),x!==void 0&&(t.style.height=x)}}}const l={value:[]},W=P("next");function M(t){const a=g.value;let d="next";for(const x of l.value){if(x===a)break;if(x===t){d="prev";break}}W.value=d,re(t)}function re(t){const{onActiveNameChange:a,onUpdateValue:d,"onUpdate:value":x}=e;a&&xe(a,t),d&&xe(d,t),x&&xe(x,t),_.value=t}function Te(t){const{onClose:a}=e;a&&xe(a,t)}function Me(){const{value:t}=L;if(!t)return;const a="transition-disabled";t.classList.add(a),te(),t.classList.remove(a)}const ne=P(null);function ze({transitionDisabled:t}){const a=z.value;if(!a)return;t&&a.classList.add("transition-disabled");const d=K();d&&ne.value&&(ne.value.style.width=`${d.offsetWidth}px`,ne.value.style.height=`${d.offsetHeight}px`,ne.value.style.transform=`translateX(${d.offsetLeft-aa(getComputedStyle(a).paddingLeft)}px)`,t&&ne.value.offsetWidth),t&&a.classList.remove("transition-disabled")}Le([g],()=>{e.type==="segment"&&ke(()=>{ze({transitionDisabled:!1})})}),lt(()=>{e.type==="segment"&&ze({transitionDisabled:!0})});let Ve=0;function it(t){var a;if(t.contentRect.width===0&&t.contentRect.height===0||Ve===t.contentRect.width)return;Ve=t.contentRect.width;const{type:d}=e;if((d==="line"||d==="bar")&&Me(),d!=="segment"){const{placement:x}=e;Pe((x==="top"||x==="bottom"?(a=k.value)===null||a===void 0?void 0:a.$el:B.value)||null)}}const st=Ee(it,64);Le([()=>e.justifyContent,()=>e.size],()=>{ke(()=>{const{type:t}=e;(t==="line"||t==="bar")&&Me()})});const le=P(!1);function dt(t){var a;const{target:d,contentRect:{width:x,height:j}}=t,O=d.parentElement.parentElement.offsetWidth,G=d.parentElement.parentElement.offsetHeight,{placement:ie}=e;if(!le.value)ie==="top"||ie==="bottom"?O<x&&(le.value=!0):G<j&&(le.value=!0);else{const{value:be}=$;if(!be)return;ie==="top"||ie==="bottom"?O-x>be.$el.offsetWidth&&(le.value=!1):G-j>be.$el.offsetHeight&&(le.value=!1)}Pe(((a=k.value)===null||a===void 0?void 0:a.$el)||null)}const ut=Ee(dt,64);function ct(){const{onAdd:t}=e;t&&t(),ke(()=>{const a=K(),{value:d}=k;!a||!d||d.scrollTo({left:a.offsetLeft,top:0,behavior:"smooth"})})}function Pe(t){if(!t)return;const{placement:a}=e;if(a==="top"||a==="bottom"){const{scrollLeft:d,scrollWidth:x,offsetWidth:j}=t;h.value=d<=0,C.value=d+j>=x}else{const{scrollTop:d,scrollHeight:x,offsetHeight:j}=t;h.value=d<=0,C.value=d+j>=x}}const bt=Ee(t=>{Pe(t.target)},64);ia(Ne,{triggerRef:Y(e,"trigger"),tabStyleRef:Y(e,"tabStyle"),tabClassRef:Y(e,"tabClass"),addTabStyleRef:Y(e,"addTabStyle"),addTabClassRef:Y(e,"addTabClass"),paneClassRef:Y(e,"paneClass"),paneStyleRef:Y(e,"paneStyle"),mergedClsPrefixRef:w,typeRef:Y(e,"type"),closableRef:Y(e,"closable"),valueRef:g,tabChangeIdRef:N,onBeforeLeaveRef:Y(e,"onBeforeLeave"),activateTab:M,handleClose:Te,handleAdd:ct}),Zt(()=>{te(),ge()}),ea(()=>{const{value:t}=A;if(!t)return;const{value:a}=w,d=`${a}-tabs-nav-scroll-wrapper--shadow-start`,x=`${a}-tabs-nav-scroll-wrapper--shadow-end`;h.value?t.classList.remove(d):t.classList.add(d),C.value?t.classList.remove(x):t.classList.add(x)});const ft={syncBarPosition:()=>{te()}},pt=()=>{ze({transitionDisabled:!0})},He=de(()=>{const{value:t}=D,{type:a}=e,d={card:"Card",bar:"Bar",line:"Line",segment:"Segment"}[a],x=`${t}${d}`,{self:{barColor:j,closeIconColor:O,closeIconColorHover:G,closeIconColorPressed:ie,tabColor:be,tabBorderColor:vt,paneTextColor:gt,tabFontWeight:mt,tabBorderRadius:ht,tabFontWeightActive:xt,colorSegment:yt,fontWeightStrong:Ct,tabColorSegment:St,closeSize:_t,closeIconSize:wt,closeColorHover:Tt,closeColorPressed:zt,closeBorderRadius:Pt,[X("panePadding",t)]:me,[X("tabPadding",x)]:Rt,[X("tabPaddingVertical",x)]:$t,[X("tabGap",x)]:Lt,[X("tabGap",`${x}Vertical`)]:kt,[X("tabTextColor",a)]:Bt,[X("tabTextColorActive",a)]:Wt,[X("tabTextColorHover",a)]:At,[X("tabTextColorDisabled",a)]:Et,[X("tabFontSize",t)]:It},common:{cubicBezierEaseInOut:jt}}=R.value;return{"--n-bezier":jt,"--n-color-segment":yt,"--n-bar-color":j,"--n-tab-font-size":It,"--n-tab-text-color":Bt,"--n-tab-text-color-active":Wt,"--n-tab-text-color-disabled":Et,"--n-tab-text-color-hover":At,"--n-pane-text-color":gt,"--n-tab-border-color":vt,"--n-tab-border-radius":ht,"--n-close-size":_t,"--n-close-icon-size":wt,"--n-close-color-hover":Tt,"--n-close-color-pressed":zt,"--n-close-border-radius":Pt,"--n-close-icon-color":O,"--n-close-icon-color-hover":G,"--n-close-icon-color-pressed":ie,"--n-tab-color":be,"--n-tab-font-weight":mt,"--n-tab-font-weight-active":xt,"--n-tab-padding":Rt,"--n-tab-padding-vertical":$t,"--n-tab-gap":Lt,"--n-tab-gap-vertical":kt,"--n-pane-padding-left":he(me,"left"),"--n-pane-padding-right":he(me,"right"),"--n-pane-padding-top":he(me,"top"),"--n-pane-padding-bottom":he(me,"bottom"),"--n-font-weight-strong":Ct,"--n-tab-color-segment":St}}),oe=S?ta("tabs",de(()=>`${D.value[0]}${e.type[0]}`),He,e):void 0;return Object.assign({mergedClsPrefix:w,mergedValue:g,renderedNames:new Set,segmentCapsuleElRef:ne,tabsPaneWrapperRef:ae,tabsElRef:z,barElRef:L,addTabInstRef:$,xScrollInstRef:k,scrollWrapperElRef:A,addTabFixed:le,tabWrapperStyle:q,handleNavResize:st,mergedSize:D,handleScroll:bt,handleTabsResize:ut,cssVars:S?void 0:He,themeClass:oe==null?void 0:oe.themeClass,animationDirection:W,renderNameListRef:l,yScrollElRef:B,handleSegmentResize:pt,onAnimationBeforeLeave:we,onAnimationEnter:n,onAnimationAfterEnter:r,onRender:oe==null?void 0:oe.onRender},ft)},render(){const{mergedClsPrefix:e,type:o,placement:s,addTabFixed:f,addable:p,mergedSize:c,renderNameListRef:w,onRender:S,paneWrapperClass:T,paneWrapperStyle:R,$slots:{default:z,prefix:L,suffix:A}}=this;S==null||S();const $=z?Re(z()).filter(_=>_.type.__TAB_PANE__===!0):[],k=z?Re(z()).filter(_=>_.type.__TAB__===!0):[],B=!k.length,h=o==="card",C=o==="segment",I=!h&&!C&&this.justifyContent;w.value=[];const D=()=>{const _=m("div",{style:this.tabWrapperStyle,class:`${e}-tabs-wrapper`},I?null:m("div",{class:`${e}-tabs-scroll-padding`,style:s==="top"||s==="bottom"?{width:`${this.tabsPadding}px`}:{height:`${this.tabsPadding}px`}}),B?$.map((g,N)=>(w.value.push(g.props.name),Ie(m(je,Object.assign({},g.props,{internalCreatedByPane:!0,internalLeftPadded:N!==0&&(!I||I==="center"||I==="start"||I==="end")}),g.children?{default:g.children.tab}:void 0)))):k.map((g,N)=>(w.value.push(g.props.name),Ie(N!==0&&!I?tt(g):g))),!f&&p&&h?et(p,(B?$.length:k.length)!==0):null,I?null:m("div",{class:`${e}-tabs-scroll-padding`,style:{width:`${this.tabsPadding}px`}}));return m("div",{ref:"tabsElRef",class:`${e}-tabs-nav-scroll-content`},h&&p?m($e,{onResize:this.handleTabsResize},{default:()=>_}):_,h?m("div",{class:`${e}-tabs-pad`}):null,h?null:m("div",{ref:"barElRef",class:`${e}-tabs-bar`}))},H=C?"top":s;return m("div",{class:[`${e}-tabs`,this.themeClass,`${e}-tabs--${o}-type`,`${e}-tabs--${c}-size`,I&&`${e}-tabs--flex`,`${e}-tabs--${H}`],style:this.cssVars},m("div",{class:[`${e}-tabs-nav--${o}-type`,`${e}-tabs-nav--${H}`,`${e}-tabs-nav`]},Oe(L,_=>_&&m("div",{class:`${e}-tabs-nav__prefix`},_)),C?m($e,{onResize:this.handleSegmentResize},{default:()=>m("div",{class:`${e}-tabs-rail`,ref:"tabsElRef"},m("div",{class:`${e}-tabs-capsule`,ref:"segmentCapsuleElRef"},m("div",{class:`${e}-tabs-wrapper`},m("div",{class:`${e}-tabs-tab`}))),B?$.map((_,g)=>(w.value.push(_.props.name),m(je,Object.assign({},_.props,{internalCreatedByPane:!0,internalLeftPadded:g!==0}),_.children?{default:_.children.tab}:void 0))):k.map((_,g)=>(w.value.push(_.props.name),g===0?_:tt(_))))}):m($e,{onResize:this.handleNavResize},{default:()=>m("div",{class:`${e}-tabs-nav-scroll-wrapper`,ref:"scrollWrapperElRef"},["top","bottom"].includes(H)?m(_a,{ref:"xScrollInstRef",onScroll:this.handleScroll},{default:D}):m("div",{class:`${e}-tabs-nav-y-scroll`,onScroll:this.handleScroll,ref:"yScrollElRef"},D()))}),f&&p&&h?et(p,!0):null,Oe(A,_=>_&&m("div",{class:`${e}-tabs-nav__suffix`},_))),B&&(this.animated&&(H==="top"||H==="bottom")?m("div",{ref:"tabsPaneWrapperRef",style:R,class:[`${e}-tabs-pane-wrapper`,T]},Ze($,this.mergedValue,this.renderedNames,this.onAnimationBeforeLeave,this.onAnimationEnter,this.onAnimationAfterEnter,this.animationDirection)):Ze($,this.mergedValue,this.renderedNames)))}});function Ze(e,o,s,f,p,c,w){const S=[];return e.forEach(T=>{const{name:R,displayDirective:z,"display-directive":L}=T.props,A=k=>z===k||L===k,$=o===R;if(T.key!==void 0&&(T.key=R),$||A("show")||A("show:lazy")&&s.has(R)){s.has(R)||s.add(R);const k=!A("if");S.push(k?ra(T,[[na,$]]):T)}}),w?m(la,{name:`${w}-transition`,onBeforeLeave:f,onEnter:p,onAfterEnter:c},{default:()=>S}):S}function et(e,o){return m(je,{ref:"addTabInstRef",key:"__addable",name:"__addable",internalCreatedByPane:!0,internalAddable:!0,internalLeftPadded:o,disabled:typeof e=="object"&&e.disabled})}function tt(e){const o=oa(e);return o.props?o.props.internalLeftPadded=!0:o.props={internalLeftPadded:!0},o}function Ie(e){return Array.isArray(e.dynamicProps)?e.dynamicProps.includes("internalLeftPadded")||e.dynamicProps.push("internalLeftPadded"):e.dynamicProps=["internalLeftPadded"],e}const ee={list:()=>Z.get("/suites"),get:e=>Z.get(`/suites/${e}`),create:e=>Z.post("/suites",e),update:(e,o)=>Z.put(`/suites/${e}`,o),delete:e=>Z.delete(`/suites/${e}`),run:(e,o)=>Z.post(`/suites/${e}/runs`,o),listRuns:e=>Z.get(`/suites/${e}/runs`),getRun:(e,o)=>Z.get(`/suites/${e}/runs/${o}`)},nr=pe({__name:"SuiteCenter",setup(e){const o=fa(),s=xa(),f=P([]),p=P(!1),c=P(null),w=P([]),S=P(!1),T=P(!1),R=P(!1),z=P(!1),L=P(null),A=P(null),$=P([]),k=P([]),B=P({}),h=P({target_app_id:"",environment:"",override_host:"",concurrency:void 0,perf_threshold_ms:void 0}),C=P({name:"",description:"",default_target_app_id:void 0,default_environment:"",default_concurrency:1,default_delay_ms:0,default_perf_threshold_ms:void 0}),I=P(""),D=de(()=>{if(!I.value)return f.value;const n=I.value.toLowerCase();return f.value.filter(r=>r.name.toLowerCase().includes(n))}),H=Ue({page:1,pageSize:10,showSizePicker:!0,pageSizes:[10,20,50],onChange:n=>{H.page=n},onUpdatePageSize:n=>{H.pageSize=n,H.page=1}}),_=Ue({page:1,pageSize:10,showSizePicker:!0,pageSizes:[10,20,50],onChange:n=>{_.page=n},onUpdatePageSize:n=>{_.pageSize=n,_.page=1}}),g=n=>n>=.9?"#18a058":n>=.6?"#f0a020":"#d03050",N=[{title:"名称",key:"name"},{title:"用例数",key:"case_count",render:n=>{var r;return((r=n.case_ids)==null?void 0:r.length)??0}},{title:"默认环境",key:"default_environment",render:n=>n.default_environment||"-"},{title:"创建时间",key:"created_at",render:n=>Xe(n.created_at)},{title:"操作",key:"actions",width:120,render:n=>m(J,{size:"small",onClick:()=>_e(n)},()=>"查看/执行")}],q=[{title:"状态",key:"status",width:90,render:n=>m("span",{style:`color:${n.status==="DONE"?"#18a058":n.status==="FAILED"?"#d03050":"#f0a020"}`},n.status)},{title:"用例",key:"cases",render:n=>`${n.passed_cases}/${n.total_cases} 通过`},{title:"通过率",key:"rate",render:n=>{const r=Math.round((n.overall_pass_rate??0)*100);return m("span",{style:`color:${g(n.overall_pass_rate??0)};font-weight:bold`},`${r}%`)}},{title:"开始时间",key:"started_at",render:n=>Xe(n.started_at)},{title:"操作",key:"actions",width:120,render:n=>{var r;return(r=n.job_ids)!=null&&r.length?m(J,{size:"small",onClick:()=>o.push(`/results/${n.job_ids[0]}`)},()=>"查看第1个任务"):"-"}}];async function K(){p.value=!0;try{const n=await ee.list();f.value=n.data}finally{p.value=!1}}async function ue(n){S.value=!0;try{const r=await ee.listRuns(n);w.value=r.data}finally{S.value=!1}}function _e(n){c.value=n,_.page=1,h.value={target_app_id:n.default_target_app_id||"",environment:n.default_environment||"",override_host:n.default_override_host||"",concurrency:void 0,perf_threshold_ms:n.default_perf_threshold_ms??void 0},ue(n.id)}function ve(){L.value=null,C.value={name:"",description:"",default_target_app_id:void 0,default_environment:"",default_concurrency:1,default_delay_ms:0,default_perf_threshold_ms:void 0},z.value=!0}function te(n){L.value=n.id,C.value={name:n.name,description:n.description||"",default_target_app_id:n.default_target_app_id||void 0,default_environment:n.default_environment||"",default_concurrency:n.default_concurrency??1,default_delay_ms:n.default_delay_ms??0,default_perf_threshold_ms:n.default_perf_threshold_ms??void 0},z.value=!0}async function ge(){var n,r,l;if(!C.value.name){s.warning("请填写套件名称");return}R.value=!0;try{const W={...C.value};if(W.default_environment||delete W.default_environment,W.description||delete W.description,W.default_perf_threshold_ms||delete W.default_perf_threshold_ms,L.value){const M=await ee.update(L.value,W),re=f.value.findIndex(Te=>Te.id===L.value);re>=0&&(f.value[re]=M.data),((n=c.value)==null?void 0:n.id)===L.value&&(c.value=M.data)}else{const M=await ee.create(W);f.value.unshift(M.data)}z.value=!1,s.success("保存成功")}catch(W){s.error(((l=(r=W.response)==null?void 0:r.data)==null?void 0:l.detail)||"保存失败")}finally{R.value=!1}}async function ae(n){var r,l,W;try{await ee.delete(n),f.value=f.value.filter(M=>M.id!==n),((r=c.value)==null?void 0:r.id)===n&&(c.value=null),s.success("已删除")}catch(M){s.error(((W=(l=M.response)==null?void 0:l.data)==null?void 0:W.detail)||"删除失败")}}async function ce(){var n,r;if(c.value){if(!h.value.target_app_id){s.warning("请选择目标应用");return}T.value=!0;try{const l={target_app_id:h.value.target_app_id};h.value.environment&&(l.environment=h.value.environment),h.value.override_host&&(l.override_host=h.value.override_host),h.value.concurrency&&(l.concurrency=h.value.concurrency),h.value.perf_threshold_ms&&(l.perf_threshold_ms=h.value.perf_threshold_ms),await ee.run(c.value.id,l),s.success("套件已开始执行"),await ue(c.value.id)}catch(l){s.error(((r=(n=l.response)==null?void 0:n.data)==null?void 0:r.detail)||"执行失败")}finally{T.value=!1}}}async function U(n){if(!n||!c.value)return;const r=c.value.case_ids||[];if(r.includes(n)){s.warning("用例已在套件中"),A.value=null;return}const l=[...r,n],W=await ee.update(c.value.id,{case_ids:l});c.value=W.data;const M=f.value.findIndex(re=>re.id===c.value.id);M>=0&&(f.value[M]=W.data),A.value=null,s.success("已添加")}async function we(n){if(!c.value)return;const r=(c.value.case_ids||[]).filter(M=>M!==n),l=await ee.update(c.value.id,{case_ids:r});c.value=l.data;const W=f.value.findIndex(M=>M.id===c.value.id);W>=0&&(f.value[W]=l.data)}return lt(async()=>{const[n,r]=await Promise.all([ga.list(),ma.list({limit:500})]);$.value=n.data.map(l=>({label:l.name,value:l.id})),k.value=r.data.items.map(l=>({label:l.name,value:l.id})),B.value=Object.fromEntries(r.data.items.map(l=>[l.id,l.name])),await K()}),(n,r)=>(ye(),Be(u(Ce),{vertical:"",size:16},{default:y(()=>[b(u(De),{title:"回放套件"},{"header-extra":y(()=>[b(u(Ce),null,{default:y(()=>[b(u(se),{value:I.value,"onUpdate:value":r[0]||(r[0]=l=>I.value=l),placeholder:"搜索套件名称",clearable:"",style:{width:"180px"}},null,8,["value"]),b(u(J),{type:"primary",size:"small",onClick:ve},{default:y(()=>[...r[19]||(r[19]=[Q("+ 新建套件",-1)])]),_:1})]),_:1})]),default:y(()=>[b(u(Ye),{columns:N,data:D.value,loading:p.value,"row-key":l=>l.id,pagination:H},null,8,["data","loading","row-key","pagination"])]),_:1}),c.value?(ye(),Be(u(De),{key:0,title:`套件：${c.value.name}`},{"header-extra":y(()=>[b(u(Ce),null,{default:y(()=>[b(u(J),{size:"small",onClick:r[1]||(r[1]=l=>te(c.value))},{default:y(()=>[...r[20]||(r[20]=[Q("编辑",-1)])]),_:1}),b(u(Ca),{onPositiveClick:r[2]||(r[2]=l=>ae(c.value.id))},{trigger:y(()=>[b(u(J),{size:"small",type:"error"},{default:y(()=>[...r[21]||(r[21]=[Q("删除",-1)])]),_:1})]),default:y(()=>[r[22]||(r[22]=Q(" 确认删除套件？ ",-1))]),_:1})]),_:1})]),default:y(()=>[b(u(Ga),{type:"line",animated:""},{default:y(()=>[b(u(Qe),{name:"run",tab:"执行套件"},{default:y(()=>[b(u(qe),{"label-placement":"left","label-width":"130px",style:{"max-width":"560px","margin-top":"12px"}},{default:y(()=>[b(u(F),{label:"回放目标应用",required:""},{default:y(()=>[b(u(We),{value:h.value.target_app_id,"onUpdate:value":r[3]||(r[3]=l=>h.value.target_app_id=l),options:$.value,placeholder:"选择目标应用"},null,8,["value","options"])]),_:1}),b(u(F),{label:"环境标签"},{default:y(()=>[b(u(se),{value:h.value.environment,"onUpdate:value":r[4]||(r[4]=l=>h.value.environment=l),placeholder:"staging / test（留空用套件默认）"},null,8,["value"])]),_:1}),b(u(F),{label:"Host 覆盖"},{default:y(()=>[b(u(se),{value:h.value.override_host,"onUpdate:value":r[5]||(r[5]=l=>h.value.override_host=l),placeholder:"留空用套件默认"},null,8,["value"])]),_:1}),b(u(F),{label:"并发数"},{default:y(()=>[b(u(fe),{value:h.value.concurrency,"onUpdate:value":r[6]||(r[6]=l=>h.value.concurrency=l),min:1,max:20,placeholder:"留空用套件默认"},null,8,["value"])]),_:1}),b(u(F),{label:"性能阈值(ms)"},{default:y(()=>[b(u(fe),{value:h.value.perf_threshold_ms,"onUpdate:value":r[7]||(r[7]=l=>h.value.perf_threshold_ms=l),min:0,placeholder:"超过此耗时标记 PERF FAIL"},null,8,["value"])]),_:1}),b(u(F),null,{default:y(()=>[b(u(J),{type:"primary",loading:T.value,onClick:ce},{default:y(()=>[...r[23]||(r[23]=[Q("执行套件",-1)])]),_:1},8,["loading"])]),_:1})]),_:1}),b(u(ya)),r[25]||(r[25]=sa("div",{style:{"font-weight":"600","margin-bottom":"8px"}},"执行历史",-1)),b(u(Ye),{columns:q,data:w.value,loading:S.value,size:"small",pagination:_},null,8,["data","loading","pagination"]),b(u(J),{size:"tiny",style:{"margin-top":"8px"},onClick:r[8]||(r[8]=l=>ue(c.value.id))},{default:y(()=>[...r[24]||(r[24]=[Q("刷新",-1)])]),_:1})]),_:1}),b(u(Qe),{name:"cases",tab:"包含用例"},{default:y(()=>[b(u(Ce),{vertical:"",size:8,style:{"margin-top":"12px"}},{default:y(()=>[(ye(!0),da(rt,null,ua(c.value.case_ids,l=>(ye(),Be(u(va),{key:l,closable:"",onClose:W=>we(l)},{default:y(()=>[Q(pa(B.value[l]||l.slice(0,8)),1)]),_:2},1032,["onClose"]))),128)),b(u(We),{value:A.value,"onUpdate:value":[r[9]||(r[9]=l=>A.value=l),U],options:k.value,filterable:"",clearable:"",placeholder:"添加测试用例",style:{width:"300px"}},null,8,["value","options"])]),_:1})]),_:1})]),_:1})]),_:1},8,["title"])):ca("",!0),b(u(ba),{show:z.value,"onUpdate:show":r[18]||(r[18]=l=>z.value=l),preset:"dialog",title:L.value?"编辑套件":"新建套件",style:{width:"520px"}},{action:y(()=>[b(u(J),{onClick:r[17]||(r[17]=l=>z.value=!1)},{default:y(()=>[...r[26]||(r[26]=[Q("取消",-1)])]),_:1}),b(u(J),{type:"primary",loading:R.value,onClick:ge},{default:y(()=>[...r[27]||(r[27]=[Q("保存",-1)])]),_:1},8,["loading"])]),default:y(()=>[b(u(qe),{model:C.value,"label-placement":"left","label-width":"130px"},{default:y(()=>[b(u(F),{label:"套件名称",required:""},{default:y(()=>[b(u(se),{value:C.value.name,"onUpdate:value":r[10]||(r[10]=l=>C.value.name=l),placeholder:"如：用户模块回归测试"},null,8,["value"])]),_:1}),b(u(F),{label:"描述"},{default:y(()=>[b(u(se),{value:C.value.description,"onUpdate:value":r[11]||(r[11]=l=>C.value.description=l),type:"textarea",rows:2},null,8,["value"])]),_:1}),b(u(F),{label:"默认目标应用"},{default:y(()=>[b(u(We),{value:C.value.default_target_app_id,"onUpdate:value":r[12]||(r[12]=l=>C.value.default_target_app_id=l),options:$.value,clearable:"",placeholder:"运行时可覆盖"},null,8,["value","options"])]),_:1}),b(u(F),{label:"默认环境"},{default:y(()=>[b(u(se),{value:C.value.default_environment,"onUpdate:value":r[13]||(r[13]=l=>C.value.default_environment=l),placeholder:"staging"},null,8,["value"])]),_:1}),b(u(F),{label:"默认并发数"},{default:y(()=>[b(u(fe),{value:C.value.default_concurrency,"onUpdate:value":r[14]||(r[14]=l=>C.value.default_concurrency=l),min:1,max:20},null,8,["value"])]),_:1}),b(u(F),{label:"默认延迟(ms)"},{default:y(()=>[b(u(fe),{value:C.value.default_delay_ms,"onUpdate:value":r[15]||(r[15]=l=>C.value.default_delay_ms=l),min:0},null,8,["value"])]),_:1}),b(u(F),{label:"默认性能阈值(ms)"},{default:y(()=>[b(u(fe),{value:C.value.default_perf_threshold_ms,"onUpdate:value":r[16]||(r[16]=l=>C.value.default_perf_threshold_ms=l),min:0,clearable:"",placeholder:"不限制"},null,8,["value"])]),_:1})]),_:1},8,["model"])]),_:1},8,["show","title"])]),_:1}))}});export{nr as default};
