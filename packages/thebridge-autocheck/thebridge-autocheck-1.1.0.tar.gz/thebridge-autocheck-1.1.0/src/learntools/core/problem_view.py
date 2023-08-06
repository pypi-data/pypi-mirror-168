import functools
import traceback
from collections import Counter

import ipywidgets as widgets
from IPython.display import display, clear_output

from learntools.core.richtext import *
from learntools.core.exceptions import *
from learntools.core.problem import *
from learntools.core import colors, tracking

def displayer(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        res = fn(*args, **kwargs)
        display(res)
        # Don't propagate the return to avoid double printing.
    return wrapped

def record(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        self.interactions[method.__name__] += 1
        return method(self, *args, **kwargs)
    return wrapped

class ProblemView:

    _not_attempted_msg = ("When you've updated the starter code, `check()` will"
            " tell you whether your code is correct."
    )

    def __init__(self, problem:Problem, globals_):
        self.problem = problem
        self.globals = globals_
        self.interactions = Counter()
        # The outcome of the last call to .check (as a tracking.OutcomeType).
        # Used for notebook testing.
        self._last_outcome = None

    def __getattr__(self, attr):
        """By default, expose methods of the contained Problem object if
        they're not marked private.
        """
        val = getattr(self.problem, attr)
        if not attr.endswith('_') and callable(val):
            return val
        raise AttributeError

    @property
    def questionId(self):
        # e.g. '3_MyHardProblem'
        id = self.problem.__class__.__name__
        if hasattr(self, '_order'):
            id = '{}_{}'.format(self._order, id)
        return id

    def _track_event(self, interactionType, **kwargs):
        kwargs['interactionType'] = interactionType

        if isinstance(self.problem, EqualityCheckProblem):
            kwargs['questionType'] = tracking.QuestionType.EQUALITYCHECKPROBLEM
        elif isinstance(self.problem, CodingProblem):
            kwargs['questionType'] = tracking.QuestionType.CODINGPROBLEM
        elif isinstance(self.problem, FunctionProblem):
            kwargs['questionType'] = tracking.QuestionType.FUNCTIONPROBLEM
        elif isinstance(self.problem, ThoughtExperiment):
            kwargs['questionType'] = tracking.QuestionType.THOUGHTEXPERIMENT

        problem_fields = dict(
                questionId=self.questionId,
            )
        kwargs.update(problem_fields)
        tracking.track(kwargs)

    def _track_check(self, outcome, **kwargs):
        self._last_outcome = outcome
        if outcome == tracking.OutcomeType.PASS:
            kwargs['valueTowardsCompletion'] = self.problem.point_value
        self._track_event(tracking.InteractionType.CHECK, outcomeType=outcome, **kwargs)

    @record
    @displayer
    def check(self):
        try:
            if isinstance(self.problem, CodingProblem):
                args = self._get_injected_args()
            else:
                args = ()
            self.problem.check_whether_attempted(*args)
            self.problem.check(*args)
        except NotAttempted as e:
            self._track_check(tracking.OutcomeType.UNATTEMPTED)
            return ProblemStatement(self._not_attempted_msg + ' ' + str(e))
        except (Incorrect, AssertionError) as e:
            if isinstance(e, UserlandExceptionIncorrect):
                wrapped = e.wrapped_exception
                tb_lines = traceback.format_tb(wrapped.__traceback__)
                tb_str = '\n'.join(tb_lines)
                self._track_check(tracking.OutcomeType.EXCEPTION,
                    exceptionClass=wrapped.__class__.__name__,
                    trace=tb_str,
                    failureMessage=str(e),
                    )
            else:
                self._track_check(tracking.OutcomeType.FAIL,
                    failureMessage=str(e),
                    )
            return TestFailure(str(e))
        except Uncheckable as e:
            msg = str(e) or 'Sorry, no auto-checking available for this question.'
            self._track_check(tracking.OutcomeType.EXCEPTION,
                failureMessage=msg,
                exceptionClass='Uncheckable',
                trace='',
            )
            return RichText(msg, color=colors.WARN)
        else:
            self._track_check(tracking.OutcomeType.PASS)
            if hasattr(self.problem, '_congrats'):
                return Correct(self.problem._correct_message,
                               _congrats=self.problem._congrats)
            else:
                return Correct(self.problem._correct_message)

    def _get_injected_args(self):
        names = self.problem.injectable_vars
        missing = set(names) - self.globals.keys()
        if len(missing) == 0:
            return self.globals.lookup(names)
        elif len(missing) == len(names):
            # Hm, maybe RichText objects should be raisable? Or is that too much?
            raise NotAttempted("Remember, you must create the following variable{}: {}"\
                    .format('s' if len(missing) > 1 else '',
                        ', '.join('`{}`'.format(v) for v in missing)
                        )
                    )
        else:
            raise Incorrect("You still need to define the following variables: {}".format(
                    ', '.join('`{}`'.format(v) for v in missing)
                    ))


    @record
    @displayer
    def hint(self, n=1):
        hints = self.problem.hints
        if not hints:
            msg = 'Sorry, no hints available for this question.'
            self._track_event(tracking.InteractionType.HINT, failureMessage=msg)
            return RichText(msg, color=colors.WARN)
        self._track_event(tracking.InteractionType.HINT)
        # TODO: maybe wrap these kinds of user errors to present them in a nicer way?
        # (e.g. LearnUserError, LearnUsageError)
        assert n <= len(hints), "No further hints available!"
        hint = hints[n-1]
        assert isinstance(hint, str)
        return Hint(hint, n, last=(n == len(hints)))

    @record
    @displayer
    def solution(self):
        self._track_event(tracking.InteractionType.SOLUTION)
        soln = self.problem.solution
        if isinstance(soln, RichText):
            return soln
        return Solution(soln)

    def _assert_last_outcome(self, outcome):
        self.check()
        assert self._last_outcome == outcome, ("Expected last outcome to be {}, but was {}".format(
            outcome, self._last_outcome))

    def assert_check_unattempted(self):
        self._assert_last_outcome(tracking.OutcomeType.UNATTEMPTED)

    def assert_check_failed(self):
        self._assert_last_outcome(tracking.OutcomeType.FAIL)

    def assert_check_passed(self):
        self._assert_last_outcome(tracking.OutcomeType.PASS)

    ## Buttons for Jupyter Notebooks (Jupyter app)
    def hint_button(self, i):
        b1 = widgets.Button(description='Hint {}'.format(i), 
                            style=dict( button_color = colors.HINT,
                                        font_style='italic',
                                        font_weight='bold'
                                    ))
        out = widgets.Output()
        display(b1, out)
        def on_button_clicked(_):
            # "linking function with output"
            with out:
                clear_output()
                # what happens when we press the button
                self.hint(i)
        # linking button and function together using a button's method
        b1.on_click(on_button_clicked)
    
    def sol_button(self):
        b1 = widgets.Button(description='Solution', 
                            style=dict( button_color = colors.SOLUTION,
                                        font_style='italic',
                                        font_weight='bold'
                                    ))
        out = widgets.Output()
        display(b1, out)
        def on_button_clicked(_):
            with out:
                clear_output()
                self.solution()
        b1.on_click(on_button_clicked)

    def check_button(self):
        b1 = widgets.Button(description='Check', 
                            style=dict( button_color = colors.WARN,
                                        font_style='italic',
                                        font_weight='bold'
                                    ))
        out = widgets.Output()
        display(b1, out)
        def on_button_clicked(_):
            with out:
                clear_output()
                self.check()
        b1.on_click(on_button_clicked)

    def display_buttons(self):
        if hasattr(self, 'check'):
                self.check_button()
        if hasattr(self, 'hint'):
            for i in range(1, len(self.problem.hints) + 1):
                self.hint_button(i)
        if hasattr(self, 'solution'):
                self.sol_button()

    ##### TO BE REVIEWED #######################################
    # This implementation is better but we have problems with the @display : it shows the message before click
    # def display_buttons(self):
    #     if hasattr(self, 'check'):
    #             self.flex_button(desc='Check', color=colors.WARN, obj=self.check())
    #     if hasattr(self, 'hint'):
    #         for i in range(1, len(self.problem.hints) + 1):
    #             self.flex_button(desc=f'Hint {i}', color=colors.HINT, obj=self.hint(i))
    #     if hasattr(self, 'solution'):
    #             self.flex_button(desc='Solution', color=colors.SOLUTION, obj=self.solution())

    # @staticmethod
    # def flex_button(desc, color, obj):
    #     b1 = widgets.Button(description=desc, 
    #                         style=dict( button_color = color,
    #                                     font_style='italic',
    #                                     font_weight='bold'
    #                                 ))
    #     out = widgets.Output()
    #     display(b1, out)
    #     def on_button_clicked(_):
    #         # "linking function with output"
    #         with out:
    #             clear_output()
    #             # what happens when we press the button
    #             obj
    #     # linking button and function together using a button's method
    #     b1.on_click(on_button_clicked)