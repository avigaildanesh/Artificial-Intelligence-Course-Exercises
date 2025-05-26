import ex1
import search


def run_problem(func, targs=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
    return result


# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):
    for row in problem:
        print(row)

    try:
        p = ex1.create_zuma_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")


problema1 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))
# solution1: len(solution) = 4
problema2 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))
# solution2: len(solution) = 7 
problem1 = ((1, 1), (1,))  # 1, t: 0
problem2 = ((1, 2, 2, 1, 1), (2, 1))  # 1, t: 0
problem3 = ((1, 2, 3, 3, 2, 2, 1, 1), (3,))  # 1, t: 0
problem4 = ((2, 2, 3, 2), (3, 3))  # 2, t: 0
problem5 = ((2, 2, 3, 2), (3, 3, 2, 1, 2, 2, 4))  # 2, t: 0
problem6 = ((2, 2, 3, 3, 2), (1, 3))  # 2, t: 0
problem7 = ((3, 3, 4, 4, 3, 3), (3, 4))  # 2, t: 0
problem8 = ((1, 1, 2, 2, 1, 1, 3, 3, 4, 4, 3, 1, 1), (2, 4, 3, 3, 3, 1))  # 2, t: 0
problem9 = ((2, 3, 3, 2), (1, 2, 3))  # 3, t: 0
problem10 = ((4, 1, 2, 3, 3, 2, 2, 1, 1), (4, 3, 4))  # 3, t: 0
problem11 = ((1, 1, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 4, 1, 1, 4, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 3, 4))  # 3, t: 0
problem12 = ((2, 2, 3, 3, 1), (1, 1, 2, 3))  # 4, t: 0
problem13 = ((4, 2, 2, 3, 3, 2), (1, 3, 4, 4))  # 4, t: 0
problem14 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4))  # 4, t: 0
problem15 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))  # 4, t: 0
problem16 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 2))  # 4, t: 0.05, 0
problem17 = ((1, 1, 3, 3, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 3, 3, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))  # 4, t: 0.1, 0
problem18 = ((2, 2, 3, 3, 1), (4, 1, 1, 2, 3))  # 5, t: 0
problem18_1 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 2, 1))  # 5, t: 0
problem19 = ((1, 2, 2, 1, 1, 3, 3, 1), (4, 2, 3, 4, 4, 3, 2, 3, 2, 2, 3, 1, 1))  # 5, t: 0
problem20 = ((1, 1, 2, 4, 1, 1, 4, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 3, 4))  # 5, t: 0.25, 0.1
problem21 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 2, 3, 4))  # 5, t: 0.21, 0.05
problem22 = ((1, 1, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 2, 2), (1, 2, 3, 4, 1, 3))  # 5, t: 0.17, 0.03
problem22_1 = ((1, 1, 3, 3, 2, 2, 3, 1, 2, 3, 3, 2, 2, 3, 3, 1, 1), (3, 1, 2, 4, 3, 4, 3, 1))  # 5, t: 0.08, 0.03
problem22_2 = ((1, 1, 3, 3, 2, 2, 3, 1, 4, 2, 3, 3, 2, 2, 3, 3, 1, 1), (3, 4, 1, 2, 4, 3, 4, 3, 1))  # 6, t: 9.6, 2
problem23 = ((3, 3, 4, 4, 3, 3), (3, 1, 2, 3, 2, 1, 4))  # 7, t: 0
problem24 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 2))  # 7, t: 0
problem25 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))  # 7, t: 0.06
problem25_1 = ((1, 1, 2, 2, 1, 1, 3, 3, 4, 4, 3, 1, 1), (3, 3, 3, 3, 3, 2, 4, 3, 3, 3, 1))  # 7, t: 0.23, 0.06
problem25_2 = ((3, 3, 1, 1, 4, 3, 2, 4, 3, 3, 2, 4, 4, 1, 3), (4, 4, 2, 2, 3, 3, 3, 1, 3))  # 7, t: 9.6, 7.2
problem26 = ((1, 3, 3, 2, 1, 2, 2), (1, 3, 2, 4, 2, 3, 4, 2))  # 8, t: 0.03, 0.01
problem27 = ((1, 2, 1, 2), (1, 2, 4, 1, 2, 2, 4, 1, 3, 2, 1, 2))  # 10, t: 0
problem28 = ((2, 2, 3, 2), (3, 1))  # no, t: 0
problem29 = ((4, 2, 2, 3, 3, 2), (1, 3))  # no, t: 0
problem30 = ((2, 2, 3, 3, 2, 4), (2, 2, 3, 2))  # no, t: 0
problem31 = ((4, 2, 2, 3, 3, 2), (1, 3, 4))  # no, t: 0
problem32 = ((4, 2, 2, 3, 3, 1), (1, 1, 2, 3))  # no, t: 0


def main():
    problem = problema2
    algorithm = "gbfs"  # or "astar"

    solve_problems(problem, algorithm)


if __name__ == '__main__':
    main()
