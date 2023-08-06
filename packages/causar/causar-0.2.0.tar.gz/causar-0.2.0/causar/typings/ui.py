from typing import Union, TypeVar, Any, Sequence

import disnake

MessageUIComponent = Union[disnake.ui.Button[Any], disnake.ui.Select[Any]]
ModalUIComponent = disnake.ui.TextInput
UIComponentT = TypeVar("UIComponentT", bound=disnake.ui.WrappedComponent)
StrictUIComponentT = TypeVar("StrictUIComponentT", MessageUIComponent, ModalUIComponent)
Components = Union[
    "ActionRow[UIComponentT]",
    UIComponentT,
    Sequence[Union["ActionRow[UIComponentT]", UIComponentT, Sequence[UIComponentT]]],
]
