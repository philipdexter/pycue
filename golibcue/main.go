package main

import (
	"C"
	"fmt"
	"sync"

	"cuelang.org/go/cue"
	"cuelang.org/go/cue/format"
)

var r cue.Runtime

//export Print
func Print(id int) {
	i := lookup(id)
	bytes, err := format.Node(i.Syntax())
	if err != nil {
		return
	}
	fmt.Println(string(bytes))
}

// TODO return error strings
// and "return" using out parameters

//export Fields
func Fields(id int) int {
	i := lookup(id)
	fiter, err := i.Fields()
	if err != nil {
		return -1
	}
	return insertIter(fiter)
}

//export Elems
func Elems(id int) int {
	i := lookup(id)
	liter, err := i.List()
	if err != nil {
		return -1
	}
	return insertIter(&liter)
}

//export IsStruct
func IsStruct(id int) bool {
	return lookup(id).Kind() == cue.StructKind
}

//export IsList
func IsList(id int) bool {
	return lookup(id).Kind() == cue.ListKind
}

//export Next
func Next(id int) bool {
	i := lookupIter(id)
	return i.Next()
}

//export Label
func Label(id int) *C.char {
	i := lookupIter(id)
	return C.CString(i.Label())
}

//export Value
func Value(id int) int {
	i := lookupIter(id)
	return insert(i.Value())
}

//export Test
func Test(i *int) {
	*i = 2
}

//export ToString
func ToString(id int) *C.char {
	i := lookup(id)
	bytes, err := format.Node(i.Syntax())
	if err != nil {
		return C.CString("")
	}
	return C.CString(string(bytes))
}

//export Compile
func Compile(str string) int {
	i, err := r.Compile("", str)
	if err != nil {
		return -1
	}
	return insert(i.Value())
}

//export Unifies
func Unifies(id1, id2 int) bool {
	v1 := lookup(id1)
	v2 := lookup(id2)
	return v1.Unify(v2).Kind() != cue.BottomKind
}

func main() {
}

var mu sync.Mutex
var index int
var values = make(map[int]cue.Value)

func lookup(i int) cue.Value {
	mu.Lock()
	defer mu.Unlock()
	return values[i]
}

func insert(v cue.Value) int {
	mu.Lock()
	defer mu.Unlock()
	index++
	values[index] = v
	return index
}

var muIter sync.Mutex
var indexIter int
var iters = make(map[int]*cue.Iterator)

func lookupIter(i int) *cue.Iterator {
	muIter.Lock()
	defer muIter.Unlock()
	return iters[i]
}

func insertIter(v *cue.Iterator) int {
	muIter.Lock()
	defer muIter.Unlock()
	indexIter++
	iters[indexIter] = v
	return indexIter
}