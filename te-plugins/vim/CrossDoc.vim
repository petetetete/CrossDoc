

function Init()
        :exe system("cross-doc init")
endfunction

"<&>
"This fucntion insert the cross-doc Creaete comment line to the code"
"Todo: Need to work on the inerting it into cross docs"
function Insert()
        normal O
        let curline = getline('.')
        call inputsave()
        let name = input('Enter Comment: ')
        exe system("cdoc cc -t " . name)
        call setline('.', curline . ' '. Anchor() . name)
endfunction <&> 7879963^@hello

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
        :s/<&>/
        :exe ":normal dd"
        :exe ":normal O"
endfunction

function Update(ucomment)
        :exe system("cdoc uc" . a:ucomment)
endfunction

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

map <F6> :call Insert()
