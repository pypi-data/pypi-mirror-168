import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ILauncher } from '@jupyterlab/launcher';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { imageIcon } from '@jupyterlab/ui-components';
import { NotebookModel } from '@jupyterlab/notebook';

import { requestAPI } from './handler';

/**
 * Initialization data for the wooty_woot extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'wooty_woot:plugin',
  autoStart: true,
  optional: [ISettingRegistry, ILauncher, IFileBrowserFactory, IDocumentManager],
  activate: (
    app: JupyterFrontEnd, 
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher | null,
    fileBrowser: IFileBrowserFactory,
    docManager: IDocumentManager | null
  ) => {
    console.log('JupyterLab extension wooty_woot is activated!');

    // Load the settings from schema/plugin.json
    // This can include adding commands to a context menu
    // or to the main or other menu
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('wooty_woot settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for wooty_woot.', reason);
        });
    }

    app.commands.addCommand('wooty_woot:open', {
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
          'viewer', 
          {
            body: JSON.stringify({'path': fileBrowser.defaultBrowser.model.path}), 
            method: 'POST'
          }
        );
        console.log("Aaaand I'm back");
        console.log(reply)
        reply.then(data => {
          console.log(data);
          const model = new NotebookModel();
          model.fromString(data["content"]);
          //app.shell.content.model = model;
          console.log(model);
          app.commands.execute(
            "notebook:create-new",
            { activate: true }
          ).then(notebook => {
            notebook.content.model = model;
          });
          ///const panel = new NotebookWidgetFactory(context=model);
        });

        //
        //

        // widget.make_a_file(fileBrowser.defaultBrowser.model.path);
      },
      icon: imageIcon,
      label: 'Open Tutorial Widget'
    });

    app.commands.addCommand('wooty_woot:open2', {
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
          'miewer', 
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
      label: 'Open TWOOOOO'
    });
    // Add item to launcher
    if (launcher) {
      launcher.add({
        command: 'wooty_woot:open',
        category: 'Moo'
      });
      launcher.add({
        command: 'wooty_woot:open2',
        category: 'Moo'
      });
    }

    requestAPI<any>('viewer')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The wooty_woot server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
