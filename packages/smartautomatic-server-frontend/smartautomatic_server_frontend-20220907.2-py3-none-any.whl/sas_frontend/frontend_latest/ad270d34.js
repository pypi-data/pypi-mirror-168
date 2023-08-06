"use strict";(self.webpackChunksmartautomatic_server_frontend=self.webpackChunksmartautomatic_server_frontend||[]).push([[26136],{26136:(t,r,a)=>{a.a(t,(async t=>{a.r(r);var e=a(37500),s=a(50467),i=a(99476),c=t([i]);i=(c.then?await c:c)[0];class n extends i.p{async getCardSize(){if(!this._cards)return 0;const t=[];for(const r of this._cards)t.push((0,s.N)(r));return(await Promise.all(t)).reduce(((t,r)=>t+r),0)}static get styles(){return[super.sharedStyles,e.iv`
        #root {
          display: flex;
          flex-direction: column;
          height: 100%;
        }
        #root > * {
          margin: var(
            --vertical-stack-card-margin,
            var(--stack-card-margin, 4px 0)
          );
        }
        #root > *:first-child {
          margin-top: 0;
        }
        #root > *:last-child {
          margin-bottom: 0;
        }
      `]}}customElements.define("hui-vertical-stack-card",n)}))}}]);
//# sourceMappingURL=ad270d34.js.map