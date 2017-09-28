## Dependency injection mechanism

### Reference an object in a way that enables dependency injection

Instead of this

```
def frozzle_a_thing(spams):
  thing = Thing(spams=spams)
  thing.frozzle()
```

write this

```
from pw_dependency_injector import dependency

def frozzle_a_thing(spams):
  thing = dependency(Thing)(spams=spams)
  thing.frozzle()
```


### Inject a dependency using a context manager

```
from pw_dependency_injector import dependency_context

with dependency_context as context:
  context.inject(Thing, FakeThing)
  frozzle_a_thing(spams=37)
```

### Inject a dependency using an xUnit pattern

```
from pw_dependency_injector import open_dependency_context


class MyTest(TestCase):

  def setUp(self):
    self.dependencies = open_dependency_context()

  def test_something(self):
    self.dependencies.inject(Thing, FakeThing)
    outcome = frozzle_a_thing(spams=37)
    expect(outcome).to(equal('cardinal_ximinez'))

  def tearDown(self):
    self.dependencies_close()
```


### Return the same fake object every time the SUT instantiates a given class

```
from pw_dependency_injector import dependency, dependency_context

def frozzle_a_thing()
  thing = dependency(Thing)()
  thing.frozzle()

my_fake_thing = FakeThing()
with dependency_context as context:
  context.inject_as_class(Thing, my_fake_thing)
  frozzle_a_thing()
```

Without the injection ```dependency``` returns the Thing class so frozzle_a_thing() instantiates a ```Thing```
and assigns it to the ```thing``` variable.

With the injection, ```dependency``` returns a ```SingletonClass``` instance which wraps ```my_fake_thing```.
```SingletonClass``` pretends to be a class but actually returns its wrapped object when it is invoked.
Therefore, the ```thing``` variable will become a reference to ```my_fake_thing``` instead of a new ```Thing``` instance.
