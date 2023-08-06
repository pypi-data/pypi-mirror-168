#!/bin/sh

if [ -z $1 ] || [ -z $2 ]; then
    echo "Usage: ./filter_prefix.sh WORDLIST PREFIX_LENGTH"
    exit 0
else
    cat "$1" | pcregrep -o1 "^([a-zA-Z]{$2})" | uniq
    exit 0
fi
