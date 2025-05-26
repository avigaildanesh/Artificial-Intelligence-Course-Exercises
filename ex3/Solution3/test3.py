import ex3
import zuma

def solve(game: zuma.Game, debug=False):
    policy = ex3.Policy(game)
    return game.evaluate_policy(policy, 5000, visualize=debug)

# Provided results
provided_results = {
    5: [-11.1364, 28.563, 2.0114, -3.806, -5.246, -8.6566, -10.3142, -11.2202, -12.8852, -13.8732],
    10: [-19.3912, 61.51, 9.4976, 1.0076, -1.567, -6.6588, -7.5254, -8.9704, -10.6912, -11.7906],
    20: [-35.9464, 94.2624, 22.2294, 9.155, 5.6466, 1.1238, -2.1264, -3.714, -5.4032, -6.139],
    30: [-52.4024, 111.6314, 30.2928, 15.483, 13.4494, 6.6456, 4.0912, 2.7176, 2.4884, -0.7604],
    40: [-68.8154, 119.9152, 40.6316, 20.121, 23.1612, 13.9964, 10.3104, 10.3064, 8.6902, 7.423],
    50: [-85.27, 123.7646, 47.8192, 28.4574, 30.7978, 17.7722, 16.8604, 14.0318, 14.7574, 13.1836]
}

example = {
    'chosen_action_prob': {1: 0.6, 2: 0.7, 3: 0.5, 4: 0.9},
    'next_color_dist': {1: 0.1, 2: 0.6, 3: 0.15, 4: 0.15},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150,
    'seed': 42}

def main():
    debug_mode = False
    turns = [5, 10, 20, 30, 40, 50]
    my_results = {}
    total_difference = 0
    total_count = 0

    for j in turns:
        print(f"Number of turns: {j}")
        my_results[j] = []
        for i in range(1, 11):
            game = zuma.create_zuma_game((j, i, [], example, debug_mode))
            avg_result = solve(game, debug_mode)
            my_results[j].append(avg_result)

            # Difference with provided results
            difference = avg_result - provided_results[j][i - 1]
            total_difference += difference
            total_count += 1

            print(f"max line: {i} - My Average: {avg_result:.4f} - "
                  f"Provided Average: {provided_results[j][i - 1]:.4f} - "
                  f"Difference: {difference:.4f}")

        print("")

    # Calculate and print the average difference
    avg_difference = total_difference / total_count
    print(f"Average difference between my results and provided results: {avg_difference:.4f}")

main()
