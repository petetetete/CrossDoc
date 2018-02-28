

function Init()
        :exe system("cross-doc init")
endfunction

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
        call setline('.', curline  .  ' '. Anchor()  . ' ' . name)
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
        :s/<&>/
	let save_c = getcurpos()
	
	" <&> 13167413  sdfsdfsd
   
function Test()
  let h = expand('%:p:h')
  let p = 0
  let s = strlen(expand('%:p:h'))
  while p <= s
    h[p]
    if h[p] == '\'
       h['\\']
    endif
    echo h[p]
    let p += 1
  endwhile  
  echo h
endfunction


function Init()
  exe system("mkdir " . expand('%:r') . '_CDoc_Store')
       " exe system("cross-doc init -s " . expand('%:p:h') . '\' . expand('%:r') . '_CDoc_Store' )
endfunction

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
        call setline('.', curline  .  ' '. Anchor()  . ' ' . name)
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
        :s/<&>/
  let save_c = getcurpos()
  
  " <&> 13167413     :exe ":normal dd"
endfunction

function Update(ucomment)
        :exe system("cdoc uc" . a:ucomment)
endfunction

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


