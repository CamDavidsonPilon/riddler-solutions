def simulated_annealing(loss, sample_generator, initial_sol, cooling_steps=100,
                        steps_per_temp=350, alpha=0.97, initial_temp=1.):

    def boltzman_probability(loss1, loss2, temp):
        k = 50.
        return np.exp((loss1 - loss2) / (k * temp))


    t = initial_temp
    sol = initial_sol
    min_loss = loss(sol)

    for _ in xrange(cooling_steps):
        for i in xrange(steps_per_temp):
            sol_ = sample_generator(sol)
            loss_ = loss(sol_)
            if loss_ < 0:
                return True

            if min_loss > loss_:
                min_loss = loss_
                sol = sol_
            elif boltzman_probability(min_loss, loss_, t) > np.random.random():
                min_loss = loss_
                sol = sol_
        t = alpha * t
    return False


def loss(T, opponent):
    prize = [-1, 1]
    return sum([
            prize[(T[i] < opponent[i])] * (i+1)
        for i in xrange(10)])

def sample_generator(T):
    # pick one index to increase, pick one index to decrease. This is independent of the sum of the vector.
    T_ = T.copy()
    while True:
        ix_increase, ix_decrease = np.random.randint(0, 10, 2)
        if T_[ix_decrease] > 0 and ix_decrease != ix_increase:
            T_[ix_increase] += 1
            T_[ix_decrease] -= 1
            return T_

def generate_opponent():
    return random_T_with_n_elements(100)

def random_T_with_n_elements(n):
    p = np.array([ 0.0182,  0.0364,  0.0545,  0.0727,  0.0909,  0.1091,  0.1273,
        0.1455,  0.1636,  0.1818])
    return np.random.multinomial(n, p)



for n in xrange(51, 54):
    wins = 0
    for _ in xrange(300):
        opponent = generate_opponent()
        loss_ = lambda T: loss(T, opponent)
        if simulated_annealing(loss_, sample_generator, random_T_with_n_elements(n)) \
            or simulated_annealing(loss_, sample_generator, random_T_with_n_elements(n))\
            or simulated_annealing(loss_, sample_generator, random_T_with_n_elements(n))\
            or simulated_annealing(loss_, sample_generator, random_T_with_n_elements(n))\
            or simulated_annealing(loss_, sample_generator, random_T_with_n_elements(n))\
            or simulated_annealing(loss_, sample_generator, random_T_with_n_elements(n))\
            :
            wins += 1
        else:
            print opponent
    print n, wins
