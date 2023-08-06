import{r as o,_ as e,e as t,t as i,n as r,s,y as a}from"./index-83b4bf65.js";import"./c.a094e7d5.js";import{o as n}from"./c.9c2ecd11.js";import{e as c}from"./c.72e41bd1.js";import"./c.e04f6a56.js";import"./c.fd0bb12f.js";let d=class extends s{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return a`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?a`
              <a
                slot="secondaryAction"
                href="${c(this.configuration,this.downloadFactoryFirmware)}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const e=document.createElement("a");e.download=this.configuration+".bin",e.href=c(this.configuration,this.downloadFactoryFirmware),document.body.appendChild(e),e.click(),e.remove()}_handleRetry(){n(this.configuration,this.downloadFactoryFirmware)}_handleClose(){this.parentNode.removeChild(this)}};d.styles=o`
    a {
      text-decoration: none;
    }
  `,e([t()],d.prototype,"configuration",void 0),e([t()],d.prototype,"downloadFactoryFirmware",void 0),e([i()],d.prototype,"_result",void 0),d=e([r("esphome-compile-dialog")],d);
