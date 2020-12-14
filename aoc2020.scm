;; Advent of Code 2020
;; https://adventofcode.com/2020

;; imports

(import srfi-1)  ; strings
(import srfi-95) ; sort 
(import regex)   ; regex

;; utility functions

(define (perm s)
  (cond ((null? s) '())
  ((null? (cdr s)) (list s))
  (else ;; extract each item in list in turn and perm the rest
    (let splice ((l '()) (m (car s)) (r (cdr s)))
      (append
        (map (lambda (x) (cons m x)) (perm (append l r)))
        (if (null? r) '()
    (splice (cons m l) (car r) (cdr r))))))))

(define (comb m lst)
  (cond ((= m 0) '(()))
        ((null? lst) '())
        (else (append (map (lambda (y) (cons (car lst) y)) (comb (- m 1) (cdr lst)))
                      (comb m (cdr lst))))))
(define (range x)
  (let loop ((y 0))
    (if (= x y) '()
    (cons y (loop (add1 y))))))

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

;; 7b

(define (pairs lst)
  (cond ((null? lst) '())
        (else (cons (list (car lst) (cadr lst)) (pairs (cddr lst))))))

(define (range n)
  (cond ((< n 1) '())
        (else (cons n (range (sub1 n))))))

(define (open-bag sym)
   (cdr (car (filter (lambda (x) (equal? sym (car x))) datas))))

(define (expand-bag pair)
  (map (lambda (x) (cadr pair)) (range (car pair))))

(define (count-bags sum lst)
  (if (null? lst) sum
    (count-bags (+ sum (apply + (filter number? lst)))
                (flatten (map open-bag (flatten (map expand-bag (pairs lst))))))))

(count-bags 0 (open-bag 'shiny_gold))
  
;; 8a -- Day 8: Handheld Halting

(define (cycle sp a states)
  (let ((instr (list-ref datas sp)))
    (print (list sp instr a))
    (if (not (member sp states))
      (case (car instr)
        ('nop (cycle (add1 sp) a (cons sp states)))
        ('acc (cycle (add1 sp) (+ a (cadr instr)) (cons sp states)))
        ('jmp (cycle (+ sp (cadr instr)) a (cons sp states))))
      a)))
(cycle 0 0 '())
  
;; 8b
  
(define (find-indexes sym)
  (let while ((n 0) (finds '()))
    (if (< n (length mem))
      (while (add1 n) (if (eq? (car (list-ref mem n)) sym) (cons n finds) finds))
      finds)))

(define (cycle nop sp a states)
  (if (>= sp (length mem)) a
    (let ((instr (list-ref mem sp)))
      (if (not (member sp states))
        (if (= nop sp)
            (cycle nop (add1 sp) a (cons sp states))
          (case (car instr)
            ('nop (cycle nop (add1 sp) a (cons sp states)))
            ('acc (cycle nop (add1 sp) (+ a (cadr instr)) (cons sp states)))
            ('jmp (cycle nop (+ sp (cadr instr)) a (cons sp states)))))
        #f))))

(filter number?
  (map (lambda (x) (cycle x 0 0 '())) (find-indexes 'jmp)))

;; 9a -- Day 9: Encoding Error

(define (find-invalid preamble)
  (let while ((n preamble))
    (when (< n (length datas))
      (let* ((prev (take (drop datas (- n preamble)) preamble)) (combs (comb 2 prev)))
        (if (not (null? (filter (lambda (x) (= (+ (car x) (cadr x)) (list-ref datas n))) combs)))
          (while (add1 n))
          (list-ref datas n))))))
(find-invalid 25)
  
;; 9b
  
(define (sum-check lst n)
  (= (apply + lst) n))

(define (check-range lst sum)
  (if (null? lst) '()
    (if (sum-check lst sum) lst
      (check-range (cdr lst) sum))))

(define (find-sum sum)
  (let while ((n (length datas)) (lst datas))
    (if (= n 0) '()
      (cons (check-range (take lst n) sum) (while (sub1 n) (take lst n))))))

(let ((range (sort (car (cdr (filter pair? (find-sum 14144619)))) <)))
  (+ (car range) (car (reverse range))))

;; 10a -- Day 10: Adapter Array

(define (check lst)
  (let while ((n 0) (one 1) (three 1))
    (if (< n (sub1 (length lst)))
      (case (- (list-ref lst (add1 n)) (list-ref lst n))
        ((1) (while (add1 n) (add1 one) three))
        ((3) (while (add1 n) one (add1 three))))
      (list one three))))
(apply * (check (sort datas <)))
