![Rules](notascii/rules.png "Timm's rules")
 
tim.menzies@gmail.com  
Aug 9 2014


FIRST PRINCIPLES
=================

TISTF: Truth is Shorter than Fiction
-------------------------------------

If you do not understand it, you cannot code it succinctly.
So to check if you understand it, try to code it.

BeValued:
---------

The real worth of a machine is what added value it
gives back to the community. Be valued. Give of
yourself- your wisdom, your tricks, your tips,
captured in code, shared in a publicly accessible repo, 
available for
all.

No man is an _Iland_,  
intire of it selfe;   
every man is a peece of the _Continent_,   
a part of the _maine_;  
if a _Clod_ bee washed away by the _Sea,   
Europe_ is the lesse,   
as well as if a _Promontorie_ were,   
as well as if a _Mannor_ of thy _friends_ or of _thine owne_ were;   
any mans _death_ diminishes _me_,   
because I am involved in _Mankinde_;   
And therefore never send to know for whom the _bell_ tolls;   
It tolls for _thee_.  
-- John Donne, 1623

DOOR SOURCE: OpenSource, OpenDoor, SpecialSauce
---------------------------------------------------

For years and years, I made my money by what I could
give away. I made my code open source so it open
doors to people who, otherwise, might not care
to. Once inside those doors, I earned a living
configuring (adding the special sauce) those the
open tools since, for the tools I created, I was one
of the few people who really knew the little tweaks
that make all the difference.

SHOW OFF:
--------

Code should know how to show off. All files end in

    if __name__ == '__main__': doSomethingCool();

See also _YCYR_.

TTS: Teach the Source:
----------------------

Teach from the code. One lecture = what you can show
students in one hour.

YCYR: Your Code = Your Resume
------------------------------

When going for jobs, imagine sending prospective
employees your Github repo containing impressive
code. Think how much more interested that would make
them.

PYTHON RULES
============

2.7: Two point seven 
--------------------

Use Python 2.7+, not Python 3, since many useful
libraries are NOT yet ported to Python 3. 

Note: this rule will hopefully change, soon.
 
ATMC: Add the missing code.
---------------------------

All python files should start with 

    from __future__ import division 
    import sys 
    sys.dont_write_bytecode = True
    """ some copyright notice """
	
Also, as said in _SHOW OFF_, all files should end
with:

	if __name__ == '__main__': doSomethingCool();

BCD: Beware container defaults 
------------------------------

Default params to functions, methods are evaluated
at load time. Which means that N calls to a function
with an argument that defaults to, say, an empty
list will always be talking to the *same* list,
every time you call the function.

IRU: Iterators are us
---------------------

Don't understand the following? Then work it out!

    def item(items):
      if isinstance(items,(list,tuple)):
        for one in items:
          for x in item(one):
            yield x
      else:
        yield items


LRU: Lambdas are us
-------------------

Anonymous functions (lambdas) rule. Allows for simple
implementation of generics, just by passing in a lambda
body.


NO W: No Wraps
---------------

All code <= 52 characters. Not "self" but
"i". Indents using 2 spaces. Try to keep
functions, classes, under 60 lines (and much less
is much better).

STACK OVERFLOW
---------------

Any Python question you want answered has already
been asked and answered already on
stackoverflow.com. Read it!

CODING RULES
============

BBB: Burn baby burn
-------------------

_"Perfection is achieved, not when there is nothing
more to add, but when there is nothing left to take
away."_   
-- Antoine de Saint-Exupery

Once it starts works, burn some of it away.
Benchmark it against a simpler option.  Throw away
what does not improve performance. Note: often, you
can throw away a lot of superfluous stuff

CA: Constants Aren't:
----------------------

Put the code in a function where the 'constants' are
defaults to function arguments (so later, you can
call it another way).

HAIL REPO: 
----------

The code repo is your off-site backup, your undo
facility, your sharing tool. Use it. Always.  Many
times a day.

IDM: It doesn't matter.
-----------------------

Don't waste time arguing in theory about some tuning
issue. Just try it out. It probably won't matter in
practice.

JDI: Just do it.
----------------

Systems are not written; they grow. So find the
smallest next thing and just do that. Repeat.

KISS: 
-----

keep it simple stupid.

LIB: Leave it Broken:
---------------------

At the end of the day, leave behind a broken test
(this is where you can start back up, tomorrow).

NoGo: Globals are Evil:
-----------------------

N-1 globals is better than N globals.


NBO: No Buried Options
----------------------

Keep all 'The' settings. Print 'The' settings in
front of all output.

R: Refactor:
------------

To code it once, just do it.  If you code it twice,
wince.  But if you code it thrice, refactor.

RESUMABLE: 
----------

An anytime computation is stoppable and resumable.
 
For long computations, implement occasional "dump to
disk" and "restart from part-way". That way, if the
long computation crashes, you can restart from some
interim point (and not redo it all).

TAG: 'Things' Are Good
---------------------

Consider not defining a new class if a simple 'Thing'
will do (useful for named access to data only
classes).

TDD: Test Driven Development:
-----------------------------

Write a test.
Write the code.
Fix the fault.
Run all tests
Fix the faults.
Repeat.

YAGNI: 
------

You aren't gonna need it. Only code stuff that is
needed for your latest test. All other
generalizations are hallucinations.

SCIENCE RULES
==============

ESM: Effect size matters.
-------------------------

Statistical significance tests can condone very small
variations in large computations. So always use an effect
size test with the significance test to avoid small
number bullsh*t.

NET: Nine equals ten
--------------------

Minor numeric differences in performance are usually
unstable and disappear when you run the experiment
again. So don't fret the small deltas. 
Always seek the "big a*s" differences.

FSSS: Fast stats, slow stats.
-----------------------------

Two kinds of statistical tests: fast and slow.
Fast tests (parametric, e.g. t-tests) are used as heuristics
during a run to check for (say) early stopping. Slow tests
(non-parametric, e.g. bootstraps) are used after the run
to confirm some experimental hypothesis.

KTS: Keep the seed.
-------------------

To allow for reproduction, keep the seed and print
it as part of the options.

NAN: Normal ain't normal
------------------------

Much reasoning assumes a standard bell shaped
"normal" distribution.  But normal distributions are
not normally found in real world data. So favor
non-parametric distributions over trite normal
descriptions of data.

RNC: Random not crazy 
---------------------

Often the stochastic version is simpler, or scales
better, or both.

MOEA rules
==========

MaxSmarter
----------

Never show users something minimizing something. This
is America! Always maximize!

