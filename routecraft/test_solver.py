import itertools
import random
import unittest
from solver import solve,length
class SolverTests(unittest.TestCase):
    def test_square_optimum(self):
        p=[[0,0],[1,1],[1,0],[0,1]];r=solve(p)
        self.assertAlmostEqual(r['optimised_length'],4)
        self.assertEqual(r['route'][0],0)
    def test_every_stop_once_and_never_worse(self):
        rng=random.Random(42)
        for n in range(2,30):
            p=[[rng.random()*100,rng.random()*100] for _ in range(n)];r=solve(p)
            self.assertEqual(sorted(r['route']),list(range(n)))
            self.assertLessEqual(r['optimised_length'],r['nearest_neighbour_length']+1e-8)
    def test_duplicate_points(self):self.assertEqual(solve([[0,0],[0,0]])['saved_percent'],0)
    def test_invalid(self):
        for p in [[],[[float('nan'),0]],[[True,0]],[[10001,0]],[[1]]]:
            with self.assertRaises(ValueError):solve(p)
    def test_small_instance_against_exact_optimum(self):
        p=[[0,0],[1,0],[1,1],[0,1],[.5,.5]]
        exact=min(length(p,[0]+list(t)) for t in itertools.permutations(range(1,len(p))))
        self.assertAlmostEqual(solve(p)['optimised_length'],exact)
