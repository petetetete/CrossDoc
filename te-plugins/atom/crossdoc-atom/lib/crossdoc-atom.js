'use babel';

import CrossdocAtomView from './crossdoc-atom-view';
import { CompositeDisposable } from 'atom';
import child_process from 'child_process'


export default {

  crossdocAtomView: null,
  modalPanel: null,
  subscriptions: null,

  //Atom calls this state upon initial load, use for any startup info
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
    //Register testingShell command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:testingShell': () => this.testingShell()
    }));

  },

  //Atom calls this whenever package is deactivated, such as the editor being closed
  //or refreshed
  deactivate() {
    this.modalPanel.destroy();
    this.subscriptions.dispose();
    this.crossdocAtomView.destroy();
  },

  //Allows for saving of package states between uses.
  serialize() {
    return {
      crossdocAtomViewState: this.crossdocAtomView.serialize()
    };
  },

  //how function works, at cursor, deletes the current line, or selected lines
  //moves to the beginning of linethen generates and inserts our anchor into the line.
  insertAnchor() {
    let anchorToInsert = "Cdoc #000001abc:"
    let editor

    //handling cdoc shell commands through Node.js
    const execFile = require('child_process').execFile;
    const child = execFile('cdoc', ['ga'], (error, stdout, stderr) =>
            {
                if (error)
                {
                    console.error('stderr', stderr);
                    throw error;
                }
                anchorToInsert = stdout
                console.log('stdout', stdout);
            });


    if (editor = atom.workspace.getActiveTextEditor())
    {
      let selection = editor.getSelectedText()
      editor.deleteLine()
      editor.moveToBeginningOfScreenLine()

      editor.insertText(anchorToInsert)
      editor.toggleLineCommentsInSelection()
    }



  },


  //how function works;
  deleteAnchor() {
    let editor
    let anchorToStore
    if (editor = atom.workspace.getActiveTextEditor())
    {
      editor.moveToBeginningOfScreenLine()  //move to beginning of where we are
      editor.selectToFirstCharacterOfLine() //move to first character seen (should be cdoc anchor)
      editor.selectToEndOfWord() //select all of the anchor
      anchorToStore = editor.getSelectedText() //grab that anchor
      editor.toggleLineCommentsInSelection() //toggle the comment off
      editor.deleteLine() //delete
    }

    //handling cdoc shell commands
    const execFile = require('child_process').execFile;
    const child2 = execFile('cdoc', ['da'], (error, stdout, stderr) =>
            {
                if (error)
                {
                    console.error('stderr', stderr);
                    throw error;
                }
                anchorToInsert = stdout
                console.log('stdout', stdout);
            });

  },

  testingShell()
  {

    let anchorToInsert = "TESTING ANC"
    const execFile = require('child_process').execFile;
    const child = execFile('cdoc', ['ga'], (error, stdout, stderr) =>
            {
                if (error)
                {
                    console.error('stderr', stderr);
                    throw error;
                }
                anchorToInsert = stdout
                console.log('stdout', stdout);
            });
    let editor
    if (editor = atom.workspace.getActiveTextEditor())
    {
      editor.insertText(anchorToInsert)
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
