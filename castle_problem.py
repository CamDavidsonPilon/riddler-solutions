import np

def simulated_annealing(loss, sample_generator, initial_sol, cooling_steps=75,
                        steps_per_temp=250, alpha=0.90, initial_temp=1.):

    def boltzman_probability(loss1, loss2, temp):
        k = 1.
        return np.exp((loss1 - loss2) / (k * temp))


    t = initial_temp
    sol = initial_sol
    min_loss = loss(sol)

    for _ in xrange(cooling_steps):
        for i in xrange(steps_per_temp):
            sol_ = sample_generator(sol)
            loss_ = loss(sol_)
            if min_loss > loss_:
                min_loss = loss_
                sol = sol_
            elif boltzman_probability(min_loss, loss_, t) > np.random.random():
                min_loss = loss_
                sol = sol_
        t = alpha * t

    return sol, min_loss


def loss(T, data):
    # given a (1, 10) vector of troop positions, T, what is the expected value of winning
    # needs to account for ties better.
    prizes = np.arange(1, 11, dtype=float)
    my_score = (data < T).dot(prizes)
    opp_score = (data > T).dot(prizes)
    return (my_score > opp_score).mean()


def sample_generator(T):
    # pick one index to increase, pick one index to decrease
    T_ = T.copy()
    while True:
        ix_increase, ix_decrease = np.random.randint(0, 10, 2)
        if T_[0][ix_decrease] > 0 and ix_decrease != ix_increase:
            T_[0][ix_increase] += 1
            T_[0][ix_decrease] -= 1
            return T_

def create_new_optimal_strategy(data):
    T = np.array([10*[10]])
    loss_ = lambda t: loss(t, data)
    T_prime, loss_prime = simulated_annealing(loss_, sample_generator, T)
    return T_prime, loss_prime


def create_final_optimum_strategy(data):
    loss_ = lambda t: loss(t, data)
    T = np.array([10*[10]])
    strategies = []
    for _ in xrange(20):
        strategies.append(simulated_annealing(loss_, sample_generator, T, cooling_steps=100, steps_per_temp=400, alpha=0.88, initial_temp=1.))
    return min(strategies, key=lambda z: z[1])


data = pd.read_csv("data.csv")
del data['Why did you choose your troop deployment?']
COLS = data.columns
NEW_ADDITIONS = 600
for x in xrange(1, NEW_ADDITIONS+1):
    print "round %d" % x
    novel_strategy, loss_prime = create_new_optimal_strategy(data)
    print novel_strategy, loss_prime
    data = data.append(dict(zip(COLS, novel_strategy[0])), ignore_index=True)
    data = data.append(dict(zip(COLS, novel_strategy[0])), ignore_index=True)
    print


print create_final_optimum_strategy(data)
