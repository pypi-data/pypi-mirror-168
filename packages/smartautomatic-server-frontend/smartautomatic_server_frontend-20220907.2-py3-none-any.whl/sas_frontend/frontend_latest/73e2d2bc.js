/*! For license information please see 73e2d2bc.js.LICENSE.txt */
"use strict";(self.webpackChunksmartautomatic_server_frontend=self.webpackChunksmartautomatic_server_frontend||[]).push([[17809],{14114:(A,e,t)=>{t.d(e,{P:()=>r});const r=A=>(e,t)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const A=e.constructor._observers;e.constructor._observers=new Map,A.forEach(((A,t)=>e.constructor._observers.set(t,A)))}}else{e.constructor._observers=new Map;const A=e.updated;e.updated=function(e){A.call(this,e),e.forEach(((A,e)=>{const t=this.constructor._observers.get(e);void 0!==t&&t.call(this,this[e],A)}))}}e.constructor._observers.set(t,A)}},61092:(A,e,t)=>{t.d(e,{K:()=>l});var r=t(87480),i=(t(91156),t(14114)),n=t(98734),o=t(37500),s=t(33310),a=t(8636);class l extends o.oi{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new n.A((()=>(this.shouldRenderRipple=!0,this.ripple))),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:A=>{const e=A.type;this.onDown("mousedown"===e?"mouseup":"touchend",A)}}]}get text(){const A=this.textContent;return A?A.trim():""}render(){const A=this.renderText(),e=this.graphic?this.renderGraphic():o.dy``,t=this.hasMeta?this.renderMeta():o.dy``;return o.dy`
      ${this.renderRipple()}
      ${e}
      ${A}
      ${t}`}renderRipple(){return this.shouldRenderRipple?o.dy`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?o.dy`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const A={multi:this.multipleGraphics};return o.dy`
      <span class="mdc-deprecated-list-item__graphic material-icons ${(0,a.$)(A)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return o.dy`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const A=this.twoline?this.renderTwoline():this.renderSingleLine();return o.dy`
      <span class="mdc-deprecated-list-item__text">
        ${A}
      </span>`}renderSingleLine(){return o.dy`<slot></slot>`}renderTwoline(){return o.dy`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(A,e){const t=()=>{window.removeEventListener(A,t),this.rippleHandlers.endPress()};window.addEventListener(A,t),this.rippleHandlers.startPress(e)}fireRequestSelected(A,e){if(this.noninteractive)return;const t=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:e,selected:A}});this.dispatchEvent(t)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const A of this.listeners)for(const e of A.eventNames)A.target.addEventListener(e,A.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const A of this.listeners)for(const e of A.eventNames)A.target.removeEventListener(e,A.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const A=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(A)}}(0,r.__decorate)([(0,s.IO)("slot")],l.prototype,"slotElement",void 0),(0,r.__decorate)([(0,s.GC)("mwc-ripple")],l.prototype,"ripple",void 0),(0,r.__decorate)([(0,s.Cb)({type:String})],l.prototype,"value",void 0),(0,r.__decorate)([(0,s.Cb)({type:String,reflect:!0})],l.prototype,"group",void 0),(0,r.__decorate)([(0,s.Cb)({type:Number,reflect:!0})],l.prototype,"tabindex",void 0),(0,r.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0}),(0,i.P)((function(A){A?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],l.prototype,"disabled",void 0),(0,r.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],l.prototype,"twoline",void 0),(0,r.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],l.prototype,"activated",void 0),(0,r.__decorate)([(0,s.Cb)({type:String,reflect:!0})],l.prototype,"graphic",void 0),(0,r.__decorate)([(0,s.Cb)({type:Boolean})],l.prototype,"multipleGraphics",void 0),(0,r.__decorate)([(0,s.Cb)({type:Boolean})],l.prototype,"hasMeta",void 0),(0,r.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0}),(0,i.P)((function(A){A?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],l.prototype,"noninteractive",void 0),(0,r.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0}),(0,i.P)((function(A){const e=this.getAttribute("role"),t="gridcell"===e||"option"===e||"row"===e||"tab"===e;t&&A?this.setAttribute("aria-selected","true"):t&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(A,"property")}))],l.prototype,"selected",void 0),(0,r.__decorate)([(0,s.SB)()],l.prototype,"shouldRenderRipple",void 0),(0,r.__decorate)([(0,s.SB)()],l.prototype,"_managingList",void 0)},96762:(A,e,t)=>{t.d(e,{W:()=>r});const r=t(37500).iv`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`},45036:(A,e,t)=>{var r=t(37500),i=t(33310),n=t(73366);function o(){o=function(){return A};var A={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(A,e){["method","field"].forEach((function(t){e.forEach((function(e){e.kind===t&&"own"===e.placement&&this.defineClassElement(A,e)}),this)}),this)},initializeClassElements:function(A,e){var t=A.prototype;["method","field"].forEach((function(r){e.forEach((function(e){var i=e.placement;if(e.kind===r&&("static"===i||"prototype"===i)){var n="static"===i?A:t;this.defineClassElement(n,e)}}),this)}),this)},defineClassElement:function(A,e){var t=e.descriptor;if("field"===e.kind){var r=e.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===r?void 0:r.call(A)}}Object.defineProperty(A,e.key,t)},decorateClass:function(A,e){var t=[],r=[],i={static:[],prototype:[],own:[]};if(A.forEach((function(A){this.addElementPlacement(A,i)}),this),A.forEach((function(A){if(!l(A))return t.push(A);var e=this.decorateElement(A,i);t.push(e.element),t.push.apply(t,e.extras),r.push.apply(r,e.finishers)}),this),!e)return{elements:t,finishers:r};var n=this.decorateConstructor(t,e);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(A,e,t){var r=e[A.placement];if(!t&&-1!==r.indexOf(A.key))throw new TypeError("Duplicated element ("+A.key+")");r.push(A.key)},decorateElement:function(A,e){for(var t=[],r=[],i=A.decorators,n=i.length-1;n>=0;n--){var o=e[A.placement];o.splice(o.indexOf(A.key),1);var s=this.fromElementDescriptor(A),a=this.toElementFinisherExtras((0,i[n])(s)||s);A=a.element,this.addElementPlacement(A,e),a.finisher&&r.push(a.finisher);var l=a.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],e);t.push.apply(t,l)}}return{element:A,finishers:r,extras:t}},decorateConstructor:function(A,e){for(var t=[],r=e.length-1;r>=0;r--){var i=this.fromClassDescriptor(A),n=this.toClassDescriptor((0,e[r])(i)||i);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){A=n.elements;for(var o=0;o<A.length-1;o++)for(var s=o+1;s<A.length;s++)if(A[o].key===A[s].key&&A[o].placement===A[s].placement)throw new TypeError("Duplicated element ("+A[o].key+")")}}return{elements:A,finishers:t}},fromElementDescriptor:function(A){var e={kind:A.kind,key:A.key,placement:A.placement,descriptor:A.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===A.kind&&(e.initializer=A.initializer),e},toElementDescriptors:function(A){var e;if(void 0!==A)return(e=A,function(A){if(Array.isArray(A))return A}(e)||function(A){if("undefined"!=typeof Symbol&&null!=A[Symbol.iterator]||null!=A["@@iterator"])return Array.from(A)}(e)||function(A,e){if(A){if("string"==typeof A)return f(A,e);var t=Object.prototype.toString.call(A).slice(8,-1);return"Object"===t&&A.constructor&&(t=A.constructor.name),"Map"===t||"Set"===t?Array.from(A):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?f(A,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(A){var e=this.toElementDescriptor(A);return this.disallowProperty(A,"finisher","An element descriptor"),this.disallowProperty(A,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(A){var e=String(A.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var t=p(A.key),r=String(A.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=A.descriptor;this.disallowProperty(A,"elements","An element descriptor");var n={kind:e,key:t,placement:r,descriptor:Object.assign({},i)};return"field"!==e?this.disallowProperty(A,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=A.initializer),n},toElementFinisherExtras:function(A){return{element:this.toElementDescriptor(A),finisher:c(A,"finisher"),extras:this.toElementDescriptors(A.extras)}},fromClassDescriptor:function(A){var e={kind:"class",elements:A.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(A){var e=String(A.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(A,"key","A class descriptor"),this.disallowProperty(A,"placement","A class descriptor"),this.disallowProperty(A,"descriptor","A class descriptor"),this.disallowProperty(A,"initializer","A class descriptor"),this.disallowProperty(A,"extras","A class descriptor");var t=c(A,"finisher");return{elements:this.toElementDescriptors(A.elements),finisher:t}},runClassFinishers:function(A,e){for(var t=0;t<e.length;t++){var r=(0,e[t])(A);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");A=r}}return A},disallowProperty:function(A,e,t){if(void 0!==A[e])throw new TypeError(t+" can't have a ."+e+" property.")}};return A}function s(A){var e,t=p(A.key);"method"===A.kind?e={value:A.value,writable:!0,configurable:!0,enumerable:!1}:"get"===A.kind?e={get:A.value,configurable:!0,enumerable:!1}:"set"===A.kind?e={set:A.value,configurable:!0,enumerable:!1}:"field"===A.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===A.kind?"field":"method",key:t,placement:A.static?"static":"field"===A.kind?"own":"prototype",descriptor:e};return A.decorators&&(r.decorators=A.decorators),"field"===A.kind&&(r.initializer=A.value),r}function a(A,e){void 0!==A.descriptor.get?e.descriptor.get=A.descriptor.get:e.descriptor.set=A.descriptor.set}function l(A){return A.decorators&&A.decorators.length}function d(A){return void 0!==A&&!(void 0===A.value&&void 0===A.writable)}function c(A,e){var t=A[e];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+e+"' to be a function");return t}function p(A){var e=function(A,e){if("object"!=typeof A||null===A)return A;var t=A[Symbol.toPrimitive];if(void 0!==t){var r=t.call(A,e||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(A)}(A,"string");return"symbol"==typeof e?e:String(e)}function f(A,e){(null==e||e>A.length)&&(e=A.length);for(var t=0,r=new Array(e);t<e;t++)r[t]=A[t];return r}function m(A,e,t){return m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(A,e,t){var r=function(A,e){for(;!Object.prototype.hasOwnProperty.call(A,e)&&null!==(A=u(A)););return A}(A,e);if(r){var i=Object.getOwnPropertyDescriptor(r,e);return i.get?i.get.call(t):i.value}},m(A,e,t||A)}function u(A){return u=Object.setPrototypeOf?Object.getPrototypeOf:function(A){return A.__proto__||Object.getPrototypeOf(A)},u(A)}!function(A,e,t,r){var i=o();if(r)for(var n=0;n<r.length;n++)i=r[n](i);var c=e((function(A){i.initializeInstanceElements(A,p.elements)}),t),p=i.decorateClass(function(A){for(var e=[],t=function(A){return"method"===A.kind&&A.key===n.key&&A.placement===n.placement},r=0;r<A.length;r++){var i,n=A[r];if("method"===n.kind&&(i=e.find(t)))if(d(n.descriptor)||d(i.descriptor)){if(l(n)||l(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(l(n)){if(l(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}a(n,i)}else e.push(n)}return e}(c.d.map(s)),A);i.initializeClassElements(c.F,p.elements),i.runClassFinishers(c.F,p.finishers)}([(0,i.Mo)("ha-clickable-list-item")],(function(A,e){class t extends e{constructor(...e){super(...e),A(this)}}return{F:t,d:[{kind:"field",decorators:[(0,i.Cb)()],key:"href",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"disableHref",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"openNewTab",value:()=>!1},{kind:"field",decorators:[(0,i.IO)("a")],key:"_anchor",value:void 0},{kind:"method",key:"render",value:function(){const A=m(u(t.prototype),"render",this).call(this),e=this.href||"";return r.dy`${this.disableHref?r.dy`<a aria-role="option">${A}</a>`:r.dy`<a
          aria-role="option"
          target=${this.openNewTab?"_blank":""}
          href=${e}
          >${A}</a
        >`}`}},{kind:"method",key:"firstUpdated",value:function(){m(u(t.prototype),"firstUpdated",this).call(this),this.addEventListener("keydown",(A=>{"Enter"!==A.key&&" "!==A.key||this._anchor.click()}))}},{kind:"get",static:!0,key:"styles",value:function(){return[m(u(t),"styles",this),r.iv`
        a {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          padding-left: var(--mdc-list-side-padding, 20px);
          padding-right: var(--mdc-list-side-padding, 20px);
          overflow: hidden;
        }
      `]}}]}}),n.M)},73366:(A,e,t)=>{t.d(e,{M:()=>m});var r=t(61092),i=t(96762),n=t(37500);function o(){o=function(){return A};var A={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(A,e){["method","field"].forEach((function(t){e.forEach((function(e){e.kind===t&&"own"===e.placement&&this.defineClassElement(A,e)}),this)}),this)},initializeClassElements:function(A,e){var t=A.prototype;["method","field"].forEach((function(r){e.forEach((function(e){var i=e.placement;if(e.kind===r&&("static"===i||"prototype"===i)){var n="static"===i?A:t;this.defineClassElement(n,e)}}),this)}),this)},defineClassElement:function(A,e){var t=e.descriptor;if("field"===e.kind){var r=e.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===r?void 0:r.call(A)}}Object.defineProperty(A,e.key,t)},decorateClass:function(A,e){var t=[],r=[],i={static:[],prototype:[],own:[]};if(A.forEach((function(A){this.addElementPlacement(A,i)}),this),A.forEach((function(A){if(!l(A))return t.push(A);var e=this.decorateElement(A,i);t.push(e.element),t.push.apply(t,e.extras),r.push.apply(r,e.finishers)}),this),!e)return{elements:t,finishers:r};var n=this.decorateConstructor(t,e);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(A,e,t){var r=e[A.placement];if(!t&&-1!==r.indexOf(A.key))throw new TypeError("Duplicated element ("+A.key+")");r.push(A.key)},decorateElement:function(A,e){for(var t=[],r=[],i=A.decorators,n=i.length-1;n>=0;n--){var o=e[A.placement];o.splice(o.indexOf(A.key),1);var s=this.fromElementDescriptor(A),a=this.toElementFinisherExtras((0,i[n])(s)||s);A=a.element,this.addElementPlacement(A,e),a.finisher&&r.push(a.finisher);var l=a.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],e);t.push.apply(t,l)}}return{element:A,finishers:r,extras:t}},decorateConstructor:function(A,e){for(var t=[],r=e.length-1;r>=0;r--){var i=this.fromClassDescriptor(A),n=this.toClassDescriptor((0,e[r])(i)||i);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){A=n.elements;for(var o=0;o<A.length-1;o++)for(var s=o+1;s<A.length;s++)if(A[o].key===A[s].key&&A[o].placement===A[s].placement)throw new TypeError("Duplicated element ("+A[o].key+")")}}return{elements:A,finishers:t}},fromElementDescriptor:function(A){var e={kind:A.kind,key:A.key,placement:A.placement,descriptor:A.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===A.kind&&(e.initializer=A.initializer),e},toElementDescriptors:function(A){var e;if(void 0!==A)return(e=A,function(A){if(Array.isArray(A))return A}(e)||function(A){if("undefined"!=typeof Symbol&&null!=A[Symbol.iterator]||null!=A["@@iterator"])return Array.from(A)}(e)||function(A,e){if(A){if("string"==typeof A)return f(A,e);var t=Object.prototype.toString.call(A).slice(8,-1);return"Object"===t&&A.constructor&&(t=A.constructor.name),"Map"===t||"Set"===t?Array.from(A):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?f(A,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(A){var e=this.toElementDescriptor(A);return this.disallowProperty(A,"finisher","An element descriptor"),this.disallowProperty(A,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(A){var e=String(A.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var t=p(A.key),r=String(A.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=A.descriptor;this.disallowProperty(A,"elements","An element descriptor");var n={kind:e,key:t,placement:r,descriptor:Object.assign({},i)};return"field"!==e?this.disallowProperty(A,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=A.initializer),n},toElementFinisherExtras:function(A){return{element:this.toElementDescriptor(A),finisher:c(A,"finisher"),extras:this.toElementDescriptors(A.extras)}},fromClassDescriptor:function(A){var e={kind:"class",elements:A.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(A){var e=String(A.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(A,"key","A class descriptor"),this.disallowProperty(A,"placement","A class descriptor"),this.disallowProperty(A,"descriptor","A class descriptor"),this.disallowProperty(A,"initializer","A class descriptor"),this.disallowProperty(A,"extras","A class descriptor");var t=c(A,"finisher");return{elements:this.toElementDescriptors(A.elements),finisher:t}},runClassFinishers:function(A,e){for(var t=0;t<e.length;t++){var r=(0,e[t])(A);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");A=r}}return A},disallowProperty:function(A,e,t){if(void 0!==A[e])throw new TypeError(t+" can't have a ."+e+" property.")}};return A}function s(A){var e,t=p(A.key);"method"===A.kind?e={value:A.value,writable:!0,configurable:!0,enumerable:!1}:"get"===A.kind?e={get:A.value,configurable:!0,enumerable:!1}:"set"===A.kind?e={set:A.value,configurable:!0,enumerable:!1}:"field"===A.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===A.kind?"field":"method",key:t,placement:A.static?"static":"field"===A.kind?"own":"prototype",descriptor:e};return A.decorators&&(r.decorators=A.decorators),"field"===A.kind&&(r.initializer=A.value),r}function a(A,e){void 0!==A.descriptor.get?e.descriptor.get=A.descriptor.get:e.descriptor.set=A.descriptor.set}function l(A){return A.decorators&&A.decorators.length}function d(A){return void 0!==A&&!(void 0===A.value&&void 0===A.writable)}function c(A,e){var t=A[e];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+e+"' to be a function");return t}function p(A){var e=function(A,e){if("object"!=typeof A||null===A)return A;var t=A[Symbol.toPrimitive];if(void 0!==t){var r=t.call(A,e||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(A)}(A,"string");return"symbol"==typeof e?e:String(e)}function f(A,e){(null==e||e>A.length)&&(e=A.length);for(var t=0,r=new Array(e);t<e;t++)r[t]=A[t];return r}let m=function(A,e,t,r){var i=o();if(r)for(var n=0;n<r.length;n++)i=r[n](i);var c=e((function(A){i.initializeInstanceElements(A,p.elements)}),t),p=i.decorateClass(function(A){for(var e=[],t=function(A){return"method"===A.kind&&A.key===n.key&&A.placement===n.placement},r=0;r<A.length;r++){var i,n=A[r];if("method"===n.kind&&(i=e.find(t)))if(d(n.descriptor)||d(i.descriptor)){if(l(n)||l(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(l(n)){if(l(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}a(n,i)}else e.push(n)}return e}(c.d.map(s)),A);return i.initializeClassElements(c.F,p.elements),i.runClassFinishers(c.F,p.finishers)}([(0,t(33310).Mo)("ha-list-item")],(function(A,e){return{F:class extends e{constructor(...e){super(...e),A(this)}},d:[{kind:"get",static:!0,key:"styles",value:function(){return[i.W,n.iv`
        :host {
          padding-left: var(--mdc-list-side-padding, 20px);
          padding-right: var(--mdc-list-side-padding, 20px);
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction);
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction);
        }
      `]}}]}}),r.K)},77289:(A,e,t)=>{t.d(e,{lC:()=>n,IZ:()=>o,v6:()=>s,Uw:()=>a,jP:()=>l});var r=t(63864),i=t(21897);const n=async A=>{(0,r.I)(A.config.version,2021,2,4)?await A.callWS({type:"supervisor/api",endpoint:"/supervisor/reload",method:"post"}):await A.callApi("POST","saserver/supervisor/reload")},o=async A=>(0,r.I)(A.config.version,2021,2,4)?A.callWS({type:"supervisor/api",endpoint:"/supervisor/info",method:"get"}):(0,i._F)(await A.callApi("GET","saserver/supervisor/info")),s=async A=>(0,r.I)(A.config.version,2021,2,4)?A.callWS({type:"supervisor/api",endpoint:"/info",method:"get"}):(0,i._F)(await A.callApi("GET","saserver/info")),a=async(A,e)=>A.callApi("GET",`saserver/${e.includes("_")?`addons/${e}`:e}/logs`),l=async(A,e)=>{(0,r.I)(A.config.version,2021,2,4)?await A.callWS({type:"supervisor/api",endpoint:"/supervisor/options",method:"post",data:e}):await A.callApi("POST","saserver/supervisor/options",e)}},17809:(A,e,t)=>{t.r(e);t(24103);var r=t(37500),i=t(33310),n=t(7323);t(22098),t(45036);function o(){o=function(){return A};var A={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(A,e){["method","field"].forEach((function(t){e.forEach((function(e){e.kind===t&&"own"===e.placement&&this.defineClassElement(A,e)}),this)}),this)},initializeClassElements:function(A,e){var t=A.prototype;["method","field"].forEach((function(r){e.forEach((function(e){var i=e.placement;if(e.kind===r&&("static"===i||"prototype"===i)){var n="static"===i?A:t;this.defineClassElement(n,e)}}),this)}),this)},defineClassElement:function(A,e){var t=e.descriptor;if("field"===e.kind){var r=e.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===r?void 0:r.call(A)}}Object.defineProperty(A,e.key,t)},decorateClass:function(A,e){var t=[],r=[],i={static:[],prototype:[],own:[]};if(A.forEach((function(A){this.addElementPlacement(A,i)}),this),A.forEach((function(A){if(!l(A))return t.push(A);var e=this.decorateElement(A,i);t.push(e.element),t.push.apply(t,e.extras),r.push.apply(r,e.finishers)}),this),!e)return{elements:t,finishers:r};var n=this.decorateConstructor(t,e);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(A,e,t){var r=e[A.placement];if(!t&&-1!==r.indexOf(A.key))throw new TypeError("Duplicated element ("+A.key+")");r.push(A.key)},decorateElement:function(A,e){for(var t=[],r=[],i=A.decorators,n=i.length-1;n>=0;n--){var o=e[A.placement];o.splice(o.indexOf(A.key),1);var s=this.fromElementDescriptor(A),a=this.toElementFinisherExtras((0,i[n])(s)||s);A=a.element,this.addElementPlacement(A,e),a.finisher&&r.push(a.finisher);var l=a.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],e);t.push.apply(t,l)}}return{element:A,finishers:r,extras:t}},decorateConstructor:function(A,e){for(var t=[],r=e.length-1;r>=0;r--){var i=this.fromClassDescriptor(A),n=this.toClassDescriptor((0,e[r])(i)||i);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){A=n.elements;for(var o=0;o<A.length-1;o++)for(var s=o+1;s<A.length;s++)if(A[o].key===A[s].key&&A[o].placement===A[s].placement)throw new TypeError("Duplicated element ("+A[o].key+")")}}return{elements:A,finishers:t}},fromElementDescriptor:function(A){var e={kind:A.kind,key:A.key,placement:A.placement,descriptor:A.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===A.kind&&(e.initializer=A.initializer),e},toElementDescriptors:function(A){var e;if(void 0!==A)return(e=A,function(A){if(Array.isArray(A))return A}(e)||function(A){if("undefined"!=typeof Symbol&&null!=A[Symbol.iterator]||null!=A["@@iterator"])return Array.from(A)}(e)||function(A,e){if(A){if("string"==typeof A)return f(A,e);var t=Object.prototype.toString.call(A).slice(8,-1);return"Object"===t&&A.constructor&&(t=A.constructor.name),"Map"===t||"Set"===t?Array.from(A):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?f(A,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(A){var e=this.toElementDescriptor(A);return this.disallowProperty(A,"finisher","An element descriptor"),this.disallowProperty(A,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(A){var e=String(A.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var t=p(A.key),r=String(A.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=A.descriptor;this.disallowProperty(A,"elements","An element descriptor");var n={kind:e,key:t,placement:r,descriptor:Object.assign({},i)};return"field"!==e?this.disallowProperty(A,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=A.initializer),n},toElementFinisherExtras:function(A){return{element:this.toElementDescriptor(A),finisher:c(A,"finisher"),extras:this.toElementDescriptors(A.extras)}},fromClassDescriptor:function(A){var e={kind:"class",elements:A.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(A){var e=String(A.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(A,"key","A class descriptor"),this.disallowProperty(A,"placement","A class descriptor"),this.disallowProperty(A,"descriptor","A class descriptor"),this.disallowProperty(A,"initializer","A class descriptor"),this.disallowProperty(A,"extras","A class descriptor");var t=c(A,"finisher");return{elements:this.toElementDescriptors(A.elements),finisher:t}},runClassFinishers:function(A,e){for(var t=0;t<e.length;t++){var r=(0,e[t])(A);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");A=r}}return A},disallowProperty:function(A,e,t){if(void 0!==A[e])throw new TypeError(t+" can't have a ."+e+" property.")}};return A}function s(A){var e,t=p(A.key);"method"===A.kind?e={value:A.value,writable:!0,configurable:!0,enumerable:!1}:"get"===A.kind?e={get:A.value,configurable:!0,enumerable:!1}:"set"===A.kind?e={set:A.value,configurable:!0,enumerable:!1}:"field"===A.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===A.kind?"field":"method",key:t,placement:A.static?"static":"field"===A.kind?"own":"prototype",descriptor:e};return A.decorators&&(r.decorators=A.decorators),"field"===A.kind&&(r.initializer=A.value),r}function a(A,e){void 0!==A.descriptor.get?e.descriptor.get=A.descriptor.get:e.descriptor.set=A.descriptor.set}function l(A){return A.decorators&&A.decorators.length}function d(A){return void 0!==A&&!(void 0===A.value&&void 0===A.writable)}function c(A,e){var t=A[e];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+e+"' to be a function");return t}function p(A){var e=function(A,e){if("object"!=typeof A||null===A)return A;var t=A[Symbol.toPrimitive];if(void 0!==t){var r=t.call(A,e||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(A)}(A,"string");return"symbol"==typeof e?e:String(e)}function f(A,e){(null==e||e>A.length)&&(e=A.length);for(var t=0,r=new Array(e);t<e;t++)r[t]=A[t];return r}!function(A,e,t,r){var i=o();if(r)for(var n=0;n<r.length;n++)i=r[n](i);var c=e((function(A){i.initializeInstanceElements(A,p.elements)}),t),p=i.decorateClass(function(A){for(var e=[],t=function(A){return"method"===A.kind&&A.key===n.key&&A.placement===n.placement},r=0;r<A.length;r++){var i,n=A[r];if("method"===n.kind&&(i=e.find(t)))if(d(n.descriptor)||d(i.descriptor)){if(l(n)||l(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(l(n)){if(l(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}a(n,i)}else e.push(n)}return e}(c.d.map(s)),A);i.initializeClassElements(c.F,p.elements),i.runClassFinishers(c.F,p.finishers)}([(0,i.Mo)("ha-logo-svg")],(function(A,e){return{F:class extends e{constructor(...e){super(...e),A(this)}},d:[{kind:"method",key:"render",value:function(){return r.YP`
    <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="200px" height="200px" viewBox="0 0 200 200" enable-background="new 0 0 200 200" xml:space="preserve">  <image id="image0" width="200" height="200" x="0" y="0"
    href="data:image/png;base64,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
OjM0KzAzOjAwzpg7mgAAAABJRU5ErkJggg==" />
</svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: var(--ha-icon-display, inline-flex);
        align-items: center;
        justify-content: center;
        position: relative;
        vertical-align: middle;
        fill: currentcolor;
        width: var(--mdc-icon-size, 24px);
        height: var(--mdc-icon-size, 24px);
      }
      svg {
        width: 100%;
        height: 100%;
        pointer-events: none;
        display: block;
      }
    `}}]}}),r.oi);var m=t(748),u=t(77289),h=(t(60010),t(11654)),v=t(27322);function y(){y=function(){return A};var A={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(A,e){["method","field"].forEach((function(t){e.forEach((function(e){e.kind===t&&"own"===e.placement&&this.defineClassElement(A,e)}),this)}),this)},initializeClassElements:function(A,e){var t=A.prototype;["method","field"].forEach((function(r){e.forEach((function(e){var i=e.placement;if(e.kind===r&&("static"===i||"prototype"===i)){var n="static"===i?A:t;this.defineClassElement(n,e)}}),this)}),this)},defineClassElement:function(A,e){var t=e.descriptor;if("field"===e.kind){var r=e.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===r?void 0:r.call(A)}}Object.defineProperty(A,e.key,t)},decorateClass:function(A,e){var t=[],r=[],i={static:[],prototype:[],own:[]};if(A.forEach((function(A){this.addElementPlacement(A,i)}),this),A.forEach((function(A){if(!w(A))return t.push(A);var e=this.decorateElement(A,i);t.push(e.element),t.push.apply(t,e.extras),r.push.apply(r,e.finishers)}),this),!e)return{elements:t,finishers:r};var n=this.decorateConstructor(t,e);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(A,e,t){var r=e[A.placement];if(!t&&-1!==r.indexOf(A.key))throw new TypeError("Duplicated element ("+A.key+")");r.push(A.key)},decorateElement:function(A,e){for(var t=[],r=[],i=A.decorators,n=i.length-1;n>=0;n--){var o=e[A.placement];o.splice(o.indexOf(A.key),1);var s=this.fromElementDescriptor(A),a=this.toElementFinisherExtras((0,i[n])(s)||s);A=a.element,this.addElementPlacement(A,e),a.finisher&&r.push(a.finisher);var l=a.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],e);t.push.apply(t,l)}}return{element:A,finishers:r,extras:t}},decorateConstructor:function(A,e){for(var t=[],r=e.length-1;r>=0;r--){var i=this.fromClassDescriptor(A),n=this.toClassDescriptor((0,e[r])(i)||i);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){A=n.elements;for(var o=0;o<A.length-1;o++)for(var s=o+1;s<A.length;s++)if(A[o].key===A[s].key&&A[o].placement===A[s].placement)throw new TypeError("Duplicated element ("+A[o].key+")")}}return{elements:A,finishers:t}},fromElementDescriptor:function(A){var e={kind:A.kind,key:A.key,placement:A.placement,descriptor:A.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===A.kind&&(e.initializer=A.initializer),e},toElementDescriptors:function(A){var e;if(void 0!==A)return(e=A,function(A){if(Array.isArray(A))return A}(e)||function(A){if("undefined"!=typeof Symbol&&null!=A[Symbol.iterator]||null!=A["@@iterator"])return Array.from(A)}(e)||function(A,e){if(A){if("string"==typeof A)return P(A,e);var t=Object.prototype.toString.call(A).slice(8,-1);return"Object"===t&&A.constructor&&(t=A.constructor.name),"Map"===t||"Set"===t?Array.from(A):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?P(A,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(A){var e=this.toElementDescriptor(A);return this.disallowProperty(A,"finisher","An element descriptor"),this.disallowProperty(A,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(A){var e=String(A.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var t=D(A.key),r=String(A.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=A.descriptor;this.disallowProperty(A,"elements","An element descriptor");var n={kind:e,key:t,placement:r,descriptor:Object.assign({},i)};return"field"!==e?this.disallowProperty(A,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=A.initializer),n},toElementFinisherExtras:function(A){return{element:this.toElementDescriptor(A),finisher:z(A,"finisher"),extras:this.toElementDescriptors(A.extras)}},fromClassDescriptor:function(A){var e={kind:"class",elements:A.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(A){var e=String(A.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(A,"key","A class descriptor"),this.disallowProperty(A,"placement","A class descriptor"),this.disallowProperty(A,"descriptor","A class descriptor"),this.disallowProperty(A,"initializer","A class descriptor"),this.disallowProperty(A,"extras","A class descriptor");var t=z(A,"finisher");return{elements:this.toElementDescriptors(A.elements),finisher:t}},runClassFinishers:function(A,e){for(var t=0;t<e.length;t++){var r=(0,e[t])(A);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");A=r}}return A},disallowProperty:function(A,e,t){if(void 0!==A[e])throw new TypeError(t+" can't have a ."+e+" property.")}};return A}function g(A){var e,t=D(A.key);"method"===A.kind?e={value:A.value,writable:!0,configurable:!0,enumerable:!1}:"get"===A.kind?e={get:A.value,configurable:!0,enumerable:!1}:"set"===A.kind?e={set:A.value,configurable:!0,enumerable:!1}:"field"===A.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===A.kind?"field":"method",key:t,placement:A.static?"static":"field"===A.kind?"own":"prototype",descriptor:e};return A.decorators&&(r.decorators=A.decorators),"field"===A.kind&&(r.initializer=A.value),r}function b(A,e){void 0!==A.descriptor.get?e.descriptor.get=A.descriptor.get:e.descriptor.set=A.descriptor.set}function w(A){return A.decorators&&A.decorators.length}function L(A){return void 0!==A&&!(void 0===A.value&&void 0===A.writable)}function z(A,e){var t=A[e];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+e+"' to be a function");return t}function D(A){var e=function(A,e){if("object"!=typeof A||null===A)return A;var t=A[Symbol.toPrimitive];if(void 0!==t){var r=t.call(A,e||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(A)}(A,"string");return"symbol"==typeof e?e:String(e)}function P(A,e){(null==e||e>A.length)&&(e=A.length);for(var t=0,r=new Array(e);t<e;t++)r[t]=A[t];return r}function k(A,e,t){return k="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(A,e,t){var r=function(A,e){for(;!Object.prototype.hasOwnProperty.call(A,e)&&null!==(A=W(A)););return A}(A,e);if(r){var i=Object.getOwnPropertyDescriptor(r,e);return i.get?i.get.call(t):i.value}},k(A,e,t||A)}function W(A){return W=Object.setPrototypeOf?Object.getPrototypeOf:function(A){return A.__proto__||Object.getPrototypeOf(A)},W(A)}const X=[{name:"change_log",path:"/latest-release-notes/",iconPath:"M16.56,5.44L15.11,6.89C16.84,7.94 18,9.83 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12C6,9.83 7.16,7.94 8.88,6.88L7.44,5.44C5.36,6.88 4,9.28 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12C20,9.28 18.64,6.88 16.56,5.44M13,3H11V13H13",iconColor:"#4A5963"},{name:"bug",path:"/issues",iconPath:"M14,12H10V10H14M14,16H10V14H14M20,8H17.19C16.74,7.22 16.12,6.55 15.37,6.04L17,4.41L15.59,3L13.42,5.17C12.96,5.06 12.5,5 12,5C11.5,5 11.04,5.06 10.59,5.17L8.41,3L7,4.41L8.62,6.04C7.88,6.55 7.26,7.22 6.81,8H4V10H6.09C6.04,10.33 6,10.66 6,11V12H4V14H6V15C6,15.34 6.04,15.67 6.09,16H4V18H6.81C7.85,19.79 9.78,21 12,21C14.22,21 16.15,19.79 17.19,18H20V16H17.91C17.96,15.67 18,15.34 18,15V14H20V12H18V11C18,10.66 17.96,10.33 17.91,10H20V8Z",iconColor:"#F1C447"},{name:"help",path:"/community",iconPath:"M10,19H13V22H10V19M12,2C17.35,2.22 19.68,7.62 16.5,11.67C15.67,12.67 14.33,13.33 13.67,14.17C13,15 13,16 13,17H10C10,15.33 10,13.92 10.67,12.92C11.33,11.92 12.67,11.33 13.5,10.67C15.92,8.43 15.32,5.26 12,5A3,3 0 0,0 9,8H6A6,6 0 0,1 12,2Z",iconColor:"#B1345C"}];let Z=function(A,e,t,r){var i=y();if(r)for(var n=0;n<r.length;n++)i=r[n](i);var o=e((function(A){i.initializeInstanceElements(A,s.elements)}),t),s=i.decorateClass(function(A){for(var e=[],t=function(A){return"method"===A.kind&&A.key===n.key&&A.placement===n.placement},r=0;r<A.length;r++){var i,n=A[r];if("method"===n.kind&&(i=e.find(t)))if(L(n.descriptor)||L(i.descriptor)){if(w(n)||w(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(w(n)){if(w(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}b(n,i)}else e.push(n)}return e}(o.d.map(g)),A);return i.initializeClassElements(o.F,s.elements),i.runClassFinishers(o.F,s.finishers)}(null,(function(A,e){class t extends e{constructor(...e){super(...e),A(this)}}return{F:t,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_osInfo",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_saserverInfo",value:void 0},{kind:"method",key:"render",value:function(){var A;const e=this.hass,t=window.CUSTOM_UI_LIST||[];return r.dy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        back-path="/config"
        .header=${this.hass.localize("ui.panel.config.info.caption")}
      >
        <div class="content">
          <ha-card outlined>
            <div class="logo-versions">
              <a
                href=${(0,v.R)(this.hass,"")}
                target="_blank"
                rel="noreferrer"
              >
                <ha-logo-svg
                  title=${this.hass.localize("ui.panel.config.info.smartautomatic_server_logo")}
                >
                </ha-logo-svg>
              </a>
              <div class="versions">
                <span class="ha-version"
                  >SmartAutomatic ${e.connection.saVersion}</span
                >
                ${this._saserverInfo?r.dy`<span
                      >Supervisor ${this._saserverInfo.supervisor}</span
                    >`:""}
                ${null!==(A=this._osInfo)&&void 0!==A&&A.version?r.dy`<span>Operating System ${this._osInfo.version}</span>`:""}
                <span>
                  ${this.hass.localize("ui.panel.config.info.frontend_version","version","20220907.2","type","latest")}
                </span>
              </div>
            </div>
            <mwc-list>
              ${X.map((A=>r.dy`
                  <ha-clickable-list-item
                    graphic="avatar"
                    openNewTab
                    href=${(0,v.R)(this.hass,A.path)}
                    @click=${this._entryClicked}
                  >
                    <div
                      slot="graphic"
                      class="icon-background"
                      .style="background-color: ${A.iconColor}"
                    >
                      <ha-svg-icon .path=${A.iconPath}></ha-svg-icon>
                    </div>
                    <span>
                      ${this.hass.localize(`ui.panel.config.info.items.${A.name}`)}
                    </span>
                  </ha-clickable-list-item>
                `))}
            </mwc-list>
            ${t.length?r.dy`
                  <div class="custom-ui">
                    ${this.hass.localize("ui.panel.config.info.custom_uis")}
                    ${t.map((A=>r.dy`
                        <div>
                          <a href=${A.url} target="_blank"> ${A.name}</a>:
                          ${A.version}
                        </div>
                      `))}
                  </div>
                `:""}
          </ha-card>
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(A){k(W(t.prototype),"firstUpdated",this).call(this,A);const e=(window.CUSTOM_UI_LIST||[]).length;setTimeout((()=>{(window.CUSTOM_UI_LIST||[]).length!==e.length&&this.requestUpdate()}),2e3),(0,n.p)(this.hass,"saserver")&&this._loadSupervisorInfo()}},{kind:"method",key:"_loadSupervisorInfo",value:async function(){const[A,e]=await Promise.all([(0,m.KS)(this.hass),(0,u.v6)(this.hass)]);this._saserverInfo=e,this._osInfo=A}},{kind:"method",key:"_entryClicked",value:function(A){A.currentTarget.blur()}},{kind:"get",static:!0,key:"styles",value:function(){return[h.Qx,r.iv`
        .content {
          padding: 28px 20px 0;
          max-width: 1040px;
          margin: 0 auto;
        }

        ha-logo-svg {
          padding: 12px;
          height: 150px;
          width: 150px;
        }

        ha-card {
          padding: 16px;
          max-width: 600px;
          margin: 0 auto;
          margin-bottom: 24px;
          margin-bottom: max(24px, env(safe-area-inset-bottom));
        }

        .logo-versions {
          display: flex;
          justify-content: flex-start;
          align-items: center;
        }

        .versions {
          display: flex;
          flex-direction: column;
          color: var(--secondary-text-color);
          padding: 12px 0;
          align-self: stretch;
          justify-content: flex-start;
        }

        .ha-version {
          color: var(--primary-text-color);
          font-weight: 500;
          font-size: 16px;
        }

        mwc-list {
          --mdc-list-side-padding: 4px;
        }

        ha-svg-icon {
          height: 24px;
          width: 24px;
          display: block;
          padding: 8px;
          color: #fff;
        }

        .icon-background {
          border-radius: 50%;
        }

        @media all and (max-width: 500px), all and (max-height: 500px) {
          ha-logo-svg {
            height: 100px;
            width: 100px;
          }
        }

        .custom-ui {
          color: var(--secondary-text-color);
          text-align: center;
        }
      `]}}]}}),r.oi);customElements.define("ha-config-info",Z)},27322:(A,e,t)=>{t.d(e,{R:()=>r});const r=(A,e)=>`https://${A.config.version.includes("b")?"rc":A.config.version.includes("dev")?"next":"www"}.smartautomatic.duckdns.org:8091${e}`}}]);
//# sourceMappingURL=73e2d2bc.js.map