
from eac_test.hello_world import hello, waste_cpu


def test_hello():
    hello()


def test_waste_cpu():
    pi_est = waste_cpu()
    assert pi_est > 3.10
    assert pi_est < 3.18
    
    
