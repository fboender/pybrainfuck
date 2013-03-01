PyBrainfuck
===========

Introduction
------------

PyBrainfuck is a speed-optimized Brainfuck interpreter written in Python. 

Brainfuck is an esoteric (joke) programming language which is Turing-complete
(given enough memory) with only 8 op-codes (instructions). It was designed to
allow for the smallest possible compiler.

Some other Python interpreters already exists for Brainfuck, but they are
either obfuscated or awfully slow. PyBrainfuck has been optimized for speed by
doing various preprocessing on the code such as pre-caching loop instructions,
removing non-instructions, etc. PyBrainfuck also has configurable memory size,
infinite loop protection and a somewhat spartan debugger.

PyBrainfuck can be used both as a stand-alone Brainfuck interpreter or as a 
python library. It can read from standard input or from a string (in library
mode) and write to standard out or to a string buffer (in library mode).

Features
--------

*    Speed optimized
*    User-definable memory limit
*    Infinite loop protection
*    Debugger
*    Stand-alone use or use as library
*    Brainfuck programs can read from STDIN or string buffer
*    Brainfuck programs can write to STDOUT or string buffer

Installation
------------

Either use it directly from extracted archive or copy the brainfuck directory
to a directory in your Python interpreter's path (e.g.
/usr/lib/python2.4/site-packages/).


Usage
-----

Standalone mode: 

    Usage: ./pybrainfuck [option] PROGRAM.bf
    
    Options:
      -h, --help            show this help message and exit
      -m BYTES, --memory=BYTES
                            Number of bytes of memory.
      -i NUMBER, --instructions=NUMBER
                            Number of max instructions to run.
      -d, --debug           Show debugging information.
    
    Example:

        $ ./pybrainfuck tests/helloworld.bf 
        Hello World!

        $ ./pybrainfuck tests/divide.bf 
        62<ENTER>
        3

        $ echo "ROT13 me please." | ./pybrainfuck tests/rot13.bf
        EBG13 zr cyrnfr.

Library mode:

    Hello World:
        #!/usr/bin/python

        import brainfuck

        code = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
        bf = brainfuck.Brainfuck(code)
        out = bf.run() 
        print out # Hello, World!


    Divide:
        #!/usr/bin/python

        import brainfuck
        
        code = ",>,>++++++[-<--------<-------->>]<<[>[->+>+<<]>[-<<-[>]>>>[<[>>>-<<<[-]]>>]<<]>>>+<<[-<<+>>]<<<]>[-]>>>>[-<<<<<+>>>>>]<<<<++++++[-<++++++++>]<."
        bf = brainfuck.Brainfuck(code, '62')
        out = bf.run()
        print out # 3


Copyright
---------

pyBrainfuck is Copyright by Ferry Boender, 2008-2013 - Released under the MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
