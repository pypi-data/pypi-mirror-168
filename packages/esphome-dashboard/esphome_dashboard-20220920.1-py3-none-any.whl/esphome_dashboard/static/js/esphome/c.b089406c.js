import{b as e,e as t,n as o,s as i,y as n,S as a}from"./index-4404568b.js";import"./c.37b69dba.js";import{d as l}from"./c.b120a6fe.js";let d=class extends i{render(){return n`
      <mwc-dialog
        .heading=${`Delete ${this.name}`}
        @closed=${this._handleClose}
        open
      >
        <div>Are you sure you want to delete ${this.name}?</div>
        <mwc-button
          slot="primaryAction"
          label="Delete"
          dialogAction="close"
          @click=${this._handleDelete}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          no-attention
          label="Cancel"
          dialogAction="cancel"
        ></mwc-button>
      </mwc-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}async _handleDelete(){await l(this.configuration),a(this,"deleted")}};e([t()],d.prototype,"name",void 0),e([t()],d.prototype,"configuration",void 0),d=e([o("esphome-delete-device-dialog")],d);
