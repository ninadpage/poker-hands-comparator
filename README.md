# poker-hands-comparator
A Python implementation which categorizes 5-card-hands as per the rules of Poker. The PokerHand class
also implements `__cmp__` method to compare or sort hands.

The categorization and comparison is mainly based on the frequencies of each card number associated
with its rank in Poker. See code comments for more explanation.

### Requirements
Tested with Python 2.7. Can be made Python 3.x compatible by splitting `PokerHand.__cmp__` method
into `__lt__` and `__eq__`.

### Tests
Execute all tests using `$ python -m unittest discover`
