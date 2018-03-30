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
    //Register initCrossdoc command
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'crossdoc-atom:initCrossdoc': () => this.initCrossdoc()
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

                  //finding column indent
                  let cursor
                  let screenColumn
                  cursor = editor.getLastCursor()
                  screenColumn = cursor.getScreenColumn()

                  //inserting anchor comment
                  editor.toggleLineCommentsInSelection()
                  editor.insertText(temp)
                  editor.backspace()

                  //adding in the user comment space below cdoc anchor
                  let i
                  for(i = 0; i < 2; i++) //loop so we can modify easier, if move wanted
                  {
                    editor.insertNewline()
                    editor.toggleLineCommentsInSelection()
                  }


                }

            });

  },


  //how function works;
  deleteComment() {

    let editor
    let anchorToStore
    if (editor = atom.workspace.getActiveTextEditor())
    {

      //initialization
      let anchorTag = "<&>"

      editor.moveToFirstCharacterOfLine()
      editor.selectToEndOfWord()
      let commentMarker = editor.getSelectedText()
      let flag = 0 //escape flag
      let parsedText
      while(flag == 0)
      {
        editor.moveToFirstCharacterOfLine()
        editor.moveToEndOfWord()
        editor.moveRight(1) //move towards next word
        editor.selectToEndOfWord()
        parsedText = editor.getSelectedText()

        if(parsedText == anchorTag) //if we found our nearest anchor
        {
          flag = 1
          editor.moveRight(2) //deselect and move close to the anchortag
          editor.selectToEndOfWord()
          anchorToStore = editor.getSelectedText()
        }
        else //if not keep looking upwards
        {
          editor.moveUp(1)
        }

      }//ends while loop

      //deletion process (once we found our anchor tag we must be at top of comment)
      flag = 0
      while(flag == 0)
      {
        editor.moveToFirstCharacterOfLine()
        editor.selectToEndOfWord()
        parsedText = editor.getSelectedText()

        if(parsedText == commentMarker)//we are in a comment still
        {
          editor.deleteLine()
        }
        else //no longer in comments
        {
          flag = 1 //allow escape
        }
      }

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

    let editor
    let anchorToStore
    let commentToStore = '' //give starting value or undefined will be in text

    if (editor = atom.workspace.getActiveTextEditor())
    {
      //initialization
      let anchorTag = "<&>"

      editor.moveToFirstCharacterOfLine()
      editor.selectToEndOfWord()
      let commentMarker = editor.getSelectedText()
      let flag = 0 //escape flag
      let parsedText
      while(flag == 0)
      {
        editor.moveToFirstCharacterOfLine()
        editor.moveToEndOfWord()
        editor.moveRight(1) //move towards next word
        editor.selectToEndOfWord()
        parsedText = editor.getSelectedText()

        if(parsedText == anchorTag) //if we found our nearest anchor
        {
          flag = 1
          editor.moveRight(1) //deselect and move close to the anchortag
          editor.selectToEndOfWord()
          anchorToStore = editor.getSelectedText()
        }
        else //if not keep looking upwards
        {
          editor.moveUp(1)
        }

      }//ends while loop

      //collection of updatable comments process (once we found our anchor tag we must be at top of comment)
      editor.moveDown(1) //move past the anchor line
      flag = 0
      while(flag == 0)
      {
        editor.moveToFirstCharacterOfLine()
        editor.selectToEndOfWord()
        parsedText = editor.getSelectedText()

        if(parsedText == commentMarker)//we are in a comment still
        {
          editor.moveRight(1)
          editor.selectToEndOfLine()
          commentToStore += editor.getSelectedText() //store comment text
        }
        else //no longer in comments
        {
          flag = 1 //allow escape
        }
        editor.moveDown(1) //look at next line
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
