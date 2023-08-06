import{_ as e,e as o,n as s,s as i,y as t}from"./index-83b4bf65.js";import"./c.a094e7d5.js";import"./c.e04f6a56.js";import"./c.fd0bb12f.js";let a=class extends i{render(){return t`
      <esphome-process-dialog
        .heading=${`Clean MQTT discovery topics for ${this.configuration}`}
        .type=${"clean-mqtt"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
      </esphome-process-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}};e([o()],a.prototype,"configuration",void 0),a=e([s("esphome-clean-mqtt-dialog")],a);
