# Twin Sister: Pure Python Dependency Injection

> No, I am Zoot's identical twin sister, Dingo.

## What is dependency injection and why should I care?

If you write unit tests (and you do write them, right?) you have encountered
situations where the unit you are testing depends on some component outside of
itself.  For example, a unit that retrieves data from an HTTP API depends on
an HTTP client.  By definition, a unit test does not include systems outside
the unit, so does not make real network requests.  Instead, it configures the
unit to make fake requests using a component with the same interface as the real
HTTP client.  The mechanism that replaces the real HTTP client with a fake one
is a kind of dependency injection.

## Dependency injection mechanisms

### Most simple: specify initializer arguments

```
class Knight:

  def __init__(self, *, http_client=None):
    if not http_client:
      http_client = HttpClient()
```

In the example above, new knight objects will ordinarily construct a real HTTP
client for themselves, but the code that creates them has the opportunity to
inject an alternative client like this:

```
fake = FakeHttpClient()
sir_lancelot = Knight(http_client=fake)
```

This approach has the advantage of being simple and straightforward and can
be more than adequate if the problem space is small and well-contained.
It begins to break down, however, as the system under test becomes more
complex.  The initializer must specify each dependency that can be injected
and the target bears responsibility for maintaining each injected object and
passing it to sub-components as they are created.

In many cases, this approach will force classes to be aware of injected entities
that otherwise ought not concern them.  For example

```
class Horse:

  def __init__(self, *, tail=None):
    self.tail = tail or HorseTail()


class Knight:

  def __init__(self, *, tail_for_horse=None):
    self.horse = Horse(tail=tail_for_horse)
```

The _only_ reason `Knight.__init__` has for accepting `tail_for_horse` is to
pass it through to `Horse.__init__`.  This is awkward, aside from its damage
to separation of concerns.


### Most thorough: subvert the global symbol table

In theory, it would be possible to make _all_ HTTP clients fake by redirecting
HttpClient in the global symbol table to FakeHttpClient.  This approach has
the advantage of not requiring the targeted code to be aware of the injection
and is likely to be highly effective if successful. It suffers from major drawbacks,
however. The symtable module (sensibly) does not permit write access, so redirection would
need to be performed at a lower level which would break compatibility across
Python implementations. It's also an extreme hack with potentially serious side
effects.

### Middle ground: request dependencies explicitly

Twin Sister takes a middle approach.  It maintains a registry of symbols
that have been injected and then handles requests for dependencies.  In this way,
only code that requests a dependency explicity is affected by injection:

```
from younger_twin_sister import dependency

class Horse:

  def __init__(self):
    self.tail = dependency(Tail)()


class Knight:

  def __init__(self):
    self.horse = dependency(Horse)()
```

`dependency` returns the injected replacement if one exists.  Otherwise, it
returns the real thing.  In this way, the system will behave sensibly whether
injection has occurred or not.


# Injecting a dependency with Twin Sister

## Installation

```
python setup.py install
```

## Generic technique to inject any object as a dependency

```
from younger_twin_sister import dependency, dependency_context

class Knight:

  def __init__(self):
    self.horse = dependency(Horse)()
    self.start_month = dependency(current_month)()
    self.guess = dependency(VELOCITY_OF_SOUTH_AFRICAN_SWALLOW)


with dependency_context() as context:
  context.inject(Horse, FakeHorse)
  context.inject(current_month, lambda: 'February')
  context.inject(VELOCITY_OF_SOUTH_AFRICAN_SWALLOW, 42)
  lancelot = Knight()
  lancelot.visit_castle()
  expect(lancelot.strength).to(equal(0))
```

Injection is effective only inside the dependency context.  Inside the context,
requests for `Horse` will return `FakeHorse`.  Outside the context
(after the `with` statement), requests for `Horse` will return `Horse`.


## Special technique: "classes" that always produce the same object

```
with dependency_context() as context:
  eric_the_horse = FakeHorse()
  context.inject_as_class(Horse, eric_the_horse)
  lancelot = Knight()
  lancelot.visit_castle()
  expect(eric_the_horse.hunger).to(equal(42))
```

Each time the system under test executes code like this

```
fresh_horse = dependency(Horse)()
```

fresh_horse will be the same old eric_the_horse.


## Support for xUnit test pattern

Instead of using a context manager, a test can open and close its
dependency context explicitly:


```
from pw_dependency_injector import open_dependency_context


class MyTest(TestCase):

  def setUp(self):
    self.dependencies = open_dependency_context()

  def tearDown(self):
    self.dependencies.close()

  def test_something(self):
    self.dependencies.inject(Horse, FakeHorse)
    outcome = visit_anthrax(spams=37)
    expect(outcome).to(equal('Cardinal Ximinez'))

```

## Support for multi-threaded tests

By default, Twin Sister maintains a separate dependency context for each thread.
This allows test cases with different dependency schemes to run in parallel
without affecting each other.

However, it also provides a mechanism to attach a dependency context to a running
thread:

```
my_thread = Thread(target=spam)
my_thread.start()

with dependency_context() as context:
  context.attach_to_thread(my_thread)
  ...
```

The usual rules about context scope apply.  Even if the thread continues to run,
the context will disappear after the `with` statement ends.


## Controlling time

Sometimes it is useful -- or even necessary -- for a test case to
control time as its perceived by the system under test.  The classic example
is a routine that times out after a specified duration has elapsed.  Thorough
testing should cover both sides of the boundary, but it is usually undesirable
or impractical to wait for the duration to elapse.  That is where TimeController
comes in.  It's a self-contained way to inject a fake datetime.datetime:

```
from expects import expect, be_a, be_none
from younger_twin_sister import TimeController

# Verify that the function times out after 24 hours
time_travel = TimeController(target=some_function_i_want_to_test)
time_travel.start()
time_travel.advance(hours=24)
sleep(0.05)  # Give target a chance to cycle
expect(time_travel.exception_caught).to(be_a(TimeoutError))

# Verify that the function does not time out before 24 hours
time_travel = TimeController(target=some_function_i_want_to_test)
time_travel.start()
time_travel.advance(hours=24 - 0.0001)
sleep(0.05)  # Give target a chance to cycle
expect(time_travel.exception_caught).to(be_none)
```

The example above checks for the presence or absence of an exception, but it
is possible to check _any_ state.  For example, let's check the impact of
a long-running bound method on its object:

```
time_travel = TimeController(target=thing.monitor_age)
time_travel.start()
time_travel.advance(days=30)
sleep(0.05)
expect(thing.age_in_days).to(equal(30))
time_travel.advance(days=30)
sleep(0.05)
expect(thing.age_in_days).to(equal(60))
```

There are limitations.  The fake datetime affects only .now() and .utcnow()
at present.  This may change in a future release as needs arise.

## Fake environment variables integration
```
real_path = os.environ['PATH']
fake_path = 'something else'
with dependency_context(supply_env=True) as context:
  context.set_env(PATH=fake_path)
  assert(dependency(os).environ['PATH']) == fake_path
assert os.environ['PATH'] == real_path
```


## Fake filesystem (PyFakeFS) integration

```
with dependency_context(supply_fs=True):
  filename = 'favorites.txt'
  open = dependency(open)
  with open(filename, 'w') as f:
     f.write('some of my favorite things')
  with open(filename, 'r') as f:
     print('From the fake file: %s' % f.read())
  assert dependency(os).path.exists(filename)
assert not os.path.exists(filename)
```

## Fake log system integration
```
message = 'This goes only to the fake log'
with dependency_context(supply_logging=True) as context:
  log = dependency(logging).getLogger(__name__)
  log.error(message)
  # fake_log.stored_records is a list of logging.LogRecord objects
  assert context.fake_log.stored_records[0].msg == message
```
