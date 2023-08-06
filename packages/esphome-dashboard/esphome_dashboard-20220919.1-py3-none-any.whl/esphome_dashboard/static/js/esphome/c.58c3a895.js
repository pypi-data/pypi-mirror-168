import{k as o,r as a,_ as e,e as t,n,s as i,y as s,K as l}from"./index-83b4bf65.js";import"./c.e04f6a56.js";import"./c.089ef6e1.js";import{W as c}from"./c.21ed9449.js";import{o as d}from"./c.9c2ecd11.js";import{t as r}from"./c.fd0bb12f.js";let m=class extends i{render(){return s`
      <mwc-dialog
        open
        .heading=${this.configuration}
        @closed=${this._handleClose}
      >
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleYamlDownload}
        >
          <span>Download YAML</span>
          <span slot="secondary">
            Download as local backup or share with friends and family
          </span>
          ${c}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleWebDownload}
        >
          <span>Download compiled binary</span>
          <span slot="secondary">
            To install using ESPHome Web and other tools.
          </span>
          ${c}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleManualDownload}
        >
          <span>Download compiled binary (legacy format)</span>
          <span slot="secondary">For use with ESPHome Flasher.</span>
          ${c}
        </mwc-list-item>

        <a
          href=${"https://web.esphome.io/?dashboard_install"}
          target="_blank"
          rel="noopener noreferrer"
          class="bottom-left"
          >Open ESPHome Web</a
        >
        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      </mwc-dialog>
    `}_handleYamlDownload(){l(this.configuration).then((o=>{r(o,this.configuration)}))}_handleManualDownload(){d(this.configuration,!1)}_handleWebDownload(){d(this.configuration,!0)}async _handleClose(){this.parentNode.removeChild(this)}};m.styles=[o,a`
      mwc-list-item {
        margin: 0 -20px;
      }
      svg {
        fill: currentColor;
      }
      a.bottom-left {
        z-index: 1;
        position: absolute;
        line-height: 36px;
        bottom: 9px;
      }
    `],e([t()],m.prototype,"configuration",void 0),m=e([n("esphome-download-choose-dialog")],m);
