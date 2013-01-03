# Yet Another Python Apriori Algorithm Implementation

The python implementation of Apriori Algorithm.  
Frequently used for association rule mining. e.g. People like coke, also like
lime

## Installation

    $ sudo python setup.py install

## Getting started

    >>> from yapa.apriori import NaiveApriori
    >>> # Instantiate a apriori with universal set, and a bunch of parameters
    >>> apriori = NaiveApriori(universal_set = set(range(1,10)),
                               support_criterion=0.2,
                               confident_criterion=0.7,
                               maximum_cardinality=4)
    >>> # Prepare the sample sets, AKA, training sets.
    >>> data_sets = (set(1,2,5), set(2,3,4), set(1,2,3), set(2,10))
    >>> # Generate the rules
    >>> apriori.generate_rules(data_sets)
    >>> # Predict a associated element based on an input
    >>> for result, confident in apriori.predict([0,1]):
            print set([0,1]),"->", result, confident
    set([1,2])->set([4]), 0.75

## API Reference

Please reference the docstrings

## Test

    $ nosetests test
    
or  

    $ python -m unittest test 

## License

See LICENSE

