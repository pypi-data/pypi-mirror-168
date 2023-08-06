import{w as t,O as e,D as o,W as i,q as s,r as a,b as r,e as n,t as l,n as c,s as d,y as p}from"./index-4404568b.js";import{g as h}from"./c.4c2fa6da.js";import"./c.37b69dba.js";import{E as m,c as u,o as w}from"./c.9109f225.js";import{W as _,s as g,a as v}from"./c.a91cfa45.js";import{o as b}from"./c.d01de6a8.js";import{g as f,a as $,e as y}from"./c.b120a6fe.js";class k{constructor(t){this.Y=t}disconnect(){this.Y=void 0}reconnect(t){this.Y=t}deref(){return this.Y}}class C{constructor(){this.Z=void 0,this.q=void 0}get(){return this.Z}pause(){var t;null!==(t=this.Z)&&void 0!==t||(this.Z=new Promise((t=>this.q=t)))}resume(){var t;null===(t=this.q)||void 0===t||t.call(this),this.Z=this.q=void 0}}const S=t=>!i(t)&&"function"==typeof t.then;const P=t(class extends e{constructor(){super(...arguments),this._$Cwt=1073741823,this._$Cyt=[],this._$CK=new k(this),this._$CX=new C}render(...t){var e;return null!==(e=t.find((t=>!S(t))))&&void 0!==e?e:o}update(t,e){const i=this._$Cyt;let s=i.length;this._$Cyt=e;const a=this._$CK,r=this._$CX;this.isConnected||this.disconnected();for(let t=0;t<e.length&&!(t>this._$Cwt);t++){const o=e[t];if(!S(o))return this._$Cwt=t,o;t<s&&o===i[t]||(this._$Cwt=1073741823,s=0,Promise.resolve(o).then((async t=>{for(;r.get();)await r.get();const e=a.deref();if(void 0!==e){const i=e._$Cyt.indexOf(o);i>-1&&i<e._$Cwt&&(e._$Cwt=i,e.setValue(t))}})))}return o}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}}),x=(t,e)=>{import("./c.9b58010d.js");const o=document.createElement("esphome-compile-dialog");o.configuration=t,o.downloadFactoryFirmware=e,document.body.append(o)},W=async(t,e)=>{let o;if(import("./c.f6d5b730.js"),t.port)o=new m(t.port,console);else try{o=await u(console)}catch(o){return void("NotFoundError"===o.name?w((()=>W(t,e))):alert(`Unable to connect: ${o.message}`))}e&&e();const i=document.createElement("esphome-install-web-dialog");i.params=t,i.esploader=o,document.body.append(i)};let A=class extends d{constructor(){super(...arguments),this._ethernet=!1,this._state="pick_option"}render(){let t,e;return"pick_option"===this._state?(t=`How do you want to install ${this.configuration} on your device?`,e=p`
        <mwc-list-item
          twoline
          hasMeta
          .port=${"OTA"}
          @click=${this._handleLegacyOption}
        >
          <span>${this._ethernet?"Via the network":"Wirelessly"}</span>
          <span slot="secondary">Requires the device to be online</span>
          ${_}
        </mwc-list-item>

        ${this._error?p`<div class="error">${this._error}</div>`:""}

        <mwc-list-item twoline hasMeta @click=${this._handleBrowserInstall}>
          <span>Plug into this computer</span>
          <span slot="secondary">
            For devices connected via USB to this computer
          </span>
          ${_}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
          <span>Plug into the computer running ESPHome Dashboard</span>
          <span slot="secondary">
            For devices connected via USB to the server
          </span>
          ${_}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          @click=${()=>{this._state="pick_download_type"}}
        >
          <span>Manual download</span>
          <span slot="secondary">
            Install it yourself using ESPHome Web or other tools
          </span>
          ${_}
        </mwc-list-item>

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"pick_server_port"===this._state?(t="Pick Server Port",e=void 0===this._ports?this._renderProgress("Loading serial devices"):0===this._ports.length?this._renderMessage("👀","No serial devices found.",!0):p`
              ${this._ports.map((t=>p`
                  <mwc-list-item
                    twoline
                    hasMeta
                    .port=${t.port}
                    @click=${this._handleLegacyOption}
                  >
                    <span>${t.desc}</span>
                    <span slot="secondary">${t.port}</span>
                    ${_}
                  </mwc-list-item>
                `))}

              <mwc-button
                no-attention
                slot="primaryAction"
                label="Back"
                @click=${()=>{this._state="pick_option"}}
              ></mwc-button>
            `):"pick_download_type"===this._state?(t="What version do you want to download?",e=p`
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleWebDownload}
        >
          <span>Modern format</span>
          <span slot="secondary">
            For use with ESPHome Web and other tools.
          </span>
          ${_}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleManualDownload}
        >
          <span>Legacy format</span>
          <span slot="secondary">For use with ESPHome Flasher.</span>
          ${_}
        </mwc-list-item>

        <a
          href="https://web.esphome.io"
          target="_blank"
          rel="noopener noreferrer"
          class="bottom-left"
          >Open ESPHome Web</a
        >
        <mwc-button
          no-attention
          slot="primaryAction"
          label="Back"
          @click=${()=>{this._state="pick_option"}}
        ></mwc-button>
      `):"web_instructions"===this._state&&(t="Install ESPHome via the browser",e=p`
        <div>
          ESPHome can install ${this.configuration} on your device via the
          browser if certain requirements are met:
        </div>
        <ul>
          <li>ESPHome is visited over HTTPS</li>
          <li>Your browser supports WebSerial</li>
        </ul>
        <div>
          Not all requirements are currently met. The easiest solution is to
          download your project and do the installation with ESPHome Web.
          ESPHome Web works 100% in your browser and no data will be shared with
          the ESPHome project.
        </div>
        <ol>
          <li>
            ${P(this._compileConfiguration,p`<a download disabled href="#">Download project</a>
                preparing&nbsp;download…
                <mwc-circular-progress
                  density="-8"
                  indeterminate
                ></mwc-circular-progress>`)}
          </li>
          <li>
            <a href=${"https://web.esphome.io/?dashboard_install"} target="_blank" rel="noopener"
              >Open ESPHome Web</a
            >
          </li>
        </ol>

        <mwc-button
          no-attention
          slot="secondaryAction"
          label="Back"
          @click=${()=>{this._state="pick_option"}}
        ></mwc-button>
        <mwc-button
          no-attention
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
      `),p`
      <mwc-dialog
        open
        heading=${t}
        scrimClickAction
        @closed=${this._handleClose}
        .hideActions=${!1}
      >
        ${e}
      </mwc-dialog>
    `}_renderProgress(t,e){return p`
      <div class="center">
        <div>
          <mwc-circular-progress
            active
            ?indeterminate=${void 0===e}
            .progress=${void 0!==e?e/100:void 0}
            density="8"
          ></mwc-circular-progress>
          ${void 0!==e?p`<div class="progress-pct">${e}%</div>`:""}
        </div>
        ${t}
      </div>
    `}_renderMessage(t,e,o){return p`
      <div class="center">
        <div class="icon">${t}</div>
        ${e}
      </div>
      ${o&&p`
        <mwc-button
          slot="primaryAction"
          dialogAction="ok"
          label="Close"
        ></mwc-button>
      `}
    `}firstUpdated(t){super.firstUpdated(t),this._updateSerialPorts(),f(this.configuration).then((t=>{this._ethernet=t.loaded_integrations.includes("ethernet")}))}async _updateSerialPorts(){this._ports=await h()}willUpdate(t){super.willUpdate(t),t.has("_state")&&"web_instructions"===this._state&&!this._compileConfiguration&&(this._abortCompilation=new AbortController,this._compileConfiguration=$(this.configuration).then((()=>p`
            <a download href="${y(this.configuration,!0)}"
              >Download project</a
            >
          `),(()=>p`
            <a download disabled href="#">Download project</a>
            <span class="prepare-error">preparation failed:</span>
            <button
              class="link"
              dialogAction="close"
              @click=${this._handleWebDownload}
            >
              see what went wrong
            </button>
          `)).finally((()=>{this._abortCompilation=void 0})))}updated(t){if(super.updated(t),t.has("_state"))if("pick_server_port"===this._state){const t=async()=>{await this._updateSerialPorts(),this._updateSerialInterval=window.setTimeout((async()=>{await t()}),5e3)};t()}else"pick_server_port"===t.get("_state")&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0)}_storeDialogWidth(){this.style.setProperty("--mdc-dialog-min-width",`${this.shadowRoot.querySelector("mwc-list-item").clientWidth+4}px`)}_showServerPorts(){this._storeDialogWidth(),this._state="pick_server_port"}_handleManualDownload(){x(this.configuration,!1)}_handleWebDownload(){x(this.configuration,!0)}_handleLegacyOption(t){b(this.configuration,t.currentTarget.port),this._close()}_handleBrowserInstall(){if(!g||!v)return this._storeDialogWidth(),void(this._state="web_instructions");W({configuration:this.configuration},(()=>this._close()))}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){var t;null===(t=this._abortCompilation)||void 0===t||t.abort(),this._updateSerialInterval&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0),this.parentNode.removeChild(this)}};A.styles=[s,a`
      mwc-list-item {
        margin: 0 -20px;
      }
      svg {
        fill: currentColor;
      }
      .center {
        text-align: center;
      }
      mwc-circular-progress {
        margin-bottom: 16px;
      }
      li mwc-circular-progress {
        margin: 0;
      }
      .progress-pct {
        position: absolute;
        top: 50px;
        left: 0;
        right: 0;
      }
      .icon {
        font-size: 50px;
        line-height: 80px;
        color: black;
      }
      .show-ports {
        margin-top: 16px;
      }
      .error {
        padding: 8px 24px;
        background-color: #fff59d;
        margin: 0 -24px;
      }
      .prepare-error {
        color: var(--alert-error-color);
      }
      li a {
        display: inline-block;
        margin-right: 8px;
      }
      a[disabled] {
        pointer-events: none;
        color: #999;
      }
      ol {
        margin-bottom: 0;
      }
      a.bottom-left {
        z-index: 1;
        position: absolute;
        line-height: 36px;
        bottom: 9px;
      }
    `],r([n()],A.prototype,"configuration",void 0),r([l()],A.prototype,"_ethernet",void 0),r([l()],A.prototype,"_ports",void 0),r([l()],A.prototype,"_state",void 0),r([l()],A.prototype,"_error",void 0),A=r([c("esphome-install-choose-dialog")],A);var E=Object.freeze({__proto__:null});export{W as a,E as i,x as o};
