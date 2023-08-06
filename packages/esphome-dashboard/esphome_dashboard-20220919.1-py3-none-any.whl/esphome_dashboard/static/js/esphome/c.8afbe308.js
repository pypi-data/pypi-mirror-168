import{q as t,J as e,z as o,P as i,k as s,r,_ as a,e as n,t as l,n as c,s as d,y as p}from"./index-83b4bf65.js";import{g as h}from"./c.e776f311.js";import"./c.e04f6a56.js";import"./c.089ef6e1.js";import{W as m,s as u,a as _}from"./c.21ed9449.js";import{o as w}from"./c.f5c30fa1.js";import{o as v}from"./c.9c2ecd11.js";import{E as g,c as b,o as f}from"./c.ff3a4769.js";import{g as $,a as y,e as C}from"./c.72e41bd1.js";class k{constructor(t){this.Y=t}disconnect(){this.Y=void 0}reconnect(t){this.Y=t}deref(){return this.Y}}class S{constructor(){this.Z=void 0,this.q=void 0}get(){return this.Z}pause(){var t;null!==(t=this.Z)&&void 0!==t||(this.Z=new Promise((t=>this.q=t)))}resume(){var t;null===(t=this.q)||void 0===t||t.call(this),this.Z=this.q=void 0}}const P=t=>!i(t)&&"function"==typeof t.then;const x=t(class extends e{constructor(){super(...arguments),this._$Cwt=1073741823,this._$Cyt=[],this._$CK=new k(this),this._$CX=new S}render(...t){var e;return null!==(e=t.find((t=>!P(t))))&&void 0!==e?e:o}update(t,e){const i=this._$Cyt;let s=i.length;this._$Cyt=e;const r=this._$CK,a=this._$CX;this.isConnected||this.disconnected();for(let t=0;t<e.length&&!(t>this._$Cwt);t++){const o=e[t];if(!P(o))return this._$Cwt=t,o;t<s&&o===i[t]||(this._$Cwt=1073741823,s=0,Promise.resolve(o).then((async t=>{for(;a.get();)await a.get();const e=r.deref();if(void 0!==e){const i=e._$Cyt.indexOf(o);i>-1&&i<e._$Cwt&&(e._$Cwt=i,e.setValue(t))}})))}return o}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}}),j=async(t,e)=>{let o;if(import("./c.b5cd2d8a.js"),t.port)o=new g(t.port,console);else try{o=await b(console)}catch(o){return void("NotFoundError"===o.name?f((()=>j(t,e))):alert(`Unable to connect: ${o.message}`))}e&&e();const i=document.createElement("esphome-install-web-dialog");i.params=t,i.esploader=o,document.body.append(i)};let A=class extends d{constructor(){super(...arguments),this._ethernet=!1,this._state="pick_option"}render(){let t,e;return"pick_option"===this._state?(t=`How do you want to install ${this.configuration} on your device?`,e=p`
        <mwc-list-item
          twoline
          hasMeta
          .port=${"OTA"}
          @click=${this._handleLegacyOption}
        >
          <span>${this._ethernet?"Via the network":"Wirelessly"}</span>
          <span slot="secondary">Requires the device to be online</span>
          ${m}
        </mwc-list-item>

        ${this._error?p`<div class="error">${this._error}</div>`:""}

        <mwc-list-item twoline hasMeta @click=${this._handleBrowserInstall}>
          <span>Plug into this computer</span>
          <span slot="secondary">
            For devices connected via USB to this computer
          </span>
          ${m}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
          <span>Plug into the computer running ESPHome Dashboard</span>
          <span slot="secondary">
            For devices connected via USB to the server
          </span>
          ${m}
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
                    ${m}
                  </mwc-list-item>
                `))}

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
            ${x(this._compileConfiguration,p`<a download disabled href="#">Download project</a>
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
    `}firstUpdated(t){super.firstUpdated(t),this._updateSerialPorts(),$(this.configuration).then((t=>{this._ethernet=t.loaded_integrations.includes("ethernet")}))}async _updateSerialPorts(){this._ports=await h()}willUpdate(t){super.willUpdate(t),t.has("_state")&&"web_instructions"===this._state&&!this._compileConfiguration&&(this._abortCompilation=new AbortController,this._compileConfiguration=y(this.configuration).then((()=>p`
            <a download href="${C(this.configuration,!0)}"
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
          `)).finally((()=>{this._abortCompilation=void 0})))}updated(t){if(super.updated(t),t.has("_state"))if("pick_server_port"===this._state){const t=async()=>{await this._updateSerialPorts(),this._updateSerialInterval=window.setTimeout((async()=>{await t()}),5e3)};t()}else"pick_server_port"===t.get("_state")&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0)}_storeDialogWidth(){this.style.setProperty("--mdc-dialog-min-width",`${this.shadowRoot.querySelector("mwc-list-item").clientWidth+4}px`)}_showServerPorts(){this._storeDialogWidth(),this._state="pick_server_port"}_handleWebDownload(){v(this.configuration,!0)}_handleLegacyOption(t){w(this.configuration,t.currentTarget.port),this._close()}_handleBrowserInstall(){if(!u||!_)return this._storeDialogWidth(),void(this._state="web_instructions");j({configuration:this.configuration},(()=>this._close()))}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){var t;null===(t=this._abortCompilation)||void 0===t||t.abort(),this._updateSerialInterval&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0),this.parentNode.removeChild(this)}};A.styles=[s,r`
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
    `],a([n()],A.prototype,"configuration",void 0),a([l()],A.prototype,"_ethernet",void 0),a([l()],A.prototype,"_ports",void 0),a([l()],A.prototype,"_state",void 0),a([l()],A.prototype,"_error",void 0),A=a([c("esphome-install-choose-dialog")],A);var W=Object.freeze({__proto__:null});export{W as i,j as o};
