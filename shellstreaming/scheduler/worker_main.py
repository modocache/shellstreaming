# -*- coding: utf-8 -*-
"""
    shellstreaming.scheduler.main
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :synopsis: Provides scheduler's main loop
"""
import time
from importlib import import_module
from shellstreaming.worker import worker_struct as ws


def sched_loop(
    job_graph,
    sched_module_name,
    reschedule_interval_sec,
):
    """Scheduler main loop of stream processing

    Loop of 1-3.

    1. calculate next job placement from current job placement, machine resource usage, ...
    2. request each worker next job placement
    3. sleep
    """
    sched_module = import_module(sched_module_name)
    while True:
        sched_module.update_instances(job_graph, ws.REGISTERED_JOBS, ws.job_instances)
        time.sleep(0.1)  # [fix] - consider sleep time
