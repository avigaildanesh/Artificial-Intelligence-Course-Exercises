import zuma
import copy

id = ["111111"] 


class Controller:
    """This class is a controller for a Zuma game."""

    def __init__(self, game: zuma.Game):
        """Initialize controller for given game model.
        This method MUST terminate within the specified timeout.
        """
        self.original_game = game
        self.copy_game = copy.deepcopy(game)
        self.model = game.get_model()

    def explosion_of_balls(self, line_of_balls, insertion_point):
        """This function estimates the potential explosion in the line of balls after inserting a ball.
        """ 

        if 0 <= insertion_point < len(line_of_balls):
            test_line = line_of_balls[:insertion_point] + [line_of_balls[insertion_point]] + line_of_balls[insertion_point:]
        else:
            test_line = line_of_balls

        color_sequences = self.find_sequences_of_colors(test_line)
        potential_explosion = sum(len(sequence) * self.model['color_pop_prob'].get(color, 0.5) for color, sequence in color_sequences.items() for ball in sequence if len(sequence) >= 3)

        return potential_explosion

    def find_sequences_of_colors(self, line_of_balls):
        """This function finds sequences of all colors in the line of balls. 
        Returns a dictionary where keys are colors and values are lists of sequences of that color.
        """ 

        sequences = {} 
        current_sequence = []
        current_color = None
        
        for ball in line_of_balls:
            if current_color is None or current_color != ball:
                if current_sequence:
                    if len(current_sequence) >= 3:
                        sequences[current_color] = sequences.get(current_color, []) + [current_sequence]
                current_color = ball
                current_sequence = [ball]
            else:
                current_sequence.append(ball)

        if current_sequence:
            if len(current_sequence) >= 3:
                sequences[current_color] = sequences.get(current_color, []) + [current_sequence]

        return {color: tuple(sequence) for color, sequence_list in sequences.items() for sequence in sequence_list}

    def get_result_of_actions(self, action):
        """This function here is calculating the result for the given actions.   
        """ 

        game_copy = copy.deepcopy(self.original_game)
        line_of_balls, current_ball, _, _ = game_copy.get_current_state()
        game_copy.submit_next_action(action)
        updated_reward = game_copy.get_current_reward() - self.original_game.get_current_reward()
        estimated_explosion_on_line = self.explosion_of_balls(line_of_balls, action)
        prob_action = self.model['chosen_action_prob'].get(current_ball, 0.5)
        result = prob_action * 2 + updated_reward * 4 + estimated_explosion_on_line * 3
        
        return result

    def choose_next_action(self):
        """Choose next action for Zuma given the current state of the game.
        """ 

        line_of_balls, current_ball, _, _ = self.original_game.get_current_state()
        predicted_actions = list(range(len(line_of_balls) + 1))
        results_of_actions = { action: self.get_result_of_actions(action) for action in predicted_actions}
        best_action = max(results_of_actions, key=results_of_actions.get)
        
        return best_action
