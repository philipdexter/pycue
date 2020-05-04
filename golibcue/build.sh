#!/usr/bin/env sh

go build -o golibcue.so -buildmode=c-shared main.go && cp golibcue.so ../cue/_golibcue.so
