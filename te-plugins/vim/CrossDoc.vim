function Init()
  try
  exe system("mkdir " . expand('%:r') . '_CDoc_Store')
  exe system("cross-doc init -s " .  join(split(expand('%:p:h'), '\'), "\\\\") . '\' . expand('%:r') . '_CDoc_Store' )
  catch
    echo "There already a crossdoc store in dictionary"
  endtry
endfunction

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

function Update()
        ":exe system("cdoc uc" . a:ucomment)
  let clu = split(getline('.'))
  let listlen = len(clu)
  let n = 0
  let i = 0
  let h = 0
  let h = ""
  let j = line('$')
  "let emline = exe :/^$"
  exe ":normal gg"
  while i < j
    try
    while n <= listlen
      if clu[n] == "<&>"
        echo clu[n + 1]
        while strlen(getline('.')) != 0
          exe ":call Uncomment()"
          let p ='' .  getline('.')
          exe ":call Comment()"
          let h = h . p
          exe ":normal j"
          echo getline('.')
        endwhile  
        echo h
        exe system("cdoc uc -anchor ". clu[n + 1] . " -text " . h )
      endif
      let h = ""
      let p = ""
      let n += 1
    endwhile
  catch
  endtry
    let clu = split(getline('.'))
    let n = 0
    exe ":normal j"
    let i += 1
  endwhile
endfunction
" <&> f0f999d4e4af5a1f
" "heklsjfdlks lksdjfl \n
" ksjdflk slkfdj \n
" sjdflk jsdklfjklsd Brian "

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
" <&> 2144955e3ee89ab6
" "ksld fkls skljf \n
" fskdljf lsj kl \n
" ksjdflksj Saganey"

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

function Test()
  let i = 0 
  let cls = split(getline('.'))
  if cls[i] == Comment()
    exe ":normal dd"
  endif
endfunction

"Hotkey for Cross-Doc functionality
map <F6> :call Insert()
map <F7> :call Delete()
map <F8> :call Update()
map <F5> :call Init()
