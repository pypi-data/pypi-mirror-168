import{_ as o,e as t,t as e,n as s,s as i,y as r,O as n}from"./index-83b4bf65.js";import"./c.a094e7d5.js";import{o as a}from"./c.9e8d87de.js";import"./c.e04f6a56.js";import"./c.fd0bb12f.js";import"./c.e776f311.js";import"./c.21ed9449.js";let c=class extends i{render(){return r`
      <esphome-process-dialog
        always-show-close
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){n(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){a(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],c.prototype,"configuration",void 0),o([t()],c.prototype,"target",void 0),o([e()],c.prototype,"_result",void 0),c=o([s("esphome-logs-dialog")],c);
