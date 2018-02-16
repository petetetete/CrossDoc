
"<&>
"This fucntion insert the cross-doc Creaete comment line to the code"
"Todo: Need to work on the inerting it into cross docs"
function Insert()
	:exe ":normal O" . Anchor()
	:exe ":normal i" . system("cross-doc create-comment")
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
	:exe ":normal dd"
	:exe ":normal O"
endfunction
