import{b as o,e as i,t,n as e,s,y as n,V as a,k as l}from"./index-fad1e0cd.js";import"./c.5096b8c4.js";import"./c.78fc724b.js";let c=class extends s{render(){const o=void 0===this._valid?"":this._valid?"✅":"❌";return n`
      <esphome-process-dialog
        .heading=${`Validate ${this.configuration} ${o}`}
        .type=${"validate"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_openInstall(){l(this.configuration)}_handleProcessDone(o){this._valid=0==o.detail}_handleClose(){this.parentNode.removeChild(this)}};o([i()],c.prototype,"configuration",void 0),o([t()],c.prototype,"_valid",void 0),c=o([e("esphome-validate-dialog")],c);
