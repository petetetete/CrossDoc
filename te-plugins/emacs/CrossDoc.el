; Debug flag
; (setq debug-on-error t)

(defun update-comments()
  (interactive)

  ; Get lines of the current buffer
  (setq curr-buffer-lines (split-string (buffer-string) "\n" t))

  ; For each line in buffer
  (dolist (elt curr-buffer-lines)

    ; Save split line
    (setq split-line (split-string elt " " t))

    ; If we are at a CrossDoc comment
    (if (string= "<&>" (nth 1 split-line))
      (progn
        ; Save the current lines comment text
        (setq comment-text (mapconcat 'identity (nthcdr 3 split-line) " "))

        ; Send off update-comment
        (setq output (substring (shell-command-to-string (concat "cdoc uc -a " (nth 2 split-line) " -t \"" comment-text "\"")) 0 -1))

        ; Message CrossDoc output
        (if (string= "fatal" (substring output 0 5))
          (message output) ; Show output on fatal
          ; Do nothing on else
          )))))


(defun delete-comment ()
  (interactive)

  ; Get the current line position of cursor 
  (setq curr-line (split-string (thing-at-point 'line )))

  ; Check and see if we are in a CrossDoc comment
  (if (string= "<&>" (cadr curr-line))
    (progn
      (setq output (substring (shell-command-to-string (concat "cdoc dc -a " (nth 2 curr-line))) 0 -1))
      (if (not (string= "fatal" (substring output 0 5)))
        (kill-whole-line) ; If not fatal, delete line in text file
        (message output))) ; Else if fatal show output

    (message "fatal: not highlighting a CrossDoc comment")))


(defun insert-comment ()
  (interactive)

  ; Get CrossDoc command line output from create-comment
  (setq output (substring (shell-command-to-string "cdoc cc -t \"[COMMENT HERE]\"") 0 -1))
  (if (not (string= "fatal" (substring output 0 5)))

    ; If not fatal: continue creating comment
    (progn

      ; Move to beginning of line and tab to match
      (move-beginning-of-line nil)
      (indent-according-to-mode)

      ; For each of the lines of the comment
      (let ((output-split (split-string output "\n" t)))
        (dolist (elt output-split)
          (progn

            ; Insert actual comment line (and comment)
            (insert elt)
            (comment-region (line-beginning-position) (line-end-position))

            ; Correct the pointer position
            (insert "\n")
            (indent-according-to-mode)))))

    ; Else if fatal: forward the fatal message to the console
    (message output)))


; Set command hot keys
(global-set-key [f6] 'insert-comment)
(global-set-key [f7] 'delete-comment)
(global-set-key [f8] 'update-comment)

; Add hooks
(add-hook 'after-save-hook 'update-comments)

(provide 'cdoc)
