from unittest import TestCase, main

from expects import \
    expect, be, be_a, be_above, \
    be_above_or_equal, be_below, be_below_or_equal, equal, \
    have_length

from twin_sister.fakes import EmptyFake, MutableObject
from twin_sister.expects_matchers import complain


class TestEmptyFake(TestCase):

    def test_call_accepts_arbitary_args_and_kwargs(self):
        expect(lambda: EmptyFake()(4, spams=1)).not_to(
            complain(TypeError))

    def test_call_returns_fresh_fake(self):
        original = EmptyFake()
        returned = original()
        expect(returned).to(be_a(EmptyFake))
        expect(returned).not_to(be(original))

    def test_contains_returns_false(self):
        expect('beans' in EmptyFake()).to(be(False))

    def test_can_be_context_manager(self):

        def attempt():
            with EmptyFake(1, beans=0):
                pass

        expect(attempt).not_to(complain(TypeError))

    def test_yields_fresh_fake(self):
        original = EmptyFake()

        with original as context:
            expect(context).to(be_a(EmptyFake))
            expect(context).not_to(be(original))

    def test_delitem_is_present(self):

        def attempt():
            del EmptyFake()['witch']

        expect(attempt).not_to(complain(TypeError))

    def test_eq_returns_true_if_other_is_empty_fake(self):
        expect(EmptyFake()).to(equal(EmptyFake()))

    def test_eq_returns_false_if_other_is_not_empty_fake(self):
        expect(EmptyFake()).not_to(equal(dict()))

    def test_float_is_0_point_0(self):
        expect(float(EmptyFake())).to(equal(0.0))

    def test_getattr_returns_fresh_fake(self):
        original = EmptyFake()
        returned = original.ximinez
        expect(returned).to(be_a(EmptyFake))
        expect(returned).not_to(be(original))

    def test_getitem_returns_fresh_fake(self):
        original = EmptyFake()
        returned = original['biggles']
        expect(returned).to(be_a(EmptyFake))
        expect(returned).not_to(be(original))

    def test_ge_is_true_if_other_is_empty_fake(self):
        expect(EmptyFake()).to(be_above_or_equal(EmptyFake()))

    def test_ge_is_false_if_other_is_not_empty_fake(self):
        expect(EmptyFake()).not_to(be_above_or_equal(42))

    def test_gt_returns_false(self):
        expect(EmptyFake()).not_to(be_above(42))

    def test_same_fake_has_same_hash(self):
        fake = EmptyFake()
        expect(hash(fake)).to(equal(hash(fake)))

    def test_different_fake_has_different_hash(self):
        expect(hash(EmptyFake())).not_to(equal(hash(EmptyFake())))

    def test_iter_returns_self(self):
        fake = EmptyFake()
        expect(iter(fake)).to(be(fake))

    def test_le_returns_true_if_other_is_empty_fake(self):
        expect(EmptyFake()).to(be_below_or_equal(EmptyFake()))

    def test_returns_false_if_other_is_not_empty_fake(self):
        expect(EmptyFake()).not_to(be_below_or_equal(42))

    def test_lt_returns_false(self):
        expect(EmptyFake()).not_to(be_below(42))

    def test_len_is_0(self):
        expect(EmptyFake()).to(have_length(0))

    def test_ne_returns_true_if_other_is_not_empty_fake(self):
        assert EmptyFake() != 42, '__ne__ returned false for 42'

    def test_ne_returns_false_if_other_is_empty_fake(self):
        assert not(EmptyFake() != EmptyFake()), \
            '__ne__ returned true for another EmptyFake'

    def test_next_raises_stop_iteration(self):
        expect(lambda: next(EmptyFake())).to(
            complain(StopIteration))

    def test_reversed_returns_self(self):
        fake = EmptyFake()
        expect(reversed(fake)).to(be(fake))

    def test_setitem_is_present(self):
        expect(lambda: EmptyFake()['spam']).not_to(
            complain(TypeError))

    def test_str_returns_str(self):
        expect(str(EmptyFake())).to(be_a(str))

    def test_raises_attribute_error_on_attempt_to_break_pattern_object(self):
        pattern = object()
        fake = EmptyFake(pattern_obj=pattern)
        expect(lambda: fake.nope).to(complain(AttributeError))

    def test_returns_empty_fake_when_obj_pattern_satisfied(self):
        pattern = MutableObject()
        attr = 'yup'
        setattr(pattern, attr, None)
        fake = EmptyFake(pattern_obj=pattern)
        returned = getattr(fake, attr)
        expect(returned).to(be_a(EmptyFake))
        # Verify that the pattern restriction is not inherited
        expect(returned.spam).to(be_a(EmptyFake))

    def test_respects_hasattr_for_pattern_objects(self):

        class Pattern:
            def __getattr__(self, name):
                return 'spam'

        fake = EmptyFake(pattern_obj=Pattern())
        assert hasattr(fake, 'anything'), 'hasattr returned False'

    def test_can_use_falsy_object_patterns(self):
        fake = EmptyFake(pattern_obj=set())
        expect(lambda: fake.spam).to(complain(AttributeError))

    def test_raises_attribute_error_on_attempt_to_break_pattern_cls(self):
        fake = EmptyFake(pattern_cls=str)
        expect(lambda: fake.spam).to(complain(AttributeError))

    def test_returns_empty_fake_when_cls_pattern_satisfied(self):
        fake = EmptyFake(pattern_cls=str)
        returned = fake.split
        expect(returned).to(be_a(EmptyFake))
        expect(returned.spam).to(be_a(EmptyFake))

    def test_complains_about_attempt_to_set_pattern_obj_and_cls(self):
        expect(lambda: EmptyFake(pattern_cls=str, pattern_obj=1)).to(
            complain(TypeError))

    def test_check_for_both_patterns_not_fooled_by_falsy_objects(self):
        expect(lambda: EmptyFake(pattern_cls=str, pattern_obj=0)).to(
            complain(TypeError))

    def test_getattr_does_not_invent_private_attributes(self):
        expect(lambda: EmptyFake()._private).to(
            complain(AttributeError))

    def test_str_behaves_sensibly_for_subclass_that_neglects_super(self):

        class BadFake(EmptyFake):

            def __init__(self):
                pass

        expect(str(BadFake())).to(be_a(str))


if '__main__' == __name__:
    main()
