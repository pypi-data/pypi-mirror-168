import random
import numpy as np
from dataclasses import asdict
from datetime import datetime
from functools import partial
from typing import Any, Callable, Dict, Iterator, List, NamedTuple
from multiprocessing import Process, Queue

from paramga.plot import (
    plot_loss,
    plot_observed_compare,
    plot_param,
    plot_param_compare,
)

from .crossover import param_crossover
from .mutation import mutate_param_state

from .iteration_state import IterationState

Parameters = dict
ModelOutput = np.ndarray
ModelData = np.ndarray


def get_outputs(func, input_args, input_kwargs):
    return np.array([func(*args, **input_kwargs) for args in input_args])


def get_outputs_parallel(
    func: Callable[[Parameters, ModelData], ModelOutput],
    input_args: List[List[Any]],
    func_kwargs: dict,
    TIMEOUT: float = 100,
) -> ModelOutput:
    """Run the model in parallel

    Parameters
    ----------
    func : Callable[[Parameters, ModelData], ModelOutput]
        model function.
    input_args : List[List[Any]]
        list of dictionaries of arguments for model run
    func_kwargs: dict
        Additional kwargs to pass to model func

    Returns
    -------
    List[ModelOutput]
        The outputs of the Model for each run

    """
    Qu = None
    procs = []
    population=len(input_args)
    try:
        Qu = Queue(maxsize=population)

        def _func(i, args, kwargs):
            # We use a middleware func to link the function outputs to the population index
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                return i, e
            return i, result

        def q_wrap(q, args, kwargs):
            # Add the output of _func to the queue to be collected later
            q.put(_func(*args, kwargs))

        outputs = [None for _ in range(population)]

        # ==== for each run in population we create a process containing a queue writer.
        # NOTE: Args here is (i, model_args)
        for args in enumerate(input_args):
            # Starting Process
            p = Process(target=q_wrap, args=([Qu, args, func_kwargs]))
            procs.append(p)
            p.start()

        # # ==== wait for all processes to complete
        for p in procs:
            p.join(TIMEOUT)

        # # ==== wait for all processes to complete ALT IMPLEMENTATION
        # # Solution from https://stackoverflow.com/questions/26063877/python-multiprocessing-module-join-processes-with-timeout
        # DELAY = .1
        # start = time.time()
        # while time.time() - start <= TIMEOUT:
        #     print("Checking processes")
        #     if not any([p.is_alive() for p in procs]):
        #         # All the processes are done, break now.
        #         break

        #     time.sleep(DELAY)  # Just to avoid hogging the CPU
        # else:
        #     # We only enter this if we didn't 'break' above.
        #     print("timed out, killing all processes")
        #     for p in procs:
        #         p.terminate()
        #         p.join()
        # ===================================================

        # ==== Each process should have written the output of the model to the queue(Qu)
        for p in procs:
            i, res = Qu.get(timeout=.1)
            if isinstance(res, Exception):
                raise res
            outputs[i] = res
            p.close()

    except Exception as e:
        try:
            for p in procs:
                try:
                    print(p.exitcode)
                    p.terminate()
                    p.join(.1)
                except:
                    p.kill()
        except:
            # TODO: Should warn about fail to teardown multi processes
            pass
        print(e)
        raise Exception("Model run multiprocessing failed: {}".format(str(e)))
    return np.array(outputs)


class Logger:
    def __init__(self, log_level):
        self.log_level = log_level

    def log(self, message):
        if self.log_level > 0:
            print(message)


def get_initial_params(
    param_base: dict,
    mutation_conf: dict,
    population: int,
) -> dict:
    return [
        mutate_param_state(param_base, mutation_conf) for _ in range(population)
    ]


def setup_state(
    param_base: dict,
    mutation_conf: dict,
    population: int,
) -> IterationState:
    initial_parameters = get_initial_params(
        param_base,
        mutation_conf,
        population,
    )
    iteration_state = IterationState(
        parameters=initial_parameters,
        best_parameters=initial_parameters[0],
    )
    return iteration_state


def iteration(
    iteration_state: IterationState,
    func: Callable[[Parameters, ModelData], ModelOutput],
    loss_func: Callable[[ModelOutput, Parameters], float],
    population: int,
    mutation_conf: List[dict],
    input_data: np.ndarray=None,
    process_outputs: Callable[[np.ndarray], np.ndarray] = None,
    parallel=False,
    func_kwargs: dict=None,
    TIMEOUT: float = 100,
) -> IterationState:
    """Run paramga iteration.

    Parameters
    ----------
    iteration_state : IterationState
        The input iteration state
    func : Callable
        The model function to call with the parameters and data
    loss_func : Callable
        The loss function to run on the model outputs. Should return value between 0-1.
    population : int
        The number of parameter variations to call the model with.
    mutation_conf : List[dict]
        The configuration of parameter mutation.
    input_data : [type], optional
        The input data to pass to the model, by default None
    process_outputs : Callable[[np.ndarray], np.ndarray], optional
        Additional processing of output data before running loss function, by default None
    parallel : bool, optional
        If true will run populations in parallel, by default False
    func_kwargs: dict, optional
        Additional kwargs to pass to model func

    Returns
    -------
    IterationState
        Updated iteration state


    """
    parameters = iteration_state.parameters
    lowest_loss = iteration_state.lowest_loss
    best_parameters = iteration_state.best_parameters
    _func_kwargs = func_kwargs or {}

    # Run and get losses
    input_args = [(params, input_data) for params in parameters]

    run_func = partial(get_outputs_parallel, TIMEOUT=TIMEOUT) if parallel else get_outputs
    outputs = run_func(func, input_args, _func_kwargs)
    outputs_processed = np.array([process_outputs(o)
                                 for o in outputs]) if process_outputs else outputs

    losses = [loss_func(o, p) for p, o in zip(parameters, outputs_processed)]
    curr_min_loss = min(losses)

    # Sort parameters
    parameters_index_sorted = list(
        map(lambda x: x[0], sorted(enumerate(losses), key=lambda si: si[1])))

    # Set new best parameters if loss is lowest
    if curr_min_loss < lowest_loss:
        best_parameters = parameters[parameters_index_sorted[0]]
        lowest_loss = curr_min_loss
    else:
        # If min loss is not lower than lowest loss then add best parameters back to population
        parameters = parameters + [best_parameters]
        losses = losses + [lowest_loss]

    # Choose next parameter pairs using probalistic choice based on loss values
    loss_vals = 1 - (losses - np.min(losses)) / \
        np.ptp(losses) if np.ptp(losses) > 0 else np.ones(len(parameters))
    loss_ratios = loss_vals / sum(loss_vals)

    try:
        choices_population = [np.random.choice(
            len(parameters), 2, p=loss_ratios) for _ in range(population)]
    except ValueError as e:
        print(loss_ratios)
        print(parameters)
        raise e

    # We choose parameter pairs from the population with higher scoring params
    # being more likely to be picked
    crossed_parameters = [param_crossover(*[parameters[i] for i in choices])
                          for choices in choices_population]

    mutated_new_parameters = [mutate_param_state(
        param, mutation_conf) for param in crossed_parameters]

    return IterationState(
        mutated_new_parameters,
        best_parameters,
        curr_min_loss,
        lowest_loss,
        iteration_state.iterations + 1,
    )


def run_iterator(
    param_base: List[Dict],
    mutation_conf: dict,
    func: Callable[[Parameters], float],
    loss_func: Callable[[np.ndarray], float],
    input_data: any,
    process_outputs: Callable[[np.ndarray], np.ndarray] = None,
    population: int = 8,
    tolerance: float = None,
    max_iterations: int = 1000,
    verbose: bool = False,
    parallel: bool = False,
) -> Iterator[IterationState]:
    """Genetic algorithm iterator.

    Yields the next set of params and losses.

    Parameters
    ----------
    param_base : Dict
        The initial parameters for running the model.
    mutation_conf : Dict
        The configuration for mutating the parameters at each step.
    func : Callable[[Parameters, ModelData], ModelOutput]
        The model function to be called with the parameters and data.
    loss_func : Callable[[ModelOutput, Parameters], float]
        The loss function to be called with the model output
    input_data : ModelData
        Input data for the model.
    process_outputs: Callable[[np.ndarray], np.ndarray] = None,
        Function to process outputs before running loss function
    population : int, optional
        The population size for optimization algorithm, by default 8
    tolerance : float, optional
        The tolerance of the optimization algorithm, by default None
    max_iterations : int, optional
        The maximum iterations of the optimization algorithm, by default 1000
    verbose : bool, optional
        Output verbose logs, by default False
    parallel : bool, optional
        Run iterations in parallel, by default False

    Yields
    -------
    IterationState
        The iteration state.

    """
    iteration_state = setup_state(
        param_base,
        mutation_conf,
        population,
    )

    logger = Logger(1 if verbose else 0)

    logger.log("==== Starting ====")
    while iteration_state.iterations < max_iterations and (tolerance is None or iteration_state.loss > tolerance):
        logger.log(
            f"========= Running iteration: {iteration_state.iterations}. Curr loss is {iteration_state.loss}")
        iteration_state = iteration(
            iteration_state,
            func,
            loss_func,
            population,
            mutation_conf,
            input_data=input_data,
            process_outputs=process_outputs,
            parallel=parallel,
        )
        yield iteration_state
    iteration_state.complete = True
    logger.log("===== Complete ======")
    yield iteration_state


def run(
    param_base: List[Dict],
    mutation_conf: dict,
    func: Callable[[Parameters], float],
    loss_func: Callable[[np.ndarray], float],
    input_data: any,
    process_outputs: Callable[[np.ndarray], np.ndarray] = None,
    population: int = 8,
    tolerance: float = None,
    max_iterations: int = 1000,
    verbose: bool = False,
    parallel: bool = False,
) -> IterationState:
    """Wrapper for running the iterator for a set number of iterations.

    Parameters
    ----------
    param_base : Dict
        The initial parameters for running the model.
    mutation_conf : Dict
        The configuration for mutating the parameters at each step.
    func : Callable[[Parameters, ModelData], ModelOutput]
        The model function to be called with the parameters and data.
    loss_func : Callable[[ModelOutput, Parameters], float]
        The loss function to be called with the model output
    input_data : ModelData
        Input data for the model.
    process_outputs : Callable[[ModelOutput], ModelOutput], optional
            Optional function to call on model output before loss function, by default None
    population : int, optional
        [description], by default 8
    tolerance : float, optional
        The tolerance of the optimization algorithm, by default None
    max_iterations : int, optional
        The maximum iterations of the optimization algorithm, by default 1000
    verbose : bool, optional
        Output verbose logs, by default False
    parallel : bool, optional
        Run iterations in parallel, by default False

    Returns
    -------
    IterationState
        IterationState after run.

    """
    for iteration_state in run_iterator(
        param_base,
        mutation_conf,
        func,
        loss_func,
        input_data,
        process_outputs,
        population,
        tolerance,
        max_iterations,
        verbose,
        parallel,
    ):
        if iteration_state.complete:
            return iteration_state
    return iteration_state



class RunStats(NamedTuple):
    total_time: datetime


class Runner:
    """Simple wrapper around run function for class functionality."""

    def __init__(
        self,
        param_base: Dict,
        mutation_conf: Dict,
        func: Callable[[Parameters, ModelData], ModelOutput],
        loss_func: Callable[[ModelOutput, Parameters], float],
        input_data: ModelData,
        func_kwargs: dict = None,
        population: int = 8,
        process_outputs: Callable[[ModelOutput], ModelOutput] = None,
        tolerance: float = None,
        max_iterations: int = 1000,
        verbose: bool = False,
        parallel: bool = False,
        seed: int = 0,
        timeout: float = 100,
    ):
        """Create Runner instance.

        Parameters
        ----------
        param_base : Dict
            The initial parameters for running the model.
        mutation_conf : Dict
            The configuration for mutating the parameters at each step.
        func : Callable[[Parameters, ModelData], ModelOutput]
            The model function to be called with the parameters and data.
        loss_func : Callable[[ModelOutput, Parameters], float]
            The loss function to be called with the model output
        input_data : ModelData
            Input data for the model.
        func_kwargs: dict, optional
            The common kwargs to pass to the model func (Helps with parallel)
        population : int, optional
            The population size for optimization algorithm, by default 8
        process_outputs : Callable[[ModelOutput], ModelOutput], optional
            Optional function to call on model output before loss function, by default None
        tolerance : float, optional
            The tolerance of the optimization algorithm, by default None
        max_iterations : int, optional
            The maximum iterations of the optimization algorithm, by default 1000
        verbose : bool, optional
            Output verbose logs, by default False
        parallel : bool, optional
            Run iterations in parallel, by default False
        seed : int, optional
            The random seed to use, by default 0
        timeout: float
            Timeout for each parallel model run.

        """
        self.param_base = param_base
        self.mutation_conf = mutation_conf
        self.func = func
        self.loss_func = loss_func
        self.input_data = input_data
        self.func_kwargs = func_kwargs or {}
        self.population = population
        self.process_outputs = process_outputs
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.parallel = parallel
        self.timeout = timeout
        self.seed = seed
        self.stats = RunStats(None)

        self.history = []
        self._store_iterations = False

        self.logger = Logger(1 if verbose else 0)

        self.reset_state()

    def reset_state(self):
        random.seed(self.seed)
        np.random.seed(self.seed)
        self.initial_parameters = get_initial_params(
            self.param_base,
            self.mutation_conf,
            self.population,
        )
        self.iteration_state = setup_state(
            self.param_base,
            self.mutation_conf,
            self.population,
        )
        self.history = [self.iteration_state]
        self.stats = RunStats(None)
        return self

    def __iter__(self):
        def _inner():
            while self.iteration_state.iterations < self.max_iterations \
                    and (self.tolerance is None or self.iteration_state.loss > self.tolerance):
                yield next(self)
        return _inner()

    def __next__(self):
        new_state = iteration(
            iteration_state=self.iteration_state,
            func=self.func,
            loss_func=self.loss_func,
            population=self.population,
            mutation_conf=self.mutation_conf,
            input_data=self.input_data,
            process_outputs=self.process_outputs,
            parallel=self.parallel,
            func_kwargs=self.func_kwargs,
            TIMEOUT=self.timeout,
        )
        self.iteration_state = new_state
        if self._store_iterations:
            self.history.append(new_state)
        return new_state

    def info(self):
        return f"""Paramga Instance:\n
# Config
population: {self.population}
tolerance: {self.tolerance}
max_iterations: {self.max_iterations}
verbose: {self.verbose}
parallel: {self.parallel}
timeout: {self.timeout}

# State
best_parameters: {self.iteration_state.best_parameters}
loss: {self.iteration_state.loss}
lowest_loss: {self.iteration_state.lowest_loss}
iterations: {self.iteration_state.iterations}
complete: {self.iteration_state.complete}

"""

    def __str__(self):
        return self.info()

    def store_iterations(self, v: bool = True):
        self._store_iterations = v
        return self

    def run(self):
        start_time = datetime.now()
        while self.iteration_state.iterations < self.max_iterations \
                and (self.tolerance is None or self.iteration_state.lowest_loss > self.tolerance):
            next(self)
        end_time = datetime.now()
        self.stats = RunStats(end_time - start_time)
        return self

    def bootstrap_run(self):
        raise NotImplementedError("Bootstrap runs not implemented")
        # dataset_number = #column with dataset names#.size
        # bootstrap_samples = generate_bootstrap_samples(dataset_number, bootstrap_sample_number)
        # OOB_error = []
        # best_parameters_per_sample = []

        # for i in range(bootstrap_sample_number):
        #     traing_set_numbers = bootstrap_samples[i,]
        #     #Get datasets in training set
        #     #Calibrate model on bootstrap sample i
        #     testing_set_numbers = generate_out_of_bag_samples(training_set_numbers)
        #     #Get datasets in test set
        #     #Test calibrated parameters on data not included in bootstrap sample i=
        #     state_out = self.run(training_set)
        #     model_error = self.func(state_out.best_parameters, test_data)
        #     best_parameters_per_sample.append(state_out.best_parameters)
        #     # model_error = #Error from testing calibrated parameters on data not inluded in bootstrap sample i
        #     OOB_error = np.append(OOB_error, [model_error], 0)

        # # return All bootstrap_sample_number parameter sets, model weightings, OOB_error
        # # TODO: Calculate the weighted average params

    def get_best_model_output(self):
        """Run the model on the best parameters from the iteration state."""
        return self.func(self.iteration_state.best_parameters, self.input_data, **self.func_kwargs)

    def get_initial_model_output(self):
        """Run the model on the best parameters from the iteration state."""
        return self.func(self.param_base, self.input_data, **self.func_kwargs)

    def iteration_state_dump(self):
        return asdict(self.iteration_state)

    def plot(self, key='loss', ax=None, fig=None):
        if len(self.history) == 0:
            raise ValueError('Must run with store_iteraions on to create plots')

        if key == 'loss':
            loss_values = [s.lowest_loss for s in self.history[1:]]
            return plot_loss(loss_values, ax=ax, fig=fig)
        else:
            raise ValueError(f'{key} is invalid key')

    def plot_param(self, key, ax=None, fig=None):
        if len(self.history) == 0:
            raise ValueError('Must run with store_iteraions on to create plots')

        param_values = np.array(
            # [[p[key] for p in self.initial_parameters]] +
            [[p[key] for p in s.parameters] for s in self.history[:-1]])
        best_values = np.array([s.best_parameters[key] for s in self.history[1:]])
        loss_values = [s.lowest_loss for s in self.history[1:]]
        return plot_param(key, param_values, best_values, loss_values, ax=ax, fig=fig)

    def plot_param_compare(self, key_a, key_b, ax=None, fig=None):
        best_values_a = np.array([s.best_parameters[key_a] for s in self.history[1:]])
        best_values_b = np.array([s.best_parameters[key_b] for s in self.history[1:]])
        loss_values = [s.loss for s in self.history[1:]]
        return plot_param_compare(key_a, key_b, best_values_a, best_values_b, loss_values, ax=ax, fig=fig)

    def plot_compare_with_observed(
        self, observed_values, ax=None, fig=None,
    ):
        values = self.func(self.iteration_state.best_parameters, self.input_data, **self.func_kwargs)
        try:
            assert type(observed_values) == np.ndarray
            assert type(values) == np.ndarray
        except:
            raise AssertionError('Observed and model values must by numpy arrays.')
        return plot_observed_compare(
            observed_values,
            values,
            ax=ax,
            fig=fig,
            xlim=(min(observed_values), max(observed_values)),
            ylim=(min(observed_values), max(observed_values)),
        )
