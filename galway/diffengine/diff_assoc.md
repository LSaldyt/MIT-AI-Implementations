# Notes on difference engine heuristic-transformation associations

Order heuristics by importance

Given a list of transformations, do a one time abstract analysis of what heuristics they change

Associate each transform with particular heuristics

Begin a proof

Start at the beginning of the heuristic list

If the heuristic is true, apply the relevant transformations and continue

Otherwise, move to the next heuristic

If none of the specific transformations work, fall back to a-star style search

Benefits: constant time transformation picking (as opposed to generating all branches)

Learning:

Algorithm might not start with knowledge of which transformations affect which heuristics

Instead, it might create a database of these associations, and update the database as it progresses
