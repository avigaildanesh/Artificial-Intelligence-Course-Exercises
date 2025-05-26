import zuma
import pickle
import numpy as np
from collections import defaultdict
import random

id = ["111111"]  # Python Version 3.13.1


class Policy: 
    """This class is a Policy for a Zuma game.""" 

    def __init__(self, game: zuma.Game):
        """Initialize and generate Policy for given game model.
        This method MUST terminate within the specified timeout.

        methods in game that you're able to use:
        new_line, new_ball, reward_for_action, is_done = game.submit_next_action(index/or -1)
        total_reward for_episode = game.play_game(policy)
        current_line, current_ball, current_step, max_steps = game.get_current_state()
        game.reset(generate_new_line=False)
        """
        self.game = game
        self.max_steps = game.get_current_state()[3]
        self.max_line_length = game._max_length
        # tip to initialize table
        # arr = np.zeros((int(sum([math.pow(4, i) for i in range(max_line_length + 1)])), max_line_length+2)) 

        # Q-table
        self.Q = defaultdict(lambda: defaultdict(float))

        # Learning parameters
        self.alpha = 0.05
        self.gamma = 0.95 
        self.epsilon = 0.50
        self.epsilon_min = 0.10
        self.epsilon_decay = 0.995
        self.n_steps = 3
        self.num_episodes = 103000

        # Load existing policy if exists
        try:
            self.load_policy("policy")
            print("Loaded existing policy from file.")
        except FileNotFoundError:
            print("No existing policy found, starting from scratch...")

        ####### IF YOU WANT TO TRAIN, Remove the comment from the next 2 lines! #######
        #self._train_policy()
        #self.save_policy("policy")


    def _train_policy(self):
        """Train the policy using n-step Q-learning."""
        for episode in range(self.num_episodes):
            self.game.reset()
            state_history = []
            action_history = []
            reward_history = []
            done = False

            while not done:
                current_line, current_ball = self.game.get_current_state()[:2]
                state_key = self._state_to_key((current_line, current_ball))

                # Epsilon-Greedy
                if random.random() < self.epsilon:
                    action = random.choice(self._get_valid_actions((current_line, current_ball)))
                else:
                    action = self._get_best_action((current_line, current_ball))

                # Store transition
                new_line, new_ball, reward, done = self.game.submit_next_action(action)
                state_history.append(state_key)
                action_history.append(action)
                reward_history.append(reward)

                # N-step update
                if len(state_history) >= self.n_steps:
                    G = 0.0
                    for i in range(self.n_steps):
                        G += (self.gamma ** i) * reward_history[i]

                    # Butstrap if not done
                    if not done:
                        next_state_key = self._state_to_key((new_line, new_ball))
                        if len(self.Q[next_state_key]) > 0:
                            G += (self.gamma ** self.n_steps) * max(self.Q[next_state_key].values())

                    old_s = state_history[0]
                    old_a = action_history[0]
                    old_q = self.Q[old_s][old_a]
                    self.Q[old_s][old_a] = old_q + self.alpha * (G - old_q)

                    # remove the oldest step from the queue
                    state_history.pop(0)
                    action_history.pop(0)
                    reward_history.pop(0)

            # Final update for episode
            while len(state_history) > 0:
                G = 0.0
                steps_to_update = len(state_history)
                for i in range(steps_to_update):
                    G += (self.gamma ** i) * reward_history[i]

                old_s = state_history[0]
                old_a = action_history[0]
                old_q = self.Q[old_s][old_a]
                self.Q[old_s][old_a] = old_q + self.alpha * (G - old_q)

                state_history.pop(0)
                action_history.pop(0)
                reward_history.pop(0)

            # Reduce epsilon gradually
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


    def _state_to_key(self, state):
        """Convert (line, ball) -> hashable tuple."""
        line, ball = state
        return (tuple(line), ball)


    def _get_valid_actions(self, state):
        """Get list of valid actions: -1 (skip) to len(line)."""
        line, _ = state
        return list(range(-1, len(line) + 1))


    def _get_best_action(self, state):
        """Return best action based on current Q or fallback to a heuristic."""
        state_key = self._state_to_key(state)
        line, ball = state
        valid_actions = self._get_valid_actions(state)

        if state_key in self.Q and len(self.Q[state_key]) > 0:
            return max(valid_actions, key=lambda a: self.Q[state_key].get(a, 0.0))
        else:
            # Short fallback for unknown states
            return max(valid_actions, key=lambda a: self._evaluate_action(line, ball, a))


    def _evaluate_action(self, line, ball, action):
        """Heuristic for unknown states."""
        if action == -1:
            return -5  # punishment for skipping

        # evaluate potential reward
        temp_line = list(line)
        temp_line.insert(action, ball)

        # check sequence
        consecutive = self._count_consecutive(temp_line, ball)
        reward = consecutive * 5
        if consecutive >= 3:
            reward += 20

        # if we are about to exceed the line length
        if len(temp_line) >= self.max_line_length - 1:
            reward -= 10

        return reward


    def _count_consecutive(self, line, color):
        """Count max consecutive occurrences of 'color' in 'line'."""
        max_c = 0
        cur_c = 0
        for b in line:
            if b == color:
                cur_c += 1
                max_c = max(max_c, cur_c)
            else:
                cur_c = 0
        return max_c


    def choose_next_action(self, state):
        """Choose next action for Zuma given the current state of the game.
        state is a tuple of (line, ball_to_throw)
        """
        return self._get_best_action(state)


    def save_policy(self, file):
        """Save Q-table to a pkl file."""
        q_dict = {k: dict(v) for k, v in self.Q.items()}
        with open(file + ".pkl", "wb") as f:
            pickle.dump(q_dict, f)
        print("Policy saved to", file + ".pkl")


    def load_policy(self, file):
        """Load Q-table from a pkl file."""
        with open(file + ".pkl", "rb") as f:
            loaded_dict = pickle.load(f)
        self.Q = defaultdict(lambda: defaultdict(float))
        for k, v in loaded_dict.items():
            self.Q[k] = defaultdict(float, v)
        print("Policy loaded from", file + ".pkl")  
