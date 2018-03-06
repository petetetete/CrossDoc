
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
  let i = 0
        normal O
        let curline = getline('.')
        call inputsave()
        let name = input('Enter Comment: ')
        let g = system('cdoc cc -t ' . name)
        let commax = split(g)
        call setline('.', curline  .  ' '. commax[0] . ' ' . commax[1])
        exe ":call Comment()"
        exe ":normal =="
  exe ":normal o"
  let comlen = len(g)
  let commaxx = split(name)
  while i < comlen
    try
      exe ":normal A".' ' . commaxx[i]
      if commaxx[i] == '\n'
        exe ":normal o"
      endif 
    catch 
      echo ""
    endtry  
    let i += 1
  endwhile
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
      exe ":normal dd"
      let u = 0
      try
        while cls[u] == Comment()
          exe ":normal dd"
          let u += 1
        endwhile
        exe ":normal dd"
      catch
      endtry
    endif
    let i += 1
  endwhile
  let anclist = cls[curlispos]
  try
    exe system("cdoc dc -anchor " . anclist)
  catch
  endtry
endfunction

function Update(ucomment)
  while i < lislen 
      if cls[i] == "<&>"
        let curlispos = i+1
        echo "Update CrossDoc Comment"
        exe ":normal dd"
        let u = 0
        try
          while cls[u] == Comment()
            exe ":normal dd"
            let u += 1
          endwhile
          exe ":normal dd"
        catch
        endtry
      endif
      let i += 1
    endwhile
endfunction

function Update(ucomment)
        :exe system("cdoc uc" . a:ucomment)
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
