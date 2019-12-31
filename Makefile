#!/bin/bash
build:
	antlr4 -Dlanguage=Python3 rGex.g4
clean:
	rm rGexL* rGexP* rGex.i* rGex.t*
