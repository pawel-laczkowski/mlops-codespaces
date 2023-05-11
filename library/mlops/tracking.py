import requests
from contextlib import contextmanager
from mlops.config.config import settings
from mlops.src.iteration import Iteration
from mlops.exceptions.tracking import project_id_is_none_exception, experiment_id_is_none_exception, \
    failed_to_set_active_project_exception, failed_to_set_active_experiment_exception, request_failed_execption
from typing import ContextManager


def get_project(project_id: str = None) -> dict:
    """
    Function for getting projects from mlops server

    Args:
        project_id: Id od the desired project, that will be retrieved from mlops app

    Returns:
        project: json data of the project
    """
    project_id = settings.active_project_id if not project_id else project_id

    if project_id is None:
        raise project_id_is_none_exception()

    app_response = requests.get(f"{settings.url}/projects/{project_id}")
    response_json = app_response.json()

    if app_response.status_code == 200:
        return response_json
    else:
        raise request_failed_execption(app_response)


def create_project(title: str, description: str = None,
                   status: str = 'not_started', archived: bool = False) -> dict:
    """
    Function for creating mlops projects

    Args:
        title: Title of the created project
        description: Description of the created project (optional)
        status: Status of the created project (optional)
        archived: Archived status of the created project (optional)

    Returns:
        project: JSON data of the created project
    """
    data = {
        "title": title,
        "description": description,
        "status": status,
        "archived": archived
    }

    app_response = requests.post(f"{settings.url}/projects/", json=data)
    response_json = app_response.json()

    if app_response.status_code == 201:
        return response_json
    else:
        raise request_failed_execption(app_response)


def set_active_project(project_id: str) -> str:
    """
    Function for setting active project

    Args:
        project_id: Id of the project, that will be set as active

    Returns:
        project: JSON data of the active project
    """
    try:
        project = get_project(project_id)
    except Exception as e:
        raise failed_to_set_active_project_exception(e)

    settings.change_active_project(project_id)

    return f"Active project set to: {settings.active_project_id}"


def get_experiment(experiment_id: str = None, project_id: str = None) -> dict:
    """
    Function for getting projects from mlops server

    Args:
        experiment_id: Id of the experiment, that will be retrieved from mlops app
        project_id: Id of the project, that the experiment comes from (optional)

    Returns:
        experiment: json data of the experiment
    """
    experiment_id = settings.active_experiment_id if not experiment_id else experiment_id
    project_id = settings.active_project_id if not project_id else project_id

    if project_id is None:
        raise project_id_is_none_exception()
    if experiment_id is None:
        raise experiment_id_is_none_exception()

    app_response = requests.get(f"{settings.url}/projects/{project_id}/experiments/{experiment_id}")
    response_json = app_response.json()

    if app_response.status_code == 200:
        experiment = app_response.json()
        return experiment
    else:
        raise request_failed_execption(app_response)


def create_experiment(name: str, description: str = None,
                      project_id: str = None) -> dict:
    """
    Function for creating mlops experiments

    Args:
        name: Name of the created experiment
        description: Description of the created experiment (optional)
        project_id: Id of the project, that the experiment comes from (optional)

    Returns:
        experiment: json data of the created experiment
    """
    project_id = settings.active_project_id if not project_id else project_id

    if project_id is None:
        raise project_id_is_none_exception()

    data = {
        "name": name,
        "description": description,
    }

    app_response = requests.post(f"{settings.url}/projects/{project_id}/experiments/", json=data)
    response_json = app_response.json()

    if app_response.status_code == 201:
        return response_json
    else:
        raise request_failed_execption(app_response)


def set_active_experiment(experiment_id: str) -> str:
    """
    Function for setting active experiment

    Args:
        experiment_id: Id of the experiment, that will be set as active

    Returns:
        experiment: json data of the active experiment
    """
    try:
        experiment = get_experiment(experiment_id, settings.active_project_id)
    except Exception as e:
        raise failed_to_set_active_experiment_exception(e)

    settings.change_active_experiment(experiment_id)
    return f"Active experiment set to: {settings.active_experiment_id}"


@contextmanager
def start_iteration(iteration_name: str, project_id: str = None,
                    experiment_id: str = None) -> ContextManager[Iteration]:
    """
    Function for creating mlops iteration

    Args:
        iteration_name: name of the created iteration
        project_id: if passed id of the project, else active project_id from settings
        experiment_id: if passed id of the experiment, else active experiment_id from settings

    Returns:
        Iteration.end_iteration() method output
    """

    project_id = settings.active_project_id if not project_id else project_id
    experiment_id = settings.active_experiment_id if not experiment_id else experiment_id

    if project_id is None:
        raise project_id_is_none_exception()
    if experiment_id is None:
        raise experiment_id_is_none_exception()

    iteration = Iteration(
        iteration_name=iteration_name,
        project_id=project_id,
        experiment_id=experiment_id
    )
    try:
        yield iteration
    finally:
        iteration.end_iteration()