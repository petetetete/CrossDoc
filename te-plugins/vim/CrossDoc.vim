scriptencoding utf-8

function! s:cdoc_test()
  let output = system("cdoc cc -t \"[COMMENT HERE]\"")
  echo output
endfunction

command! CrossDocTest call <SID>cdoc_test()
