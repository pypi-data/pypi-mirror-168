#!/bin/sh

if [ -z $1 ] || [ -z $2 ]; then
    echo "Usage: ./filter_prefix.sh WORDLIST OUT_DIR"
    exit 0
else
    grep -P "^a" $1 > "$2/words_a.txt"
    grep -P "^b" $1 > "$2/words_b.txt"
    grep -P "^c" $1 > "$2/words_c.txt"
    grep -P "^d" $1 > "$2/words_d.txt"
    grep -P "^e" $1 > "$2/words_e.txt"
    grep -P "^f" $1 > "$2/words_f.txt"
    grep -P "^g" $1 > "$2/words_g.txt"
    grep -P "^h" $1 > "$2/words_h.txt"
    grep -P "^i" $1 > "$2/words_i.txt"
    grep -P "^j" $1 > "$2/words_j.txt"
    grep -P "^k" $1 > "$2/words_k.txt"
    grep -P "^l" $1 > "$2/words_l.txt"
    grep -P "^m" $1 > "$2/words_m.txt"
    grep -P "^n" $1 > "$2/words_n.txt"
    grep -P "^o" $1 > "$2/words_o.txt"
    grep -P "^p" $1 > "$2/words_p.txt"
    grep -P "^q" $1 > "$2/words_q.txt"
    grep -P "^r" $1 > "$2/words_r.txt"
    grep -P "^s" $1 > "$2/words_s.txt"
    grep -P "^t" $1 > "$2/words_t.txt"
    grep -P "^u" $1 > "$2/words_u.txt"
    grep -P "^v" $1 > "$2/words_v.txt"
    grep -P "^w" $1 > "$2/words_w.txt"
    grep -P "^x" $1 > "$2/words_x.txt"
    grep -P "^y" $1 > "$2/words_y.txt"
    grep -P "^z" $1 > "$2/words_z.txt"
    touch "$2/words__.txt"
    exit 0
fi
