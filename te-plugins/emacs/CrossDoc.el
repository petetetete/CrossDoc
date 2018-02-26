; Debug flag
; (setq debug-on-error t)

(defun update-comments()
  (interactive)

  ; Save starting point and reset back to the beginning
  (setq start-point (point))
  (goto-char 0)

  ; Go to each line with an anchor hook
  (while (search-forward "<&>" nil t)
    (progn

      ; Save the anchor line
      (setq split-line (split-string (thing-at-point 'line) " " t))

      ; Move forward off the anchor line
      (forward-line)
      (end-of-line)

      ; Create empty list to store lines in 
      (setq text-list '())

      ; While we are still in a comment
      (while (nth 4 (syntax-ppss))
        (progn

          ; Append to the text-list as we go along
          (add-to-list 'text-list

            ; TODO: Currently, this just splits on spaces but it really should
            ; use a better method because not all comments are followed by spaces
            (mapconcat 'identity
              (nthcdr 1 (split-string (substring (thing-at-point 'line t) 0 -1) " " t))
              " ") t)

          ; Move forward and to the end of the line
          (forward-line)
          (end-of-line)))

      ; Save the final text and send off the CrossDoc command
      (setq final-text (mapconcat 'identity text-list "\n"))
      (setq output (substring (shell-command-to-string (concat "cdoc uc -a " (nth 2 split-line) " -t \"" final-text "\"")) 0 -1))

      ; Catch errors
      (if (string= "fatal" (substring output 0 5))
        (message output)))) ; Show output on fatal

  ; Move the cursor back to where it started
  (goto-char start-point))


(defun delete-comment ()
  (interactive)

  ; Save starting point and move to the end of the line
  (setq start-point (point))
  (end-of-line)

  ; If we started in a comment
  (if (nth 4 (syntax-ppss))
    (progn

      ; If we are not already looking at a CrossDoc comment,
      ; iterate until we either find a CrossDoc comment, or the comments break
      (if (not (string-match "<&>" (thing-at-point 'line)))

        ; This is basically a do-while with the first two lines being the "do"
        (while (progn

          ; DO
          (forward-line -1)
          (end-of-line)

          ; WHILE
          (and
            (nth 4 (syntax-ppss))
            (not (string-match "<&>" (thing-at-point 'line)))))))

      ; If we ended due to finding the anchor
      (if (string-match "<&>" (thing-at-point 'line))
        (progn

          ; Get the line with the anchor in it and delete it
          (setq curr-line (split-string (thing-at-point 'line)))
          (setq output (substring (shell-command-to-string (concat "cdoc dc -a " (nth 2 curr-line))) 0 -1))

          ; Parse delete output
          (if (not (string= "fatal" (substring output 0 5)))
            ; If not fatal, clear all comment lines
            (while (progn
              (kill-whole-line)
              (end-of-line)
              (nth 4 (syntax-ppss))))

            ; Else if fatal show output
            (message output)))

        ; Else, we couldn't find the anchor
        (progn
          (goto-char start-point)
          (message "fatal: cannot find anchor"))))

    ; Else, we didn't even start in a comment
    (progn
      (goto-char start-point)
      (message "fatal: not selecting a comment"))))


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
(global-set-key [f8] 'update-comments)

; Add hooks
(add-hook 'after-save-hook 'update-comments)

(provide 'cdoc)
