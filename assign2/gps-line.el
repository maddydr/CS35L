(defun gps-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos))
        (totlines (how-many "\n" (point-min))))
    (if (= start 1)
	(message "Line %d/%d" n totlines)
      (save-excursion
	(save-restriction
	  (widen)
	  (message "line %d/%d (narrowed line %d)"
		   (+ n (line-number-at-pos start) -1) totlines n))))))
