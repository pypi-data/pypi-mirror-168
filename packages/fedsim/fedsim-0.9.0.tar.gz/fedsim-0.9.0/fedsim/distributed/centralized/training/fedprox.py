r"""
FedProx
-------
"""
from functools import partial

from torch.nn.utils import parameters_to_vector

from fedsim.local.training.step_closures import default_step_closure
from fedsim.utils import vector_to_parameters_like
from fedsim.utils import vectorize_module

from .fedavg import FedAvg


class FedProx(FedAvg):
    r"""Implements FedProx algorithm for centralized FL.

    For further details regarding the algorithm we refer to `Federated Optimization in
    Heterogeneous Networks`_.

    Args:
        data_manager (``distributed.data_management.DataManager``): data manager
        metric_logger (``logall.Logger``): metric logger for tracking.
        num_clients (int): number of clients
        sample_scheme (``str``): mode of sampling clients. Options are ``'uniform'``
            and ``'sequential'``
        sample_rate (``float``): rate of sampling clients
        model_def (``torch.Module``): definition of for constructing the model
        epochs (``int``): number of local epochs
        criterion_def (``Callable``): loss function defining local objective
        optimizer_def (``Callable``): derfintion of server optimizer
        local_optimizer_def (``Callable``): defintoin of local optimizer
        lr_scheduler_def (``Callable``): definition of lr scheduler of server optimizer.
        local_lr_scheduler_def (``Callable``): definition of lr scheduler of local
            optimizer
        r2r_local_lr_scheduler_def (``Callable``): definition to schedule lr that is
            delivered to the clients at each round (deterimined init lr of the
            client optimizer)
        batch_size (int): batch size of the local trianing
        test_batch_size (int): inference time batch size
        device (str): cpu, cuda, or gpu number
        mu (float): FedProx's :math:`\mu` hyper-parameter for local regularization

    .. note::
        definition of
            * learning rate schedulers, could be any of the ones defined at
                ``torch.optim.lr_scheduler`` or any other that implements step and
                get_last_lr methods._schedulers``.
            * optimizers, could be any ``torch.optim.Optimizer``.
            * model, could be any ``torch.Module``.
            * criterion, could be any ``fedsim.scores.Score``.

    .. _Federated Optimization in Heterogeneous Networks:
        https://arxiv.org/abs/1812.06127
    """

    def init(server_storage, *args, **kwrag):
        default_mu = 0.0001
        FedAvg.init(server_storage)
        server_storage.write("mu", kwrag.get("mu", default_mu))

    def send_to_client(server_storage, client_id):
        server_msg = FedAvg.send_to_client(server_storage, client_id)
        server_msg["mu"] = server_storage.read("mu")
        return server_msg

    def send_to_server(
        id,
        rounds,
        storage,
        datasets,
        train_split_name,
        scores,
        epochs,
        criterion,
        train_batch_size,
        inference_batch_size,
        optimizer_def,
        lr_scheduler_def=None,
        device="cuda",
        ctx=None,
        step_closure=None,
    ):
        model = ctx["model"]
        mu = ctx["mu"]
        params_init = vectorize_module(model, clone=True, detach=True)

        def transform_grads_fn(model):
            params = parameters_to_vector(model.parameters())
            grad_additive = 0.5 * (params - params_init)
            grad_additive_list = vector_to_parameters_like(
                mu * grad_additive, model.parameters()
            )

            for p, g_a in zip(model.parameters(), grad_additive_list):
                p.grad += g_a

        step_closure_ = partial(
            default_step_closure, transform_grads=transform_grads_fn
        )
        return FedAvg.send_to_server(
            id,
            rounds,
            storage,
            datasets,
            train_split_name,
            scores,
            epochs,
            criterion,
            train_batch_size,
            inference_batch_size,
            optimizer_def,
            lr_scheduler_def,
            device,
            ctx,
            step_closure=step_closure_,
        )
