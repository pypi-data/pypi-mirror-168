import inspect
from typing import Any, Callable, Optional, Union

from chalk.features import Cron, Environments, MachineType, Tags
from chalk.features.resolver import OfflineResolver, OnlineResolver, Resolver, offline, online, parse_function
from chalk.utils.duration import ScheduleOptions

__all__ = [
    "online",
    "offline",
    "realtime",
    "batch",
]


def realtime(
    fn: Optional[Callable] = None,
    /,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Optional[Union[ScheduleOptions, Cron]] = None,
    machine_type: Optional[MachineType] = None,
    when: Optional[Any] = None,
):
    """
    :param fn: The function that you're decorating as a resolver.

    :param environment: Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:

            - None (default) - candidate to run in every environment
            - str - run only in this environment
            - list[str] - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments

    :param tags: Tags allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags

    :param cron: You can schedule resolvers to run on a
        pre-determined schedule via the cron argument to resolver
        decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron

    :param machine_type: You can optionally specify that resolvers
        need to run on a machine other than the default. Must be
        configured in your deployment.

    :param when: Like tags, `when` can filter when a resolver
        is eligible to run. Unlike tags, `when` can use feature values,
        so that you can write resolvers like:

            @realtime(when=User.risk_profile == "low" or User.is_employee)
            def resolver_fn(...) -> ...:
                ...

    :return: A callable function! You can unit test resolvers
        as you would unit test any other code.

        Read more at https://docs.chalk.ai/docs/unit-tests
    """
    from .df.ChalkASTParser import ChalkASTParser

    caller_filename = inspect.stack()[1].filename

    def decorator(args, cf=caller_filename):
        parsed = parse_function(args)
        if parsed.fqn in {s.fqn for s in Resolver.registry}:
            raise ValueError(f"Duplicate resolver {parsed.fqn}")
        Resolver.registry.append(
            OnlineResolver(
                filename=cf,
                function_definition=parsed.function_definition,
                fqn=parsed.fqn,
                doc=parsed.doc,
                inputs=parsed.inputs,
                output=parsed.output,
                fn=parsed.function,
                environment=environment,
                tags=tags,
                max_staleness=None,
                cron=cron,
                machine_type=machine_type,
                when=ChalkASTParser.parse_when() if when is not None else None,
            )
        )
        return args

    return decorator(fn) if fn else decorator


def batch(
    fn: Optional[Callable] = None,
    /,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Union[ScheduleOptions, Cron] = None,
    machine_type: Optional[MachineType] = None,
):
    """
    :param fn: The function that you're decorating as a resolver.

    :param environment: Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:

            - None (default) - candidate to run in every environment
            - str - run only in this environment
            - list[str] - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments

    :param tags: Tags allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags

    :param cron: You can schedule resolvers to run on a
        pre-determined schedule via the cron argument to resolver
        decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron

    :param machine_type: You can optionally specify that resolvers
        need to run on a machine other than the default. Must be
        configured in your deployment.

    :return: A callable function! You can unit test resolvers
        as you would unit test any other code.

    Read more at https://docs.chalk.ai/docs/unit-tests
    """

    caller_filename = inspect.stack()[1].filename

    def decorator(args, cf=caller_filename):
        parsed = parse_function(args)
        if parsed.fqn in {s.fqn for s in Resolver.registry}:
            raise ValueError(f"Duplicate resolver {parsed.fqn}")
        Resolver.registry.append(
            OfflineResolver(
                filename=cf,
                function_definition=parsed.function_definition,
                fqn=parsed.fqn,
                doc=parsed.doc,
                inputs=parsed.inputs,
                output=parsed.output,
                fn=parsed.function,
                environment=environment,
                tags=tags,
                max_staleness=None,
                cron=cron,
                machine_type=machine_type,
            )
        )
        return args

    return decorator(fn) if fn else decorator
