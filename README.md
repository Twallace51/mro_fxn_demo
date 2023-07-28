# mro_fxn_demo
visual demo of c3-linearization in mro()

The first time I got an "inconsistent MRO error",  I got frustrated and didn't know what to do,
so I read whatever I could find in docs.python.org and Github.
Now also confused,  I realized that I understand quicker just reading the code and seeing what it does.

The scripts emulating mro() that I found on GitHub were varied and helpful,  but not what I needed,
since none of them could show what happens when there is a "inconsistent MRO error".

Best emulation:
https://github.com/twisted/pydoctor/blob/965ed955efde6178cb68f0882a02c34a90204447/pydoctor/mro.py#L126

The above failure is due to the fact that Python's mro() function is a compiled core function and cannot be seen nor subclassed.
Trying to run any of the above emulations on a set of classes with inconsistent errors,
are immediately aborted by the ~real~ mro().

So I wrote the following for me and whoever else might have similar interests.

Bonus:  I have similar comments about the volumes written about super(), until I realized
that `super(obj)` used in a class just means that super will use the class.\__mro\__, like Bash uses $PATH,
to simply find and return the first instance of the obj it finds in the MRO.
Easy peazy.

This script can be run as-is as a demo with various examples,  it is not an emulation.

Based on:
   Implements Python Method Resolution Order(MRO)
   https://gist.github.com/bellbind/1614683
   by https://gist.github.com/bellbind
   
twallace51@gmail.com
