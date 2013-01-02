#!/usr/bin/env python

""" Apriori algorithm for association rule mining.
"""

from __future__ import division
from abc import ABCMeta, abstractmethod
from itertools import chain, combinations
from operator import itemgetter

__all__ = ["BaseApriori", "NaiveApriori"]

class BaseApriori(object):
    """ The base class of Apriori algorithm.

        Note that this class should NOT be instantiated directly, use its
        descendant classes instead.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 universal_set,
                 support_criterion=0.2,
                 confident_criterion=0.7,
                 maximum_cardinality=5):
        self.universal_set = universal_set
        self.support_criterion = support_criterion
        self.confident_criterion = confident_criterion
        self.maximum_cardinality = maximum_cardinality

    @abstractmethod
    def generate_rules(self, data_sets):
        pass

    @abstractmethod
    def predict(self, rule):
        pass


class NaiveApriori(BaseApriori):
    """ The naive Apriori algorithm implementation.

    Parameters
    ----------
    universal_set : set,
        A set contains all the items of dataset.

    support_criterion : float, optional (default=0.2)
        The support criterion of frequent set. It is the ratio between the
        number of frequent set and the the number of the whole data set.

    confident_criterion : float, optional (default=0.7)
        The confident criterion of rules. The probability of finding an item
        that has all of frequent items is above a certain threshold. e.g. "at
        least 70% of the people who buy diapers also buy beer.

    maximum_cardinality : int, optional (default=5)
        The maximum cardinality of the set of frequent rules.

    Examples
    --------
    >>> from yapa.apriori import NaiveApriori
    >>> apriori = NaiveApriori(universal_set = set(1,2,3,,,100),
                               support_criterion=0.2,
                               confident_criterion=0.7,
                               maximum_cardinality=4)
    >>> data_sets = (set(1,2,5), set(2,3,4),,,set(2,10))
    >>> apriori.generate_rules(data_sets)
    >>> for result, confident in apriori.predict([0,1]):
            print set([0,1]),"->", result, confident
    set([1,2])->set([4]), 0.75
    """

    def __init__(self,
                 universal_set,
                 support_criterion=0.2,
                 confident_criterion=0.7,
                 maximum_cardinality=5):
        super(NaiveApriori, self).__init__(universal_set,
                                          support_criterion,
                                          confident_criterion,
                                          maximum_cardinality)

    def generate_rules(self, data_sets):
        """Generate rules in terms of apriori algorithm.

        Parameters
        ----------
        data_sets : list of sets.
            It contains all data sets, in which each data set stands for a set
            of items.

        Returns
        -------
        None
        """
        self.cardinality_data_sets = len(data_sets)
        # a list of dicts, in which storing key:value "set([1,2]):frequence".
        self.frequent_sets_dict_list = []
        candidate_sets_next_round = combinations(self.universal_set, 1)
        frequent_sets_current_round = []
        candidate_frequence_dict = {}
        for i in range(self.maximum_cardinality):
            for candidate_items in candidate_sets_next_round:
                for data_set in data_sets:
                    if data_set.issuperset(candidate_items):
                        try:
                            candidate_frequence_dict[candidate_items] += 1
                        except KeyError:
                            candidate_frequence_dict[candidate_items] = 1
            frequent_sets_current_round = \
                        self.__filter_candidate_sets(candidate_frequence_dict)
            if len(frequent_sets_current_round) == 0:
                break  # if no frequent sets are found this round, break out.

            candidate_sets_next_round = \
                    self.__build_candidate_sets(frequent_sets_current_round,
                                                i + 1)
            self.frequent_sets_dict_list.append(
                    self.__build_frequent_sets(
                        frequent_sets_current_round,
                        candidate_frequence_dict))
            candidate_frequence_dict = {}

    def __filter_candidate_sets(self, candidate_frequence_dict):
        """Filter the candidate sets that are below as the support_criterion.

        Parameters
        ----------
        candidate_frequence_dict : dict
            A dictionary of (key=candidate sets, value=frequce).

        Returns
        -------
        qualified_sets : list
            A list of sets which meet the requirements of support_criterion.
        """
        qualified_sets = [candidate_set for candidate_set, n in
                          candidate_frequence_dict.iteritems() if
                          n / self.cardinality_data_sets \
                          >= self.support_criterion]
        return qualified_sets

    def __build_frequent_sets(self, frequent_sets, candidate_frequence_dict):
        """Build the frequent sets dictionary.

        Parameters
        ----------
        frequent_sets : list
            A list of frequent sets.

        candidate_frequence_dict : dict
            A dict of candidate set and its frequence pairs.

        Returns
        -------
        frequent_sets_dict : dict
            A dict of frequent set and its frequence pairs.
        """
        return dict((
        frequent_set, candidate_frequence_dict[frequent_set]) for frequent_set
        in frequent_sets if frequent_set in candidate_frequence_dict)

    def __build_candidate_sets(self, frequent_sets_last_round, number_round):
        """Build the candidate sets for the next round. The process of building
        is straigtforward. Firstly, flatten all the frequent sets of last
        round, then build a candidate set from the frequent set, with each set
        having a cardinality of number_round+1.

        Parameters
        ----------
        frequent_sets_last_round : list
            A list of frequent set last round.

        number_round : int
            current number of round

        Returns
        -------
        candidate_sets_next_round : iterable
            Candidate sets for next round.
        """
        return combinations(set(chain.from_iterable(frequent_sets_last_round)),
                            number_round + 1)

    def predict(self, rule):
        """Predict the relevant result with given rule according to the
        frequent sets information.

        Parameters
        ----------
        rule : iterable
            Any iterable object would be turned into a set, by which predicts
            all items are frequently exposed along this rule.

        Returns
        -------
        association : generator
            A generator of associations.
            Every association tuples consists of two parts. Firstly, the item
            of this association. The second part is the confident probability
            of this association.

        Exceptions
        ----------
        AttributeException
            Raised when this method being called before generating frequent
            sets by calling method generate_rules with data sets.

        TypeError
            A TypeError is raised if the argument rule is not a iterable.
        """
        rule_set = set(rule)
        frequent_sets_list = getattr(self, "frequent_sets_dict_list")
        association_list = []

        if len(rule_set) == 0:
            return
        try:
            frequent_sets_dict = frequent_sets_list[len(rule_set)]
        except IndexError:
            # This means no frequent sets available for this rule.
            return

        association_list = [(sets, frequence) for sets, frequence
                in frequent_sets_dict.iteritems() if rule_set.issubset(sets)]
        if len(association_list) == 0:
            return
        total = sum(itemgetter(1)(association) for association in
                    association_list)
        for sets, frequence in association_list:
            yield set(sets).difference(rule_set), frequence / total

    def get_frequent_sets(self, set_cardinality):
        """Retrieve frequent sets which cardinality is set_cardinality.

        Parameters
        ----------
        set_cardinality : int

        Returns
        -------
        frequent_sets : a dict of (set tuple):frequence pais


        Exceptions
        ----------
        AttributeException
            Raised when this method being called before generating frequent
            sets by calling method generate_rules with data sets.
        """
        frequent_sets_list = getattr(self, "frequent_sets_dict_list")

        try:
            frequent_sets_dict = frequent_sets_list[set_cardinality-1]
        except IndexError:
            return {}  # This means no frequent sets available for this rule.
        return frequent_sets_dict

    def print_all_frequent_sets(self):
        """ Printing frequent sets in the order of sets' cardinality.

        Parameters
        ----------
        None


        Exceptions
        ----------
        AttributeException
            Raised when this method being called before generating frequent
            sets by calling method generate_rules with data sets.
        """
        frequent_sets_list = getattr(self, "frequent_sets_dict_list")
        for frequent_sets_dict in frequent_sets_list:
            for sets, frequence in frequent_sets_dict.iteritems():
                print sets, frequence
