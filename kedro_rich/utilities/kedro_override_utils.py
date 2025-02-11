"""This module provides methods which we use to override default Kedro methods"""
# pylint: disable=protected-access
from typing import Any, Optional, Set

from kedro.io.core import AbstractVersionedDataSet, Version


def node_str_override(self) -> str:
    """This method rich-ifies the node.__str__ method"""

    def _drop_namespaces(xset: Set[str]) -> Optional[Set]:
        """This method cleans up the namesapces"""
        split = {x.split(".")[-1] for x in xset}
        if split:
            return split
        return None

    func_name = f"[magenta]𝑓𝑥 {self._func_name}([/]"
    inputs = _drop_namespaces(self.inputs)
    bridge = "[magenta])[/] [cyan]➡[/] "
    outputs = _drop_namespaces(self.outputs)
    return f"{func_name}{inputs}{bridge}{outputs}"


def catalog_load_override(self, name: str, version: str = None) -> Any:
    """Loads a registered data set (Rich-ified output).

    Args:
        name: A data set to be loaded.
        version: Optional argument for concrete data version to be loaded.
            Works only with versioned datasets.

    Returns:
        The loaded data as configured.

    Raises:
        DataSetNotFoundError: When a data set with the given name
            has not yet been registered.

    Example:
    ::

        >>> from kedro.io import DataCatalog
        >>> from kedro.extras.datasets.pandas import CSVDataSet
        >>>
        >>> cars = CSVDataSet(filepath="cars.csv",
        >>>                   load_args=None,
        >>>                   save_args={"index": False})
        >>> io = DataCatalog(data_sets={'cars': cars})
        >>>
        >>> df = io.load("cars")
    """
    load_version = Version(version, None) if version else None
    dataset = self._get_dataset(name, version=load_version)

    self._logger.info(
        "Loading data from [bright_blue]%s[/] ([bright_blue][b]%s[/][/])...",
        name,
        type(dataset).__name__,
    )

    func = self._get_transformed_dataset_function(name, "load", dataset)
    result = func()

    version = (
        dataset.resolve_load_version()
        if isinstance(dataset, AbstractVersionedDataSet)
        else None
    )

    # Log only if versioning is enabled for the data set
    if self._journal and version:
        self._journal.log_catalog(name, "load", version)
    return result


def catalog_save_override(self, name: str, data: Any) -> None:
    """Save data to a registered data set.

    Args:
        name: A data set to be saved to.
        data: A data object to be saved as configured in the registered
            data set.

    Raises:
        DataSetNotFoundError: When a data set with the given name
            has not yet been registered.

    Example:
    ::

        >>> import pandas as pd
        >>>
        >>> from kedro.extras.datasets.pandas import CSVDataSet
        >>>
        >>> cars = CSVDataSet(filepath="cars.csv",
        >>>                   load_args=None,
        >>>                   save_args={"index": False})
        >>> io = DataCatalog(data_sets={'cars': cars})
        >>>
        >>> df = pd.DataFrame({'col1': [1, 2],
        >>>                    'col2': [4, 5],
        >>>                    'col3': [5, 6]})
        >>> io.save("cars", df)
    """
    dataset = self._get_dataset(name)

    self._logger.info(
        "Saving data to [bright_blue]%s[/] ([bright_blue][b]%s[/][/])...",
        name,
        type(dataset).__name__,
    )

    func = self._get_transformed_dataset_function(name, "save", dataset)
    func(data)

    version = (
        dataset.resolve_save_version()
        if isinstance(dataset, AbstractVersionedDataSet)
        else None
    )

    # Log only if versioning is enabled for the data set
    if self._journal and version:
        self._journal.log_catalog(name, "save", version)
