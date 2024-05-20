"""Evaluate MDRS against the validation set"""

import sys
import logging

import torch

sys.path.insert(0,'pytorch/')
import main
from mean_teacher.cli import parse_dict_args
from mean_teacher.run_context import RunContext


LOG = logging.getLogger('runner')


def parameters():
    defaults = {
        # Technical details
        'workers': 20,
        'checkpoint_epochs': 1,
        'evaluation_epochs': 1,

        # Data
        'dataset': 'mdrs',
        'exclude_unlabeled': False,

        # Data sampling
        'base_batch_size': 32,
        'base_labeled_batch_size': 16,

        # Architecture
        'arch': 'resnext152',
        'ema_decay': .9997,

        # Costs
        'consistency_type': 'kl',
        'consistency': 10.0,
        'consistency_rampup': 5,
        'logit_distance_cost': 0.01,
        'weight_decay': 5e-5,

        # Optimization
        'epochs': 60,
        'lr_rampdown_epochs': 75,
        'lr_rampup': 2,
        'initial_lr': 0.1,
        'base_lr': 0.025,
        'nesterov': True,
    }

    for data_seed in range(10, 12):
        yield {
            **defaults,
            'title': 'mean teacher r-152 eval',
            'data_seed': 0
        }


def run(title, base_batch_size, base_labeled_batch_size, base_lr, data_seed, **kwargs):
    LOG.info('run title: %s', title)
    ngpu = torch.cuda.device_count()
    adapted_args = {
        'batch_size': base_batch_size * ngpu,
        'labeled_batch_size': base_labeled_batch_size * ngpu,
        'lr': base_lr * ngpu,
        'labels': 'bypass',
    }
    context = RunContext(__file__, data_seed)
    main.args = parse_dict_args(**adapted_args, **kwargs)
    main.main(context)


if __name__ == "__main__":
    for run_params in parameters():
        run(**run_params)
