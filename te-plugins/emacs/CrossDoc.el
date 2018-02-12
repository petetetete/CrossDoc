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
(provide 'cdoc)


