# %%
import numpy as np
from matplotlib import pyplot as plt
# %%
%load_ext autoreload
%autoreload 2
from paramga.run import Runner as GRunner
# %%


def state():
    return {
        "foo": 10,
        "bar": 360,
    }

def conf():
    return {
        "foo": {
            "type": "number",
            "min": 1,
            "max": 80,
            "step": 8,
        }
    }

def model():
    def model(params, data):
        return sum(data) * params['foo']
    return model

def loss_function():
    def loss_function(output, params):
        return abs(params['bar'] - output)
    return loss_function

def data():
    return [1, 2, 3, 3]

def best_params():
    return {
        "foo": 40,
        "bar": 360,
    }

runner = GRunner(
    state(),
    conf(),
    model(),
    loss_function(),
    data(),
    max_iterations=100,
    tolerance=0.05,
)
# iteration_state = runner.run().iteration_state
# assert 100 > iteration_state.iterations > 5
# assert iteration_state.best_parameters == best_params()
# iteration_state

# %%
# runner.reset_state()
# for istate in iter(runner):
#     print(istate)

# print('complete')
# print(istate.iterations)

# %%

# %%
runner.store_iterations().reset_state().run()
runner.plot()

# error_values = [s.loss for s in runner.history]
# plt.plot(error_values)
# %%
runner.plot_param('foo')
pass

# %%

# %%
key = 'foo'
values = np.array([[p[key] for p in s.parameters] for s in runner.history])
values.shape


# %%
runner.iteration_state.parameters
# %%
last_params = runner.history[0].parameters
last_params
foo_vals = [p['foo'] for p in last_params]
error_vals = [model()(p, data()) for p in last_params]
plt.scatter(foo_vals, error_vals)
# model()(runner.history[-1].parameters[-1], data())

# %%
def state():
    return {
        "foo": 10,
        "bar": 900,
    }

def conf():
    return {
        "foo": {
            "type": "float",
            "min": 1,
            "max": 200,
            "step": 0.2,
        },
        "bar": {
            "type": "number",
            "min": 400,
            "max": 1000,
            "step": 100,
        }
    }

runner = GRunner(
    state(),
    conf(),
    model(),
    loss_function(),
    data(),
    max_iterations=100,
    tolerance=0.001,
)
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(20,10), dpi=75)
for i in range(10):
    runner.seed=i
    runner.mutation_conf['foo']['step'] = i
    runner.store_iterations().reset_state().run()
    print(runner.iteration_state.lowest_loss)
    runner.plot_param('foo', ax=axs[0][0], fig=fig)
    runner.plot(ax=axs[1][0], fig=fig)
    runner.plot_param('bar', ax=axs[0][1], fig=fig)
    runner.plot(ax=axs[1][1], fig=fig)
# %%

runner.plot_param_compare('foo', 'bar')