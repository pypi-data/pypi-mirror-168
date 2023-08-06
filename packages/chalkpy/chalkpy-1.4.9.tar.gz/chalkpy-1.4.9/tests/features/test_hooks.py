import unittest

from chalk.features import after_all, before_all
from chalk.features.hooks import Hook


@before_all
def simple_hook_init():
    return 4


@after_all
def simple_hook_teardown():
    return 5


@after_all(environment="hello")
def env_after_all():
    return 6


@before_all(environment=["hello", "itsme"])
def env_before_all():
    return 5


class Client:
    init = False


client = Client()
client2 = Client()


@before_all(environment="my-special-env")
def setup_env():
    client.init = True


@before_all(environment="my-special-env-2")
def setup_env():
    client2.init = True


class HookTestCase(unittest.TestCase):
    def test_hooks_callable(self):
        self.assertEqual(simple_hook_init(), 4)
        self.assertEqual(simple_hook_init.environment, None)

        self.assertEqual(simple_hook_teardown(), 5)
        self.assertEqual(simple_hook_teardown.environment, None)

    def test_hook_environments(self):
        self.assertEqual(env_before_all(), 5)
        self.assertEqual(env_before_all.environment, ["hello", "itsme"])

        self.assertEqual(env_after_all(), 6)
        self.assertEqual(env_after_all.environment, ["hello"])

    def run_all(self):
        self.assertEqual(client.init, False)
        self.assertEqual(client2.init, False)
        Hook.run_all_before_all("my-special-env")
        self.assertEqual(client.init, True)
        self.assertEqual(client2.init, True)


if __name__ == "__main__":
    unittest.main()
