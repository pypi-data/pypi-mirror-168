import{b as o,e as t,t as e,n as s,s as i,y as r,V as c}from"./index-fad1e0cd.js";import"./c.5096b8c4.js";import{o as n}from"./c.1edac06e.js";import"./c.78fc724b.js";import"./c.c2430a4d.js";import"./c.2c304877.js";let a=class extends i{render(){return r`
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
    `}_openEdit(){c(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){n(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],a.prototype,"configuration",void 0),o([t()],a.prototype,"target",void 0),o([e()],a.prototype,"_result",void 0),a=o([s("esphome-logs-dialog")],a);
