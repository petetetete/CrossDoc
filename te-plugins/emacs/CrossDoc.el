(defun update-comment()
  (interactive)

  ; gets contents from a file path
  (with-temp-buffer
    (insert-file-contents filePath)
    (buffer-string)
    )
  ; gets output of update comment
  (setq output (shell-command-to-string(concat "cdoc uc -a\"[Anchor]|\" -t\"[Insert comment\"")))

  ; use save-after-hook to save after a buffer has been saved and visited

  )

(defun delete-comment ()
  (interactive)

  ; Get the current line position of cursor 
  (setq curr-line (split-string (thing-at-point 'line )))

  ; Check and see if we are in a CrossDoc comment
  (if (string= "<&>" (cadr curr-line))
    (progn
      (setq output (shell-command-to-string (concat "cdoc dc -a " (cadr (cdr curr-line)))))
      (if (not (string= "fatal" (substring output 0 5)))
        (kill-whole-line) ; If not fatal, delete line in text file
        (message output) ; else if fatal show output
        )
      )

    (message "fatal: not highlighting a CrossDoc comment")
    )
  )

(defun insert-comment ()
  (interactive)

  ; Move to beginning of line and tab to match
  (move-beginning-of-line nil)
  (indent-according-to-mode)

  ; Get CrossDoc command line output from create-comment
  (setq output (substring (shell-command-to-string "cdoc cc -t \"[COMMENT HERE]\"") 0 -1))
  (if (not (string= "fatal" (substring output 0 5)))

    ; If not fatal: continue creating comment
    (progn

      ; Insert CrossDoc comment (and comment it out)
      (insert output)
      (comment-region (line-beginning-position) (line-end-position))
      
      ; Move the cursor back to the line it started, and fix the tabbing
      (insert "\n")
      (indent-according-to-mode))

    ; Else if fatal: forward the fatal message to the console
    (message output)
    
    )
  )

; Set command hot keys and provide package
(global-set-key [f6] 'insert-comment)
(global-set-key [f7] 'delete-comment)
(global-set-key [f8] 'update-comment)
(provide 'cdoc)


