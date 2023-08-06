from typing import List, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame

from rkt_lib_toolkit.logger import Logger
from rkt_lib_toolkit.config import Config


class QLearning:
    """
    Exploration vs. Exploitation Tradeoff:
        The agent initially has none or limited knowledge about the environment.
        The agent can choose to explore by selecting an action with an unknown outcome,
        to get more information about the environment.
        Or, it can choose to exploit and choose an action based on its prior knowledge of the environment
        to get a good reward.

    """

    def __init__(self,
                 actions: List,
                 should_load: bool = False,
                 qtable_file_to_load: str = "",
                 alpha: float = 0.1,
                 gamma: float = 0.8,
                 action_selection_method: str = "epsilon-greedy"):
        """
        Machine learning class based on q-learning\n

        epsilon-greedy : (https://www.baeldung.com/cs/epsilon-greedy-q-learning)

        @param actions: list of available actions
        @param should_load: define if you want load the file contain dataframe (pkl file)
        @param qtable_file_to_load: Path to dataframe pkl file
        @param alpha: learning rate, can be defined as the degree of acceptance of the new value over the old one.
                    set between 0 and 1. Setting it to 0 means that the Q-values are never updated,
                    hence nothing is learned. Setting a high value such as 0.9 means that learning can occur quickly.
        @param gamma: discount factor, generally this value vary between 0.8 and 0.99
        """

        self._me = self.__class__.__name__
        self._logger: Logger = Logger(caller_class=self.me)
        self._logger.set_logger(caller_class=self.me, output="stream")
        self._config: Config = Config()

        self.learning_rate: float = alpha
        self.discount_factor: float = gamma

        self.qtable: Optional['DataFrame'] = None
        self.available_actions = actions
        self.previous_state: str = "start"
        self.previous_action: str = "do-nothing"
        self.action_selection_method: str = action_selection_method

        self.load(should_load, qtable_file_to_load)

    # PROPERTIES
    @property
    def me(self) -> str:
        return self._me

    @me.setter
    def me(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_me' property must be a string")
        self._me: str = value

    @property
    def logger(self) -> Logger:
        return self._logger

    @logger.setter
    def logger(self, value: Logger) -> None:
        if not isinstance(value, Logger):
            raise TypeError("The '_logger' property must be a 'Logger'")
        self._logger: Logger = value

    @property
    def config(self) -> Config:
        return self._config

    @config.setter
    def config(self, value: Config) -> None:
        if not isinstance(value, Config):
            raise TypeError("The '_config' property must be a 'Config'")
        self._config: Config = value

    @property
    def learning_rate(self) -> float:
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("The '_learning_rate' property must be a float")
        self._learning_rate: float = value

    @property
    def discount_factor(self) -> float:
        return self._discount_factor

    @discount_factor.setter
    def discount_factor(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("The '_discount_factor' property must be a float")
        self._discount_factor: float = value

    @property
    def qtable(self) -> 'DataFrame':
        return self._qtable

    @qtable.setter
    def qtable(self, value: 'DataFrame') -> None:
        if not isinstance(value, DataFrame) and value is not None:
            raise TypeError("The '_qtable' property must be a DataFrame")
        self._qtable: Optional['DataFrame'] = value

    @property
    def previous_state(self) -> str:
        return self._previous_state

    @previous_state.setter
    def previous_state(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_previous_state' property must be a string")
        self._previous_state: str = value

    @property
    def previous_action(self) -> str:
        return self._previous_action

    @previous_action.setter
    def previous_action(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_previous_action' property must be a string")
        self._previous_action: str = value

    @property
    def available_actions(self) -> List:
        return self._available_actions

    @available_actions.setter
    def available_actions(self, value: List) -> None:
        if not isinstance(value, List):
            raise TypeError("The '_available_actions' property must be a list")
        self._available_actions: List = value

    @property
    def action_selection_method(self) -> str:
        return self._action_selection_method

    @action_selection_method.setter
    def action_selection_method(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_action_selection_method' property must be a str")
        self._action_selection_method: str = value

    def __repr__(self) -> str:
        return f"QLearning(alpha={self.learning_rate}, gamma={self.discount_factor})"

    # Functions
    # # Management
    def save(self, file: str) -> None:
        self.qtable.to_pickle(file)

    def load(self, do_load: bool, file_to_load: str) -> None:
        if do_load:
            self.qtable = pd.read_pickle(file_to_load)
        else:
            self.qtable = pd.DataFrame(columns=self.available_actions, dtype=np.float64)

    # # AI
    def choose_action(self, state: str):
        """
        Epsilon parameter is related to the epsilon-greedy (e_greedy) action selection procedure in the
        Q-learning algorithm.
        In the action selection step, we select the specific action based on the Q-values we already have.
        The epsilon parameter introduces randomness into the algorithm, forcing us to try different actions.
        This helps not to get stuck in a local optimum.

        If epsilon is set to 0, we never explore but always exploit the knowledge we already have.
        On the contrary, having the epsilon set to 1 force the algorithm to always take random actions and
        never use past knowledge. Usually, epsilon is selected as a small number close to 0.

        @param state :
        @return :
        """
        self.check_state_exist(state)
        chosen_action: str = "do-nothing"
        if self.action_selection_method == "epsilon-greedy":
            chosen_action = self._choose_action_epsilon_greedy(state)

        return chosen_action

    def _choose_action_epsilon_greedy(self, state: str, e_greedy: float = 0.5):
        e_greedy = 2 if self.previous_state == "start" else e_greedy

        if np.random.uniform() < e_greedy:
            action = np.random.choice(self.available_actions)
        else:
            state_action = self.qtable.loc[state, :]
            a = np.max(state_action)
            z = state_action[state_action == a]

            action = np.random.choice(z.index) if len(z) > 1 else z.index
        return action

    def learn(self, state: str, action: str, reward: float) -> None:
        """
        Run for each step from your Bot\n

        pseudo-code:\n
        Q(S{t}, A{t}) <- Q(S{t}, A{t}) + alpha * [R_{t+1} + gamma * max(Q(S{t+1}, a) - Q(S{t}, A{t}))]\n
        Q(S, A) <- Q(S, A) + alpha * [R + gamma * max(Q(S', A')) - Q(S, A)]
        Q(S{t}, A{t}) <- Q(S{t}, A{t}) + alpha * (R + gamma * np.max(Q[S{t+1}, :]) — Q(S{t}, A{t}))

        where:
            Q: qtable\n
            S: State\n
            A: selected Action (see choose_action function)\n
            R: Reward\n
            t: T time (so t+1 is next T time, etc.)\n
            max: function max like np.max()\n

        :param state:
        :param action:
        :param reward:
        :return:
        """
        self.check_state_exist(state)
        if self.previous_state != "start":
            last_qvalue = self.qtable.loc[self.previous_state, self.previous_action]
            qvalue = self.qtable.loc[state, action]

            estimated_reward = self.learning_rate * (reward + self.discount_factor * np.max(qvalue) - last_qvalue)
            self.qtable.loc[self.previous_state, self.previous_action] += estimated_reward

        self.previous_state = state
        self.previous_action = action

    def check_state_exist(self, state: str):
        if state not in self.qtable.index:
            self.qtable.loc[state] = pd.Series([0] * len(self.available_actions), index=self.qtable.columns, name=state)
