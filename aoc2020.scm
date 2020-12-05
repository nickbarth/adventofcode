;; 1a -- Day 1: Report Repair

(define (check n1 n2)
  (when (= 2020 (+ n1 n2)) (* n1 n2)))

(define (solve lst)
  (cond ((null? lst) '())
        (else (report (cdr lst)) (map (lambda (x) (check (car lst) x)) (cdr lst)))))
(filter number? (solve datas))

;; 1b

(define (check n1 n2 n3)
  (when (= 2020 (+ n1 n2 n3)) (* n1 n2 n3)))

(filter number? 
  (map (lambda (lst) (apply check lst)) (comb 3 datas)))

;; 2a -- Day 2: Password Philosophy

(define (check low high ch str)
  (let ((count
    (let while ((i 0) (n 0)) 
      (if (< i (string-length str)) 
              (while (add1 i) (if (equal? (string-ref str i) ch) (add1 n) n)) n))))
  (and (>= count low) (<= count high))))

(foldl (lambda (r n) (if n (add1 r) r)) 0
  (map (lambda (lst) (apply check lst)) datas))

;; 2b

(define (xor a b)
  (not (equal? a b)))

(define (check low high ch str)
  (xor (equal? (string-ref str (sub1 low)) ch)
      (equal? (string-ref str (sub1 high)) ch)))

(foldl (lambda (r n) (if n (add1 r) r)) 0 
  (map (lambda (lst) (apply check lst)) datas))

;; 3a -- Day 3: Toboggan Trajectory

(define (solve lst)
  (let while ((y 1) (x 3) (count 0))
    (if (< y (length lst))
      (while (add1 y) (+ 3 x) (if (= 1 (list-ref (apply circular-list (list-ref lst y)) x)) (add1 count) count))
      count)))

;; 3b

(define (solve lst yinc xinc)
  (let while ((y yinc) (x xinc) (count 0))
    (if (< y (length lst))
      (while (+ y yinc) (+ x xinc) (if (= 1 (list-ref (apply circular-list (list-ref lst y)) x)) (add1 count) count))
      count)))

(foldl (lambda (n r) (* n r)) 1
  (list (solve datas 1 1)
  (solve datas 1 3)
  (solve datas 1 5)
  (solve datas 1 7)
  (solve datas 2 1)))

;; 4a -- Day 4: Passport Processing

(define (check x lst)
  (cond ((member x lst) #t)
        (else #f)))
(check 'ecl '( ecl gry pid 860033327 eyr 2020 hcl \#fffffd byr 1937 iyr 2017 cid 147 hgt 183cm ))

(define (valid lst checks)
  (cond ((null? checks) 1)
        ((check (car checks) lst) (valid lst (cdr checks)))
        (else 0)))
(valid '(ecl gry pid 860033327 eyr 2020 hcl \#fffffd byr 1937 iyr 2017 cid 147 hgt 183cm) '(byr iyr eyr hgt hcl ecl pid))

(define checks '(byr iyr eyr hgt hcl ecl pid))
(foldl + 0 (map (lambda (x) (valid x checks)) datas))
