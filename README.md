# Circle World
================================

By [Michael Iuzzolino]
University of Colorado, Boulder

About
-----

CircleWorld is a simple foray into Genetic Algorithms. The world consists of a red background, a population of circles, and invisible predators (likely triangles, because we all know how much triangles hate circles). The parental generation of circles begin with randomly assigned colors across the spectrum, as well as random radii within the range of (0, 20]. In a loose analogy to the adapations that many species take on in order to better blend in with their environments and mitigate predation, the circles with the greatest color difference from the background will generate the lowerst amount of fitness, and will therefore die out of the population. Conversely, the circles whose colors differ from the background the least (that is, they blend in well) will thrive, find a mate (amongst the other fittest members), and produce progeny that go on to form the new generation.

During replication, a chance for mutation enables the progeny's color and radius to differ from that of their parents.


Setup
-----

Pull submodules:

```
$ make git
```

Install apt reqs:

```
$ sudo pip install pygame
```

Running
-------
This app is compatible for both Python2 and Python3. Simply run:
```
$ sh run.sh
```

Commands
--------
→ (right arrow):   Advance generations by 1
↑ (up arrow):      Advance generations by 10
↓ (down arrow):    Advance generations by 100
g:                 Advance generations by 1000
q:                 Quit
