Resource management classes and functions.

*Latest release 20220918*:
* MultiOpenMixin.close: report caller of underflow close.
* RunState: new optional handle_signal parameter to override the default method.
* New openif() context manager to open/close an object if it has a .open method.
* MultiOpenMixin.startup_shutdown: be silent for missing (obsolete) .startup, require .shutdown if .startup.

## Class `ClosedError(builtins.Exception, builtins.BaseException)`

Exception for operations invalid when something is closed.

## Class `MultiOpen(MultiOpenMixin, cs.context.ContextManagerMixin)`

Context manager class that manages a single open/close object
using a MultiOpenMixin.

*Method `MultiOpen.__init__(self, openable, finalise_later=False)`*:
Initialise: save the `openable` and call the MultiOpenMixin initialiser.

*Method `MultiOpen.shutdown(self)`*:
Close the associated openable object.

*Method `MultiOpen.startup(self)`*:
Open the associated openable object.

## Class `MultiOpenMixin(cs.context.ContextManagerMixin)`

A multithread safe mixin to count open and close calls,
and to call `.startup` on the first `.open`
and to call `.shutdown` on the last `.close`.

If used as a context manager this mixin calls `open()`/`close()` from
`__enter__()` and `__exit__()`.

It is recommended subclass implementations do as little as possible
during `__init__`, and do almost all setup during startup so
that the class may perform multiple startup/shutdown iterations.

Classes using this mixin need to:
* _either_ define a context manager method `.startup_shutdown`
  which does the startup actions before yeilding
  and then does the shutdown actions
* _or_ define separate `.startup` and `.shutdown` methods.

Example:

    class DatabaseThing(MultiOpenMixin):
        @contextmanager
        def startup_shutdown(self):
            self._db = open_the_database()
            yield
            self._db.close()
    ...
    with DatabaseThing(...) as db_thing:
        ... use db_thing ...

Why not a plain context manager? Because in multithreaded
code one wants to keep the instance "open" while any thread
is still using it.
This mixin lets threads use an instance in overlapping fashion:

    db_thing = DatabaseThing(...)
    with db_thing:
        ... kick off threads with access to the db ...
    ...
    thread 1:
    with db_thing:
       ... use db_thing ...
    thread 2:
    with db_thing:
       ... use db_thing ...

TODO:
* `subopens`: if true (default false) then `.open` will return
  a proxy object with its own `.closed` attribute set by the
  proxy's `.close`.

*Method `MultiOpenMixin.close(self, enforce_final_close=False, caller_frame=None, unopened_ok=False)`*:
Decrement the open count.
If the count goes to zero, call `self.shutdown()` and return its value.

Parameters:
* `enforce_final_close`: if true, the caller expects this to
  be the final close for the object and a `RuntimeError` is
  raised if this is not actually the case.
* `caller_frame`: used for debugging; the caller may specify
  this if necessary, otherwise it is computed from
  `cs.py.stack.caller` when needed. Presently the caller of the
  final close is recorded to help debugging extra close calls.
* `unopened_ok`: if true, it is not an error if this is not open.
  This is intended for closing callbacks which might get called
  even if the original open never happened.
  (I'm looking at you, `cs.resources.RunState`.)

*Property `MultiOpenMixin.closed`*:
Whether this object has been closed.
Note: False if never opened.

*Method `MultiOpenMixin.finalise(self)`*:
Finalise the object, releasing all callers of `.join()`.
Normally this is called automatically after `.shutdown` unless
`finalise_later` was set to true during initialisation.

*Method `MultiOpenMixin.is_opened(func)`*:
Decorator to wrap `MultiOpenMixin` proxy object methods which
should raise if the object is not yet open.

*Method `MultiOpenMixin.join(self)`*:
Join this object.

Wait for the internal _finalise `Condition` (if still not `None`).
Normally this is notified at the end of the shutdown procedure
unless the object's `finalise_later` parameter was true.

*Method `MultiOpenMixin.open(self, caller_frame=None)`*:
Increment the open count.
On the first `.open` call `self.startup()`.

*Method `MultiOpenMixin.startup_shutdown(self)`*:
Default context manager form of startup/shutdown - just
call the distinct `.startup()` and `.shutdown()` methods
if both are present, do nothing if neither use present.

This supports subclasses always using:

    with super().startup_shutdown():

as an outer wrapper.

The `.startup` check is to support legacy subclasses of
`MultiOpenMixin` which have separate `startup()` and
`shutdown()` methods.
The preferred approach is a single `startup_shutdwn()`
context manager overriding this method.

The usual form looks like this:

    @contextmanager
    def startup_shutdown(self):
        with super().startup_shutdown():
            ... do some set up ...
            try:
                yield
            finally:
                ... do some tear down ...

*Method `MultiOpenMixin.tcm_get_state(self)`*:
Support method for `TrackedClassMixin`.

## Function `not_closed(func)`

Decorator to wrap methods of objects with a .closed property
which should raise when self.closed.

## Function `openif(obj)`

Context manager to open `obj` if it has a `.open` method
and also to close it via its `.close` method.
This yields `obj.open()` if defined, or `obj` otherwise.

## Class `Pool`

A generic pool of objects on the premise that reuse is cheaper than recreation.

All the pool objects must be suitable for use, so the
`new_object` callable will typically be a closure.
For example, here is the __init__ for a per-thread AWS Bucket using a
distinct Session:

    def __init__(self, bucket_name):
        Pool.__init__(self, lambda: boto3.session.Session().resource('s3').Bucket(bucket_name)

*Method `Pool.__init__(self, new_object, max_size=None, lock=None)`*:
Initialise the Pool with creator `new_object` and maximum size `max_size`.

Parameters:
* `new_object` is a callable which returns a new object for the Pool.
* `max_size`: The maximum size of the pool of available objects saved for reuse.
    If omitted or `None`, defaults to 4.
    If 0, no upper limit is applied.
* `lock`: optional shared Lock; if omitted or `None` a new Lock is allocated

*Method `Pool.instance(self)`*:
Context manager returning an object for use, which is returned to the pool afterwards.

## Class `RunState(cs.context.ContextManagerMixin)`

A class to track a running task whose cancellation may be requested.

Its purpose is twofold, to provide easily queriable state
around tasks which can start and stop, and to provide control
methods to pronounce that a task has started (`.start`),
should stop (`.cancel`)
and has stopped (`.stop`).

A `RunState` can be used as a context manager, with the enter
and exit methods calling `.start` and `.stop` respectively.
Note that if the suite raises an exception
then the exit method also calls `.cancel` before the call to `.stop`.

Monitor or daemon processes can poll the `RunState` to see when
they should terminate, and may also manage the overall state
easily using a context manager.
Example:

    def monitor(self):
        with self.runstate:
            while not self.runstate.cancelled:
                ... main loop body here ...

A `RunState` has three main methods:
* `.start()`: set `.running` and clear `.cancelled`
* `.cancel()`: set `.cancelled`
* `.stop()`: clear `.running`

A `RunState` has the following properties:
* `cancelled`: true if `.cancel` has been called.
* `running`: true if the task is running.
  Further, assigning a true value to it sets `.start_time` to now.
  Assigning a false value to it sets `.stop_time` to now.
* `start_time`: the time `.running` was last set to true.
* `stop_time`: the time `.running` was last set to false.
* `run_time`: `max(0,.stop_time-.start_time)`
* `stopped`: true if the task is not running.
* `stopping`: true if the task is running but has been cancelled.
* `notify_start`: a set of callables called with the `RunState` instance
  to be called whenever `.running` becomes true.
* `notify_end`: a set of callables called with the `RunState` instance
  to be called whenever `.running` becomes false.
* `notify_cancel`: a set of callables called with the `RunState` instance
  to be called whenever `.cancel` is called.

*Method `RunState.__bool__(self)`*:
Return true if the task is running.

*Method `RunState.__enter_exit__(self)`*:
The `__enter__`/`__exit__` generator function:
* catch signals
* start
* `yield self` => run
* cancel on exception during run
* stop

*Method `RunState.__nonzero__(self)`*:
Return true if the task is running.

*Method `RunState.cancel(self)`*:
Set the cancelled flag; the associated process should notice and stop.

*Method `RunState.catch_signal(self, sig, call_previous=False, verbose=False, handle_signal=None)`*:
Context manager to catch the signal or signals `sig` and
cancel this `RunState`.
Restores the previous handlers on exit.
Yield a mapping of `sig`=>`old_handler`.

Parameters:
* `sig`: an `int` signal number or an iterable of signal numbers
* `call_previous`: optional flag (default `False`)
  passed to `cs.psutils.signal_handlers`
* `verbose`: if true (default `False`),
  issue a `warning` on receipt of a signal

*Method `RunState.end(self)`*:
Stop: adjust state, set `stop_time` to now.
Sets sets `.running` to `False`.

*Method `RunState.handle_signal(self, sig, _)`*:
`RunState` signal handler: cancel the run state.
Warn if `verbose`.

*Property `RunState.run_time`*:
Property returning most recent run time (`stop_time-start_time`).
If still running, use now as the stop time.
If not started, return `0.0`.

*Property `RunState.running`*:
Property expressing whether the task is running.

*Method `RunState.start(self, *a, **kw)`*:
Start: adjust state, set `start_time` to now.
Sets `.cancelled` to `False` and sets `.running` to `True`.

*Method `RunState.stop(self)`*:
Stop: adjust state, set `stop_time` to now.
Sets sets `.running` to `False`.

*Property `RunState.stopped`*:
Was the process stopped? Running is false and cancelled is true.

*Property `RunState.stopping`*:
Is the process stopping? Running is true and cancelled is true.

## Class `RunStateMixin`

Mixin to provide convenient access to a `RunState`.

Provides: `.runstate`, `.cancelled`, `.running`, `.stopping`, `.stopped`.

*Method `RunStateMixin.__init__(self, runstate=None)`*:
Initialise the `RunStateMixin`; sets the `.runstate` attribute.

Parameters:
* `runstate`: optional `RunState` instance or name.
  If a `str`, a new `RunState` with that name is allocated.

*Method `RunStateMixin.cancel(self)`*:
Call .runstate.cancel().

*Property `RunStateMixin.cancelled`*:
Test .runstate.cancelled.

*Property `RunStateMixin.running`*:
Test .runstate.running.

*Property `RunStateMixin.stopped`*:
Test .runstate.stopped.

*Property `RunStateMixin.stopping`*:
Test .runstate.stopping.

# Release Log



*Release 20220918*:
* MultiOpenMixin.close: report caller of underflow close.
* RunState: new optional handle_signal parameter to override the default method.
* New openif() context manager to open/close an object if it has a .open method.
* MultiOpenMixin.startup_shutdown: be silent for missing (obsolete) .startup, require .shutdown if .startup.

*Release 20220429*:
RunState: new catch_signal(sig,verbose=False) context manager method to cancel the RunState on receipt of a signal.

*Release 20211208*:
* MultiOpenMixin.startup_shutdown: since this is the fallback for obsolete uses of MultiOpenMixin, warn if there is no .startup/.shutdown method.
* MultiOpenMixin.startup_shutdown: fix up shutdown logic, was not using a finally clause.
* MultiOpenMixin: use ContextManagerMixin __enter_exit__ generator method instead of __enter__ and __exit__.

*Release 20210906*:
MultiOpenMixin: make startup and shutdown optional.

*Release 20210731*:
RunState: tune the sanity checks around whether the state is "running".

*Release 20210420*:
MultiOpenMixin: run startup/shutdown entirely via the new default method @contextmanager(startup_shutdown), paving the way for subclasses to just define their own startup_shutdown context manager methods instead of distinct startup/shutdown methods.

*Release 20201025*:
MultiOpenMixin.__mo_getstate: dereference self.__dict__ because using AttributeError was pulling a state object from another instance, utterly weird.

*Release 20200718*:
MultiOpenMixin: as a hack to avoid having an __init__, move state into an on demand object accesses by a private method.

*Release 20200521*:
Sweeping removal of cs.obj.O, universally supplanted by types.SimpleNamespace.

*Release 20190812*:
* MultiOpenMixin: no longer subclass cs.obj.O.
* MultiOpenMixin: remove `lock` param support, the mixin has its own lock.
* MultiOpen: drop `lock` param support, no longer used by MultiOpenMixin.
* MultiOpenMixin: do finalise inside the lock for the same reason as shutdown (competition with open/startup).
* MultiOpenMixin.close: new `unopened_ok=False` parameter intended for callback closes which might fire even if the initial open does not occur.

*Release 20190617*:
RunState.__exit__: if an exception was raised call .canel() before calling .stop().

*Release 20190103*:
* Bugfixes for context managers.
* MultiOpenMixin fixes and changes.
* RunState improvements.

*Release 20171024*:
* bugfix MultiOpenMixin finalise logic and other small logic fixes and checs
* new class RunState for tracking or controlling a running task

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
* BREAKING CHANGE: rename NestingOpenCloseMixin to MultiOpenMixin.
* New Pool class for generic object reuse.
* Assorted minor improvements.

*Release 20150115*:
First PyPI release.
