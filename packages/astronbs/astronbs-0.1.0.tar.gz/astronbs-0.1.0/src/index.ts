import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ILauncher } from '@jupyterlab/launcher';
import { imageIcon } from '@jupyterlab/ui-components';

import { requestAPI } from './handler';

/**
 * Initialization data for the astronbs extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'astronbs:plugin',
  autoStart: true,
  optional: [ISettingRegistry, ILauncher, IFileBrowserFactory, IDocumentManager],
  activate: (
    app: JupyterFrontEnd, 
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher | null,
    fileBrowser: IFileBrowserFactory,
    docManager: IDocumentManager | null
  ) => {
    console.log('JupyterLab extension astronbs is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('astronbs settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for astronbs.', reason);
        });
    }

    app.commands.addCommand('astronbs:reduction_template', {
      // code to run when this command is executed
      execute: () => {
        // const widget = new TutorialWidget();
        // const main = new MainAreaWidget({ content: widget });
        // const button = new ToolbarButton({icon: refreshIcon, onClick: () => widget.load_image()});

        // main.title.label = 'Tutorial Widget';
        // main.title.icon = imageIcon;
        // main.title.caption = widget.title.label;

        // // TODO: add a button to refresh image
        // main.toolbar.addItem('Refresh', button);
        // app.shell.add(main, 'main');
        const reply = requestAPI<any>(
          'reduction_template', 
          {
            body: JSON.stringify({'path': fileBrowser.defaultBrowser.model.path}), 
            method: 'POST'
          }
        );
        console.log("I am back in open2");
        console.log(reply)
        reply.then(data => {
          console.log(data);
          if (docManager) {
            docManager.open(data['path']);
          }
          ///const panel = new NotebookWidgetFactory(context=model);
        });

        //
        //

        // widget.make_a_file(fileBrowser.defaultBrowser.model.path);
      },
      icon: imageIcon,
      label: 'Reduction Template'
    });
    // Add item to launcher
    if (launcher) {
      launcher.add({
        command: 'astronbs:reduction_template',
        category: 'Astro',
        rank: 0
      });
    }

    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The astronbs server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
