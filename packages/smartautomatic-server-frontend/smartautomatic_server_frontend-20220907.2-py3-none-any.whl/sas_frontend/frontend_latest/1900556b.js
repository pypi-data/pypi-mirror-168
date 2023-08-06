"use strict";(self.webpackChunksmartautomatic_server_frontend=self.webpackChunksmartautomatic_server_frontend||[]).push([[89173],{89173:(t,a,r)=>{r.a(t,(async t=>{r.r(a);var s=r(37500),e=r(50467),i=r(99476),n=t([i]);i=(n.then?await n:n)[0];class c extends i.p{async getCardSize(){if(!this._cards)return 0;const t=[];for(const a of this._cards)t.push((0,e.N)(a));const a=await Promise.all(t);return Math.max(...a)}static get styles(){return[super.sharedStyles,s.iv`
        #root {
          display: flex;
          height: 100%;
        }
        #root > * {
          flex: 1 1 0;
          margin: var(
            --horizontal-stack-card-margin,
            var(--stack-card-margin, 0 4px)
          );
          min-width: 0;
        }
        #root > *:first-child {
          margin-left: 0;
        }
        #root > *:last-child {
          margin-right: 0;
        }
      `]}}customElements.define("hui-horizontal-stack-card",c)}))}}]);
//# sourceMappingURL=1900556b.js.map