/* eslint-disable prettier/prettier */
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
/* eslint-disable @typescript-eslint/ban-types */
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { Dialog, ToolbarButton } from '@jupyterlab/apputils';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { getFileContents, openLab } from '../tools';
import { axiosHandler, postLabModel,} from '../handler';
import { showFailureImportLabDialog } from '../dialog';
import { Globals } from '../config';
import { extractAtlasTokenFromQuery, SET_DEFAULT_LAB_NAME_AND_KERNEL, MODE } from '../config';

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  NotebookPanel,
  INotebookModel,
  INotebookTracker
} from '@jupyterlab/notebook';

import { SkillsNetworkFileLibrary } from '../sn-file-library';

/**
 * The plugin registration information.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  activate,
  id: 'skillsnetwork-authoring-extension:plugin',
  autoStart: true,
  requires: [IMainMenu, INotebookTracker, IDocumentManager],
};

/**
 * A notebook widget extension that adds a button to the toolbar.
 */
export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  /**
   * Create a new extension for the notebook panel widget.
   *
   * @param panel Notebook panel
   * @param context Notebook context
   * @returns Disposable on the added button
   */
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    if (Globals.SHOW_PUBLISH_BUTTON_FOR !== context.path) {
      // This is not a Skills Network Lab notebook so return a no-op disposable
      return new DisposableDelegate(() => {});
    } else {
      // This is a Skills Network Lab notebook so add the publish button
      const start = async () => {
        // Get the current file contents
        const file = await getFileContents(panel, context);
        // POST to Atlas the file contents/lab model
        const token = Globals.TOKENS.get(panel.id)
        if (token === undefined) {
          console.log('No atlas token found for id', panel.id);
          return;
        }

        postLabModel(axiosHandler(token), file);
      };

      const publishButton = new ToolbarButton({
        className: 'publish-lab-button',
        label: 'Publish on SN',
        onClick: start,
        tooltip: 'Publish Lab'
      });

      const snFileLibraryButton = new ToolbarButton({
        className: 'sn-file-library-button',
        label: 'SN File Library',
        onClick: () =>  (new SkillsNetworkFileLibrary(panel.id)).launch(),
        tooltip: 'Skills Network File Library'
      });

      panel.toolbar.insertItem(9, 'sn-file-library', snFileLibraryButton);
      panel.toolbar.insertItem(10, 'publish', publishButton);
      return new DisposableDelegate(() => {
        publishButton.dispose();
        snFileLibraryButton.dispose();
      });
    }
  }
}

/**
 * Activate the extension.
 *
 * @param app Main application object
 */
async function activate(app: JupyterFrontEnd, mainMenu: IMainMenu, notebookTracker: INotebookTracker, docManager: IDocumentManager) {

  console.log("Activated skillsnetwork-authoring-extension button plugin!");

  if (await MODE() == "learn") return

  // init the token
  const token = await extractAtlasTokenFromQuery();

  //init globals
  const env_type = await SET_DEFAULT_LAB_NAME_AND_KERNEL()

  console.log('Using default kernel: ', Globals.PY_KERNEL_NAME);

  // Add the Publish widget to the lab environment
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());

  // Try to load up a notebook when author is using the browser tool (not in local)
  app.restored.then(async () => {
    if (token !== 'NO_TOKEN' && env_type !== "local"){
      try{
        await openLab(token, docManager);
      }
      catch (e){
        Dialog.flush() // remove spinner
        showFailureImportLabDialog();
        console.log(e)
      }
    }
  })
}

/**
 * Export the plugin as default.
 */
export default plugin;
