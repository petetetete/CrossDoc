'use babel';

import CrossdocAtomView from './crossdoc-atom-view';
import { CompositeDisposable } from 'atom';

export default {

  crossdocAtomView: null,
  modalPanel: null,
  subscriptions: null,

  activate(state) {
    this.crossdocAtomView = new CrossdocAtomView(state.crossdocAtomViewState);
    this.modalPanel = atom.workspace.addModalPanel({
      item: this.crossdocAtomView.getElement(),
      visible: false
    });

    // Events subscribed to in atom's system can be easily cleaned up with a CompositeDisposable
    this.subscriptions = new CompositeDisposable();

    // Register command that toggles this view
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:toggle': () => this.toggle()
    }));
    //Register reverseText command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:reverseText': () => this.reverseText()
    }));
    //Register insertAnchor command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:insertAnchor': () => this.insertAnchor()
    }));
    //Register deleteAnchor command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:deleteAnchor': () => this.deleteAnchor()
    }));

  },

  deactivate() {
    this.modalPanel.destroy();
    this.subscriptions.dispose();
    this.crossdocAtomView.destroy();
  },

  serialize() {
    return {
      crossdocAtomViewState: this.crossdocAtomView.serialize()
    };
  },

  insertAnchor() {
    let editor
    if (editor = atom.workspace.getActiveTextEditor())
    {
      let anchorToInsert = "Cdoc #000001abc: "
      editor.insertText(anchorToInsert)
    }
  },

  deleteAnchor() {
    let editor
    if (editor = atom.workspace.getActiveTextEditor())
    {
      let selection = editor.getSelectedText()
      editor.insertText("")
    }
  },

  reverseText() {
    let editor
    if (editor = atom.workspace.getActiveTextEditor())
    {
      let selection = editor.getSelectedText()
      let reversed = selection.split('').reverse().join('')
      editor.insertText(reversed)
    }
  },

  toggle() {
    console.log('CrossDoc was toggled!');
    return (
        this.modalPanel.isVisible() ?
        this.modalPanel.hide() :
        this.modalPanel.show()
        );
    }
};
