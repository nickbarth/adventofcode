;; Advent of Code 2020
;; https://adventofcode.com/2020

(import srfi-1) ;; strings

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

(import regex)

(define (check-keys x lst)
  (cond ((member x lst) #t)
        (else #f)))

(define (has-keys lst keys)
  (cond ((null? keys) #t)
        ((check-keys (car keys) lst) (valid lst (cdr keys)))
        (else #f)))

(define keys '(byr iyr eyr hgt hcl ecl pid))
(length (filter (lambda (x) (valid x keys)) datas))

;; 4b

(define (in-range low high n)
  (cond ((not (<= low n high))  #f)
        (else #t)))

(define (byr n)
  (in-range 1920 2002 (string->number n)))

(define (iyr n)
  (in-range 2010 2020 (string->number n)))

(define (eyr n)
  (in-range 2020 2030 (string->number n)))

(define (hgt s)
  (cond ((string-match "[0-9]*cm" s)
            (in-range 150 193 (string->number (cadr (string-match "([0-9]*)cm" s)))))
        ((string-match "[0-9]*in" s)
            (in-range  59  76 (string->number (cadr (string-match "([0-9]*)in" s)))))
        (else #f)))

(define (hcl s)
  (cond ((string-match "#[0-9a-f]{6}" s) #t)
        (else #f)))

(define (ecl s)
  (cond ((string-match "(amb|blu|brn|gry|grn|hzl|oth)" s) #t)
        (else #f)))

(define (pid s)
  (cond ((string-match "[0-9]{9}" s) #t)
        (else #f)))

(define (cid s) #t)

(define (pairs lst)
  (cond ((null? lst) '())
        (else (cons (list (car lst) (cadr lst)) (pairs (cddr lst))))))

(define (check-values lst)
  (foldl (lambda (n res) (and n res)) #t (map eval (pairs lst))))

(length (filter (lambda (x) (check-values x)) 
  (filter (lambda (x) (has-keys x keys)) datas)))

;; 5a -- Binary Boarding

(import srfi-95) ;; sort 

(define (first-half lst)
  (take lst (quotient (length lst) 2)))
(define (second-half lst)
  (drop lst (quotient (length lst) 2)))

(define (F lst) (second-half lst))
(define (B lst) (first-half lst))
(define (L lst) (second-half lst)
(define (R lst) (first-half lst))

(define (range n)
  (cond ((< n 0) '())
        (else (cons n (range (sub1 n))))))

(define (seat lst)
  (let ((column (car (foldl (lambda (res n) ((eval n) res)) (range 127) (take lst 7))))
        (row (car (foldl (lambda (res n) ((eval n) res)) (range 7) (drop lst 7)))))
    (+ (* column 8) row)))

(car (sort (map seat datas) >))

;; 5b

(let ((data (map seat datas)))
  (filter (lambda (x) (not (member x data))) (range 850)))
  
;; 6a -- Day 6: Custom Customs

(apply + (map (lambda (data)
  (length (delete-duplicates (flatten data)))) datas))

;; 6b

(define (count-symbols lst s)
  (length (filter (lambda (x) (eq? s x)) lst)))

(define (count-unanimous lst)
  (length (filter (lambda (x) (= (count-symbols (flatten lst) x) (length lst))) (delete-duplicates (flatten lst)))))

(apply + (map (lambda (data)
  (count-unanimous data)) datas))
  
;; 7a -- Day 7: Handy Haversacks

(define (pairs lst)
  (cond ((null? lst) '())
        (else (cons (list (car lst) (cadr lst)) (pairs (cddr lst))))))

(define (open-bag sym)
   (cdr (car (filter (lambda (x) (equal? sym (car x))) datas))))

(define (has-gold sym)
  (let ((lst (open-bag sym)))
    (cond ((null? lst) #f)
          ((member 'shiny_gold lst) #t)
          (else (not (null? (filter (lambda (x) (has-gold  (cadr x))) (pairs lst))))))))

(length (filter has-gold (map car datas)))

