
def fitness(individual, planes):
    penalty = 0
    for position in individual:
        id, time = position
        plane = planes[int(id)]
        if time > plane.target:
            penalty+=(time-plane.target)*plane.penalty_late
        elif time < plane.target:
            penalty+=(plane.target-time)*plane.penalty_early
    return penalty
