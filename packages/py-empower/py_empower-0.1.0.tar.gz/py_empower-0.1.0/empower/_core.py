import inspect

from ._trait import (
    CallerProxy,
    Trait,
    add_trait_modules_used,
    remove_trait_modules_used,
)


class LoadTraitError(Exception):
    pass


def load_traits(path):
    traits = []
    modules = path.split(".")

    try:
        leaf_module = modules[-1]
        module = __import__(path, fromlist=[leaf_module])

        for trait_name in dir(module):
            if trait_name.startswith("_"):
                continue
            attr = getattr(module, trait_name)
            if inspect.isclass(attr) and Trait in attr.mro():
                traits.append(attr)

    except ModuleNotFoundError as error:
        # maybe path is a trait
        trait_name = leaf_module
        new_path = ".".join(modules[:-1])
        try:
            module = __import__(new_path, fromlist=[trait_name])
        except ModuleNotFoundError:
            raise LoadTraitError(str(error))

        try:
            attr = getattr(module, trait_name)
        except AttributeError as error:
            raise LoadTraitError(str(error))

        if not inspect.isclass(attr) or Trait not in attr.mro():
            raise LoadTraitError(f"{path} must be a Trait")

        traits = [getattr(module, trait_name)]

    traits = set(traits) - set([Trait])

    return traits


def use(path):
    frame = inspect.stack()[1]
    called_module = inspect.getmodule(frame[0])
    if called_module is None:
        module_name = "__main__"
    else:
        module_name = called_module.__name__

    traits = load_traits(path)

    for trait in traits:
        add_trait_modules_used(trait, module_name)


def clean(path):
    frame = inspect.stack()[1]
    called_module = inspect.getmodule(frame[0])
    if called_module is None:
        module_name = "__main__"
    else:
        module_name = called_module.__name__

    traits = load_traits(path)
    for trait in traits:
        remove_trait_modules_used(trait, module_name)


def impl(target_cls):
    """
    with `impl` decorator you can empower your class without create
    a subclass
    """

    def wrapped(trait):
        if not issubclass(trait, Trait):
            raise ValueError(f"{trait} must be a Trait")

        for method_name, method in trait.__dict__.items():
            if method_name.startswith("_"):
                continue
            method = CallerProxy(trait, method)
            setattr(target_cls, method_name, method)

        if target_cls.__doc__ is None:
            target_cls.__doc__ = ""
        doc = f"<Trait: {trait.__name__}>: {trait.__doc__}"
        target_cls.__doc__ += f"\n{doc}"

        add_trait_modules_used(trait, trait.__module__)
        trait.register(target_cls)
        return trait

    return wrapped
