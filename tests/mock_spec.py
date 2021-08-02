"""mock testing."""

from expects import equal, expect
from mamba import description, it

with description('Mock mamba test'):
    with it('Mock mamba test'):
        expect(True).to(equal(True))
