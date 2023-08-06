import os.path
from unittest import TestCase

from pandas import DataFrame

from rkt_lib_toolkit import Logger, Config
from rkt_lib_toolkit.ai import QLearning

PKL_FILE = "tests/resources/qlearning/load/load_coverage.pkl"


class TestQLearning(TestCase):
    def test_me_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.me = 'me'
        assert ql.me == 'me'

    def test_me_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        assert ql.me == 'QLearning'

    def test_logger_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.logger = Logger(caller_class=ql.me)
        assert isinstance(ql.logger, Logger)

    def test_logger_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        logger = ql.logger
        assert isinstance(logger, Logger)

    def test_config_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.config = Config()
        assert isinstance(ql.config, Config)

    def test_config_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        config = ql.config
        assert isinstance(config, Config)

    def test_learning_rate_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        original_lr = ql.learning_rate
        ql.learning_rate = 1.0
        assert ql.learning_rate != original_lr

    def test_learning_rate_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        original_lr = ql.learning_rate
        assert ql.learning_rate == original_lr

    def test_discount_factor_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        original_df = ql.discount_factor
        ql.discount_factor = 1.0
        assert ql.discount_factor != original_df

    def test_discount_factor_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        original_df = ql.discount_factor
        assert ql.discount_factor == original_df

    def test_qtable_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        assert isinstance(ql.qtable, DataFrame)

    def test_qtable_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        qtable = ql.qtable
        assert isinstance(qtable, DataFrame)

    def test_previous_state_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.previous_state = 's'
        assert ql.previous_state == 's'

    def test_previous_state_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        assert ql.previous_state == 'start'

    def test_previous_action_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.previous_action = 'a'
        assert ql.previous_action == 'a'

    def test_previous_action_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        assert ql.previous_action == 'do-nothing'

    def test_available_actions_setter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        assert ql.available_actions == ['a', 'b', 'c']

    def test_available_actions_getter(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        actions_list = ql.available_actions
        assert actions_list == ['a', 'b', 'c']

    def test_save(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.save("tests/resources/qlearning/save/save_coverage.pkl")
        assert os.path.exists("tests/resources/qlearning/save/save_coverage.pkl")

    def test_load(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.load(do_load=True, file_to_load=PKL_FILE)
        assert isinstance(ql.qtable, DataFrame)

    def test_choose_action(self):
        ql = QLearning(actions=['a', 'b', 'c'], should_load=True,
                       qtable_file_to_load=PKL_FILE)

        action = ql.choose_action(state='s')
        assert action in ['a', 'b', 'c']

    def test_learn(self):
        ql = QLearning(actions=['a', 'b', 'c'], should_load=True,
                       qtable_file_to_load=PKL_FILE)
        for i in range(2):
            action = ql.choose_action(state=f's{i}')
            ql.learn(state=f's{i}', action=action, reward=1.0)
        assert ql.qtable.index.tolist() == ['s0', 's1']

    def test_check_state_exist(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        ql.check_state_exist(state='s')
        qtable_len = len(ql.qtable.index)
        ql.check_state_exist(state='s')
        qtable2_len = len(ql.qtable.index)
        ql.check_state_exist(state='s1')
        qtable3_len = len(ql.qtable.index)
        assert qtable_len == qtable2_len and qtable_len != qtable3_len

    def test_representation(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        assert ql.__repr__() == f"QLearning(alpha={ql.learning_rate}, gamma={ql.discount_factor})"

    def test_me_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.me = 1

    def test_logger_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.logger = 1

    def test_config_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.config = 1

    def test_learning_rate_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.learning_rate = "0"

    def test_discount_factor_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.discount_factor = "0"

    def test_qtable_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.qtable = "0"

    def test_previous_state_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.previous_state = 1

    def test_previous_action_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.previous_action = 1

    def test_available_actions_setter_error(self):
        ql = QLearning(actions=['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            ql.available_actions = 1
