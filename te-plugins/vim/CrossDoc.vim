
function Init()
  try
  exe system("mkdir " . expand('%:r') . '_CDoc_Store')
  exe system("cross-doc init -s " .  join(split(expand('%:p:h'), '\'), "\\\\") . '\' . expand('%:r') . '_CDoc_Store' )
  catch
    echo "There already a crossdoc store in dictionary"
  endtry
endfunction
" <&> d10b42e201b8643a
"<&>
"This fucntion insert the cross-doc Creaete comment line to the code"
"Todo: Need to work on the inerting it into cross docs"
function Insert()
  let anc = system("cdoc ga")
        normal O
        let curline = getline('.')
        call inputsave()
        let name = input('Enter Comment: ')
        exe system("cdoc cc -t " . name)
        call setline('.', curline  .  ' '. anc . ' ' . name)
        exe ":call Comment()"
        exe ":normal =="
endfunction

"Generate an Anchor from the pip command line tool.
"Then return the cross-doc Anchor"

function Anchor()
        let anc= system("cross-doc generate-anchor")
        return anc
endfunction
"This function looks for generate-anchor in the current curser line
"Then delete the Whole line
"Laslty add a blank line to keep the spacing
function Delete()
  let cls = split(getline('.'))
  let lislen = len(cls)
  let i = 0
  let curlispos = 0
  while i < lislen 
    if cls[i] == "<&>"
      let curlispos = i+1
      echo "Deleted CrossDoc Comment"
    endif
    let i += 1
  endwhile
  let anclist = cls[curlispos]
  try
    system("cdoc dc -anchor " . anclist)
    exe ":normal dd"
  catch
    echo "Not a CrossDoc Comment"
  endtry
       " :s/<&>/
endfunction
" <&> be6102de405995fc
"Comment() will search for the file type and add the correct comment Symbol
function! Comment()
  let ext = tolower(expand('%:e'))
  if ext == 'php' || ext == 'rb' || ext == 'sh' || ext == 'py'
    silent s/^/\#/
  elseif ext == 'js'
    silent s:^:\/\/:g
  elseif ext == 'vim'
    silent s:^:\":g
  endif
endfunction

"Uncomment() search for the file type and remove the correct comment Symbol
function! Uncomment()
  let ext = tolower(expand('%:e'))
  if ext == 'php' || ext == 'rb' || ext == 'sh' || ext == 'py'
    silent s/^\#//
  elseif ext == 'js'
    silent s:^\/\/::g
  elseif ext == 'vim'
    silent s:^\"::g
  endif
endfunction

"Hotkey for Cross-Doc functionality
map <F6> :call Insert()
map <F7> :call Delete()
map <F8> :call Update()
map <F5> :call Init()
