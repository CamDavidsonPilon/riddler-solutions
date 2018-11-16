import numpy as np
import pandas as pd
# https://fivethirtyeight.com/features/riddler-nation-goes-to-war/

CARDS = np.arange(2, 15)


def simulated_annealing(loss, sample_generator, initial_sol, cooling_steps=75,
                        steps_per_temp=250, alpha=0.98, initial_temp=1.):

    def boltzman_probability(loss1, loss2, temp):
        k = 0.1
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


def house_loss(T):
    return ((T <= np.flip(CARDS, 0)).sum() >= 7) or ((T <= CARDS).sum() >= 7)


def loss(T, data):
    # given a (1, 13) vector respresenting a permutation, T, what is the expected value of winning?
    pop_score = -((T > data).sum(1) >= 7).mean()
    house_score = house_loss(T)
    return pop_score + 50*house_score


def sample_generator(T):
    # swap two positions
    for _ in xrange(10):
        x, y = np.random.randint(0, 13, size=2)
        T[x], T[y] = T[y], T[x]
        if not house_loss(T):
            return T
    return T


def create_new_optimal_strategy(data):
    T = np.random.permutation(CARDS)
    loss_ = lambda t: loss(t, data.values)
    T_prime, loss_prime = simulated_annealing(loss_, sample_generator, T)
    return T_prime, loss_prime


def create_final_optimum_strategy(data):
    loss_ = lambda t: loss(t, data.values)
    T = np.random.permutation(CARDS)
    strategies = []
    for _ in xrange(20):
        s, l = simulated_annealing(loss_, sample_generator, T, cooling_steps=100, steps_per_temp=400, alpha=0.97, initial_temp=1.)
        if not house_loss(s):
            strategies.append((s, l))
    return min(strategies, key=lambda z: z[1])


NEW_ADDITIONS = 600
INIT_RANDOM_STRATS = 200
data = pd.DataFrame([np.random.permutation(CARDS) for _ in range(INIT_RANDOM_STRATS)])
data = data[data.apply(lambda T: not house_loss(T), axis=1)]

for x in xrange(1, NEW_ADDITIONS+1):
    print "round %d" % x
    novel_strategy, loss_prime = create_new_optimal_strategy(data)
    if not house_loss(novel_strategy):
        print novel_strategy, loss_prime
        print data.apply(lambda T: not house_loss(T), axis=1).mean()
        data = data.append(dict(zip(np.arange(0, 13), novel_strategy)), ignore_index=True)
        print


