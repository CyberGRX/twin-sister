> Twin Sister:
## A Unit Testing Toolkit with Pure Python Dependency Injection

> No, I am Zoot's identical twin sister, Dingo.

## How Twin Sister can help you

Whether or not you accept Michael Feathers's definition of "legacy code" as
"code without tests," you know that you should write unit tests and that it
would be a Good Thing if those tests were legible enough to show what your code
does and effective enough to tell you when you've broken something.  On the
other hand, writing good unit tests can be _hard_ -- especially when they need
to cover the unit's interactions with external components.

Enter Twin Sister.  Initially an internal project at ProtectWise in 2016, it
was released as open source in 2017 and has been in continuous and expanding
use ever since.  Its goal is to make unit tests easier to write and easier to
read without doing violence to the system-under-test.  It consists of a small
library of test doubles and a pure Python dependency injector to deliver them
(or anything else that suits your fancy).

## What it looks like in action ##

`test_post_something.py`
```
from unittest import TestCase

from expects import expect, equal
import requests
from twin_sister import open_dependency_context
from twin_sister.fakes import EmptyFake, FunctionSpy

from post_something import post_something

class TestPostSomething(TestCase):

  def setUp(self):
      self.context = open_dependency_context()
      self.post_spy = FunctionSpy()
      requests_stub = EmptyFake(pattern_obj=requests)
      requests_stub.post = self.post_spy
      self.context.inject(requests, requests_stub)

  def tearDown(self):
      self.context.close()

  def test_uses_post_method(self):
      post_something('yadda')
      self.post_spy.assert_was_called()

  def test_sends_specified_content(self):
      content = 'yadda yadda yadda'
      post_something(content)
      expect(self.post_spy['data']).to(equal(content))  
```

`post_something.py`
```
import requests
from twin_sister import dependency

def post_something(content):
    post = dependency(requests).post
    post('http://example.com/some-api', data=content)
```

## Learning More ##
- ### <a href="#dependency-injection-section">Dependency injection mechanism</a>
  - #### <a href="#injection-techniques-section"/>Dependency injection techniques</a>
  - #### <a href="#injecting-section">Injecting a dependency with Twin Sister</a>
    - <a href="#object-injection-section">Generic technique to inject any object</a>
    - <a href="#object-as-class-injection-section">Injecting a class that always produces the same object</a>
    - <a href="#xunit-section">Support for the xUnit test pattern</a>
    - <a href="#multi-threaded-test-section">Support for multi-threaded tests</a>
- ### <a href="#context-section">The dependency context and built-in fakery</a>
  - #### <a href="#fake-environment-section">Fake environment variables</a>
  - #### <a href="#fake-logging-section">Fake logging</a>
  - #### <a href="#fake-filesystem-section">Fake filesystem</a>
  - #### <a href="#fake-time-section">Fake time</a>
- ### <a href="#doubles-section">Test doubles</a>
  - #### <a href="#mutable-object-section">MutableObject</a>
  - #### <a href="#empty-fake-section">EmptyFake</a>
  - #### <a href="#empty-context-manager-section">empty_context_manager</a>
  - #### <a href="#fake-datetime-section">FakeDateTime</a>
  - #### <a href="#function-spy-section">FunctionSpy</a>
  - #### <a href="#master-spy-section">MasterSpy</a>
- ### <a href="#expects-matchers-section">Expects matchers</a>
  - #### <a href="#complain-section">complain</a>
  - #### <a href="#contain-all-items-section">contain_all_items_in</a>


<a name="dependency-injection-section"></a>

# Dependency injection mechanism #

## What is dependency injection and why should I care? ##

If you write tests for non-trivial units, you have encountered
situations where the unit you are testing depends on some component outside of
itself.  For example, a unit that retrieves data from an HTTP API depends on
an HTTP client.  By definition, a unit test does not include systems outside
the unit, so does not make real network requests.  Instead, it configures the
unit to make fake requests using a component with the same interface as the real
HTTP client.  The mechanism that replaces the real HTTP client with a fake one
is a kind of dependency injection.

<a name="injection-techniques-section"></a>

## Dependency injection techniques ##

### Most simple: specify initializer arguments ###

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
complex.  One manifestation of this breakdown is the appearance of "hobo arguments."   The initializer must specify each dependency that can be injected
and the target bears responsibility for maintaining each injected object and
passing it to sub-components as they are created.

For example


```
class Horse:

  def __init__(self, *, tail=None):
    self.tail = tail or HorseTail()


class Knight:

  def __init__(self, *, tail_for_horse=None):
    self.horse = Horse(tail=tail_for_horse)
```

`tail_for_horse` is a hobo.  The _only_ reason `Knight.__init__` has for accepting it is to
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
from twin_sister import dependency

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


<a name="injecting-section"></a>

# Injecting a dependency with Twin Sister


## Installation from pip

```
pip install twin-sister
```

## Installation from source

```
python setup.py install
```

<a name="object-injection-section"></a>

## Generic technique to inject any object ##

```
from twin_sister import dependency, dependency_context

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


<a name="object-as-class-injection-section"></a>

## Injecting a class that always produces the same object ##

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


<a name="xunit-section"></a>

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

<a name="multi-threaded-test-section"></a>

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

<a name="context-section"></a>

# The dependency context and built-in fakery #

The dependency context is essentially a dictionary that maps real objects to their injected fakes, but it also knows how to fake some commonly-used components from the Python standard library.

<a name="fake-environment-section"></a>

## Fake environment variables

Most of the time, we don't want our unit tests to inherit real environment variables because that would introduce an implicit dependency on system configuration.  Instead, we create a dependency context with `supply_env=True`.  This creates a fake set of environment variables, initially empty.  We can then add environment variables as expected by our system under test:

```
with dependency_context(supply_env=True) as context:
  context.set_env(PATH='/bin', SPAM='eggs')
```

The fake environment is just a dictionary in an injected `os`, so the system-under-test must request it explicitly as a dependency:

```
path = dependency(os).environ['PATH']
```

The injected `os` is mostly a passthrough to the real thing.

<a name="fake-logging-section"></a>

## Fake logging

Most of the time, we don't want our unit tests to use the real Python logging system -- especially if it writes messages to standard output (as it usually does).  This makes tests fill standard output with noise from useless logging messages. Some of the time, we want our tests to see the log messages produced by the system-under-test.  The fake log system meets both needs.

```
message = 'This goes only to the fake log'
with dependency_context(supply_logging=True) as context:
  log = dependency(logging).getLogger(__name__)
  log.error(message)
  # logging.stored_records is a list of logging.LogRecord objects
  assert context.logging.stored_records[0].msg == message
```

<a name="fake-filesystem-section"></a>

## Fake filesystem

Most of the time, we don't want our unit tests to use the real filesystem.  That would introduce an implicit dependency on actual system state and potentially leave a mess behind.  To solve this problem, the dependency context can leverage [pyfakefs](https://pypi.org/project/pyfakefs/) to supply a fake filesystem.

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

<a name="fake-time-section"></a>

## Fake time

Sometimes it is useful -- or even necessary -- for a test case to
control time as its perceived by the system-under-test.  The classic example
is a routine that times out after a specified duration has elapsed.  Thorough
testing should cover both sides of the boundary, but it is usually undesirable
or impractical to wait for the duration to elapse.  That is where TimeController
comes in.  It's a self-contained way to inject a fake datetime.datetime:

```
from expects import expect, be_a, be_none
from twin_sister import TimeController

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

We can also check the return value of the target function:

```
expected = 42
time_travel = TimeController(target=lambda: expected)
time_travel_start()
time_travel.join()
expect(time_travel.value_returned).to(equal(expected))
```

By default, TimeController has its own dependency context, but it can
inherit a specified one instead:

```
with open_dependency_context() as context:
    tc = context.create_time_controller(target=some_function)
```

There are limitations.  The fake datetime affects only .now() and .utcnow()
at present.  This may change in a future release as needs arise.


<a name="doubles-section"></a>

# Test Doubles #

Classically, test doubles fall into three general categories:

#### Stubs ####
A stub faces the unit-under-test and mimics the behavior of some external component.

#### Spies ####
A spy faces the test and reports on the behavior of the unit-under-test.

#### Mocks ####
A mock is a stub that contains assertions.  Twin Sister's `fakes` module has none of these but most of the supplied fakes are so generic that mock behavior can be added.


## Supplied Stubs ##

<a name="mutable-object-section"></a>

### MutableObject ###

Embarrassingly simple, but frequently useful for creating stubs on the fly:

```
from twin_sister.fakes import MutableObject

stub = MutableObject()
stub.say_hello = lambda: 'hello, world'
```

<a name="empty-fake-section"></a>

### EmptyFake ###

An extremely generic stub that aims to be a substitute for absolutely anything.  Its attributes are EmptyFake objects.  When it's called like a function, it returns another EmptyFake.

When invoked with no arguments, EmptyFake creates the most flexible fake possible:

```
from twin_sister.fakes import EmptyFake

anything = EmptyFake()
another_empty_fake = anything.spam
yet_another_empty_fake = another_empty_fake(biggles=12)
```

It's possible to restrict an EmptyFake to attributes defined by some other object:

```
stub_path = EmptyFake(pattern_obj=os.path)
# The next line returns an EmptyFake because there is an os.path.join:
an_empty_fake = stub_path.join
# The next line will raise AttributeError because there is no os.path.spam:
stub_path.spam
```

It's also possible to restrict an EmptyFake to attributes declared by a class:

```
fake_string = EmptyFake(pattern_class=str)
# The next line returns an EmptyFake because strings have attributes called "split"
an_empty_fake = fake_string.split
# The next will raise AttributeError because normal strings lack beans:
fake_string.beans
```

Important limitation: "declared by a class" means that the attribute appears in
the class declaration.  If the attribute gets created by the initializer instead,
then it's not declared by the class and EmptyFake will insist that the attribute
does not exist.  If you need an attribute that gets created by the initializer,
you're better off instantiating an object to use as a `pattern_obj`.

<a name="empty-context-manager-section"></a>

### empty_context_manager ###

A context manager that does nothing and yields an EmptyFake, useful for preventing unwanted behavior like opening network connections.

```
from twin_sister.fakes import empty_context_manager

from my_stuff import network_connection

with dependency_context() as context:
  context.inject(network_connection, empty_context_manager)
  with dependency(network_connection)() as conn:
     conn.send("I'm singing into an EmptyFake")
```

A generic EmptyFake object will also serve as a context manager without complaints.


<a name="fake-datetime-section"></a>

### FakeDateTime ###

A datetime.datetime stub that reports that reports a fixed time.

```
from twin_sister.fakes import FakeDateTime

t = FakeDateTime(fixed_time=datetime.now())
# Returns the time when t was instantiated
t.now()
t.fixed_time = now()
# Returns a slightly later time
t.now()
```


## Supplied Spies ##

<a name="function-spy-section"></a>

### FunctionSpy ###

Pretends to be a real function and tracks calls to itself.

```
from twin_sister.fakes import FunctionSpy

fixed_return_value = 4
spy = FunctionSpy(return_value=fixed_return_value)
returned = spy(6, 37, expected='biggles')
spy.assert_was_called()
assert returned == fixed_return_value
assert spy.args_from_last_call() == (6, 37)
assert spy.kwargs_from_last_call() == {'expected': biggles}
assert spy[0] == 6
assert spy[1] == 37
assert spy['expected'] == biggles

spy('spam', 'eggs', volume=12)
assert spy[1] == 'eggs'

args, kwargs = spy.call_history[0]
assert args == (6, 37)
assert kwargs == {'expected': 'biggles'}
```


<a name="master-spy-section"></a>

### MasterSpy ###

The spy equivalent of EmptyFake, MasterSpy tracks every interaction and spawns
more spies to track interactions with its attributes.

```
from twin_sister.fakes import MasterSpy, MutableObject

target = MutableObject()
target.foo = 42
target.bar = 'soap'
target.sing = lambda thing: f'lovely {thing}'
master = MasterSpy(target=target, affect_only_functions=False)

assert master.foo == target.foo
master.bar.replace('a', 'u')
bar_spy = master.attribute_spies['bar']
args, kwargs = bar_spy.last_call_to('replace')
assert args == ('a', 'u')

master.sing(thing='SPAM')
sing_spy = master.attribute_spies('sing')
args, kwargs = sing_spy.call_history[0]
assert kwargs['thing'] == 'SPAM'
```

By default MasterSpy spawns spies only for attributes that are functions.


<a name="expects-matchers-section"></a>

# Expects Matchers #

Custom matchers for [expects](https://pypi.org/project/expects/), an
alternative way to assert.

<a name="complain-section"></a>

## complain ##

`expects.raise_error` will quietly return False if an unexpected exception is raised.
`twin_sister.expects_matchers.complain`, by contrast, will re-raise the exception.
Otherwise, the matchers are essentially equivalent.

```
from expects import expect, raise_error
from twin_sister.expects_matchers import complain

class SpamException(RuntimeError):
  pass

class EggsException(RuntimeError):
   pass

def raise_spam():
   raise SpamException()

def raise_eggs():
   raise EggsException()

# both exit quietly because the expectation is met
expect(raise_spam).to(raise_error(SpamException))
expect(raise_spam).to(complain(SpamException))

# exits quietly because a different exception was raised
expect(raise_eggs).not_to(raise_error(SpamException))

# re-raises the exception because it differs from the expectation
expect(raise_eggs).not_to(complain(SpamException))
```


<a name="contain-all-items-section"></a>

## contain_all_items_in ##

Returns true if one dictionary contains all of the items in another.

```
from expects import expect
from twin_sister.expects_matchers import contain_all_items_in

expect({'foo': 1, 'bar': 2}).to(contain_all_items_in({'foo': 1}))
expect({'foo': 1}).not_to(contain_all_items_in({'foo': 1, 'bar': 2}))
```
