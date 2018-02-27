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
    //Register createComment command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:createComment': () => this.createComment()
    }));
    //Register deleteComment command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:deleteComment': () => this.deleteComment()
    }));
    //Register updateComment command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:updateComment': () => this.updateComment()
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

  createComment() {

    this.initCrossdoc() //runs cdoc init in shell to ensure we have a config

    let editor

    //handling cdoc shell commands through Node.js
    //must execute any commands that need shell input within the execFile {}
    const execFile = require('child_process').execFile;
    const child = execFile('cdoc', ['cc', '-text', 'testTextinAtomCommand'], (error, stdout, stderr) =>
            {
                if (error)
                {
                    console.error('stderr', stderr);
                    throw error;
                }


                let temp = stdout.substr(29)
                console.log('stdout', stdout);


                if (editor = atom.workspace.getActiveTextEditor())
                {

                  //let selection = editor.getSelectedText()
                  editor.deleteLine()
                  editor.moveToBeginningOfScreenLine()

                  editor.toggleLineCommentsInSelection()
                  editor.insertText(temp)

                  //adding in the user comment space below cdoc anchor
                  editor.insertNewline()
                  editor.moveUp(1)
                  let i
                  for(i = 0; i < 2; i++) //loop so we can modify easier, if move wanted
                  {
                    editor.toggleLineCommentsInSelection()
                    editor.insertNewline()
                  }

                }

            });

  },


  //how function works;
  deleteComment() {

    this.initCrossdoc()

    let editor
    let anchorToStore
    if (editor = atom.workspace.getActiveTextEditor())
    {
      editor.moveToBeginningOfScreenLine()  //move to beginning of line (selection and or cursor)
      editor.moveToFirstCharacterOfLine() //move to first character seen (should be beginning of comment characters)
      editor.moveToEndOfWord() //moving past the comment lines
      editor.moveRight(1) //move toward next word
      editor.moveToEndOfWord() //move past cdoc anchor icon
      editor.moveRight(1) //move toward next word (should be cdoc anchor number)
      editor.selectToEndOfWord() //select to the end of our anchor number
      anchorToStore = editor.getSelectedText() //grab that anchorNumber and store it
      editor.toggleLineCommentsInSelection() //toggle the comment off
      editor.deleteLine() //delete anchor line
      editor.deleteLine()
      editor.deleteLine()
    }

    console.log('anchorToStore = ', anchorToStore)

    //handling cdoc shell commands
    const execFile = require('child_process').execFile;
    const child2 = execFile('cdoc', ['dc','-anchor', anchorToStore], (error, stdout, stderr) =>
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

  updateComment()
  {
    this.initCrossdoc()

    let editor
    let anchorToStore
    let commentToStore = '' //give starting value or undefined will be in text
    if (editor = atom.workspace.getActiveTextEditor())
    {
      editor.moveToBeginningOfScreenLine()  //move to beginning of line (selection and or cursor)
      editor.moveToFirstCharacterOfLine() //move to first character seen (should be beginning of comment characters)
      editor.moveToEndOfWord() //moving past the comment lines
      editor.moveRight(1) //move toward next word
      editor.moveToEndOfWord() //move past cdoc anchor icon
      editor.moveRight(1) //move toward next word (should be cdoc anchor number)
      editor.selectToEndOfWord() //select to the end of our anchor number
      anchorToStore = editor.getSelectedText() //grab that anchorNumber and store it


      //now to find the comments
      let i
      for(i = 0; i < 2; i++) //loop the number of comment lines to grab, find way to calc and this will work for multiline
      {
        //editor.moveDown(1)
        editor.moveToEndOfWord()
        editor.moveRight(1)
        editor.selectToEndOfLine()
        commentToStore += editor.getSelectedText() //store it
      }

    }

    console.log('anchorToStore = ', anchorToStore)
    console.log('commentToStore = ', commentToStore)

    //handling cdoc shell commands
    const execFile = require('child_process').execFile;
    const child2 = execFile('cdoc', ['uc','-anchor', anchorToStore, '-text', commentToStore], (error, stdout, stderr) =>
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

  //to be ran with all crossDoc functions, ensures we are in a valid Cdoc repo
  initCrossdoc() {
    const execFile = require('child_process').execFile;
    const child = execFile('cdoc', ['init'], (error, stdout, stderr) =>
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

  toggle() {
    console.log('CrossDoc was toggled!');
    return (
        this.modalPanel.isVisible() ?
        this.modalPanel.hide() :
        this.modalPanel.show()
        );
    }
};
