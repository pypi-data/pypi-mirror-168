import { Widget } from '@lumino/widgets';

export class BaseWidget extends Widget {
  constructor() {
    super();
    this.addClass('jp-creative-widget');
    this.id = 'creative-widget';
    this.title.label = 'Creative Widget';
    this.title.closable = true;
  }
}

// import { MainAreaWidget } from '@jupyterlab/apputils';

// export class BaseWidget {
//   constructor() {
//     const content = new Widget();
//     const widget = MainAreaWidget({ content });
//     widget.id = 'creative-widget';
//     widget.title.label = 'Creative Widget';
//     widget.title.closable = true;
//   }
// }

// export class BaseWidget extends Widget {
//   constructor() {
//     super();
//     const widget = MainAreaWidget({ Widget });
//   }
// }
