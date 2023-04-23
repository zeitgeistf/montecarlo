import unittest

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from montecarlo import Analyzer, Die, Game


class DieTestSuite(unittest.TestCase):

    def test_die_initialization_1(self):
        """
        PURPOSE: A dataframe with numeric faces and weights gets
            created upon initialization
        """
        faces = [1, 2, 3, 4, 5, 6]
        die = Die(faces)

        self.assertTrue(
            isinstance(die._die_df, pd.DataFrame), "Die DF should be an instance of Pandas dataframe")

        self.assertEqual(
            list(die._die_df.faces), faces, "Dataframe faces column value should match with input")

        self.assertEqual(
            len(die._die_df.faces), len(die._die_df.weights), "Length of faces and weights should match")

        expected_default_weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.assertEqual(
            list(die._die_df.weights), expected_default_weights, "Default weights should all equal to 1.0")

    def test_die_initialization_3(self):
        """
        PURPOSE: A dataframe with string faces and weights gets
            created upon initialization
        """
        faces = ["H", "T"]
        die = Die(faces)

        self.assertTrue(
            isinstance(die._die_df, pd.DataFrame), "Die DF should be an instance of Pandas dataframe")

        self.assertEqual(
            list(die._die_df.faces), faces, "Dataframe faces column value should match with input")

        self.assertEqual(
            len(die._die_df.faces), len(die._die_df.weights), "Length of faces and weights should match")

        expected_default_weights = [1.0, 1.0]
        self.assertEqual(
            list(die._die_df.weights), expected_default_weights, "Default weights should all equal to 1.0")


    def test_die_update_weight(self):
        """
        PURPOSE: Weight should be updated upon calling update_weight method
        """
        faces = [1, 2, 3, 4, 5, 6]
        die = Die(faces)

        expected_new_weight = 2.0
        die.update_weight(face=faces[0], new_weight=expected_new_weight)

        self.assertEqual(die._die_df.weights[0], expected_new_weight, "Updated weight should get reflected")

    def test_die_update_weight_with_incorrect_face(self):
        """
        PURPOSE: Test if this method errors out when passing in a face value that doesn't exists
            in the dataframe.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die = Die(faces)

        incorrect_face = 7
        correct_new_weight = 2.0
        self.assertRaises(ValueError, die.update_weight, incorrect_face, correct_new_weight)

    def test_die_update_weight_with_incorrect_weight(self):
        """
        PURPOSE: Test if this method errors out when passing in a weight that is not numeric
        """
        faces = [1, 2, 3, 4, 5, 6]
        die = Die(faces)

        correct_face = 1
        incorrect_new_weight = "2.0"
        self.assertRaises(ValueError, die.update_weight, correct_face, incorrect_new_weight)

    def test_die_roll(self):
        """
        PURPOSE: Test if roll method returns correct output when triggered
        """
        faces = [1, 2, 3, 4, 5, 6]
        die = Die(faces)

        res1 = die.roll(times=0)
        self.assertEqual(res1, [], "Empty list should be returned when there's no face input.")

        res2 = die.roll(times=1)
        self.assertTrue(isinstance(res2, list), "Roll method return should be a list.")
        self.assertTrue(res2[0] in faces, "Roll result should come from one of the faces.")

        res3 = die.roll(times=3)
        self.assertEqual(len(res3), 3, "Number of output should match with number of rolls.")
        for i in range(3):
            self.assertTrue(res3[i] in faces, "Roll result should come from one of the faces.")

    def test_die_show(self):
        """
        PURPOSE: Test if the show method can display the result dataframe correctly
        """
        faces = [1, 2, 3, 4, 5, 6]
        expected_weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        die = Die(faces)

        actual_df = die.show()
        self.assertTrue(isinstance(actual_df, pd.DataFrame))

        expected_df = pd.DataFrame({
            'faces': faces,
            'weights': expected_weights
        })
        assert_frame_equal(actual_df, expected_df)


class GameTestSuite(unittest.TestCase):

    def test_game_initialization(self):
        """
        PURPOSE: Test to make sure game object can be successfully created.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die = Die(faces)

        game = Game(dice=[die])
        assert_frame_equal(
            game.dice[0].show(), die.show(), "Class object contained Die object should match with the input Die.")

    def test_get_roll_number(self):
        """
        PURPOSE: Ensure correct roll number mapped list can be returned.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        one_time = 1
        three_times = 3

        # With only 1 die
        game = Game(dice=[die1])
        # 1 time
        actual_roll_number = game._get_roll_number(times=one_time)
        expected_roll_number = [1]
        self.assertEqual(actual_roll_number, expected_roll_number)
        # 3 times
        actual_roll_number = game._get_roll_number(times=three_times)
        expected_roll_number = [1, 2, 3]
        self.assertEqual(actual_roll_number, expected_roll_number)

        # With multiple dice 
        game = Game(dice=[die1, die2])
        # 1 time
        actual_roll_number = game._get_roll_number(times=one_time)
        expected_roll_number = [1, 1]
        self.assertEqual(actual_roll_number, expected_roll_number)
        # 3 times
        actual_roll_number = game._get_roll_number(times=three_times)
        expected_roll_number = [1, 2, 3, 1, 2, 3]
        self.assertEqual(actual_roll_number, expected_roll_number)

    def test_get_die_number(self):
        """
        PURPOSE: Ensure correct die number mapped list can be returned.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        one_time = 1
        three_times = 3

        # With only 1 die
        game = Game(dice=[die1])
        # 1 time
        actual_die_number = game._get_die_number(times=one_time)
        expected_die_number = [0]
        self.assertEqual(actual_die_number, expected_die_number)
        # 3 times
        actual_die_number = game._get_die_number(times=three_times)
        expected_die_number = [0, 0, 0]
        self.assertEqual(actual_die_number, expected_die_number)

        # With multiple dice 
        game = Game(dice=[die1, die2])
        # 1 time
        actual_die_number = game._get_die_number(times=one_time)
        expected_die_number = [0, 1]
        self.assertEqual(actual_die_number, expected_die_number)
        # 3 times
        actual_die_number = game._get_die_number(times=three_times)
        expected_die_number = [0, 0, 0, 1, 1, 1]
        self.assertEqual(actual_die_number, expected_die_number)

    def test_roll_dice(self):
        """
        PURPOSE: Ensure correct dice rolling results can be returned.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        one_time = 1
        three_times = 3

        # With only 1 die
        game = Game(dice=[die1])
        # 1 time
        actual_face_rolled = game._roll_dice(times=one_time)
        self.assertTrue(actual_face_rolled[0] in faces)
        # 3 times
        actual_face_rolled = game._roll_dice(times=three_times)
        for i in range(three_times * 1):
            self.assertTrue(actual_face_rolled[i] in faces)

        # With multiple dice 
        game = Game(dice=[die1, die2])
        # 1 time
        actual_face_rolled = game._roll_dice(times=one_time)
        for i in range(one_time * 2):
            self.assertTrue(actual_face_rolled[i] in faces)
        # 3 times
        actual_face_rolled = game._roll_dice(times=three_times)
        for i in range(three_times * 2):
            self.assertTrue(actual_face_rolled[i] in faces)

    def test_play(self):
        """
        PURPOSE: Ensure play method returns correct dataframe.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        one_time = 1
        three_times = 3

        # With only 1 die
        game = Game(dice=[die1])
        # 1 time
        game.play(times=one_time)
        actual = game._play_df.drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1],
            'die_number': [0]
        }).set_index('roll_number')
        assert_frame_equal(actual, expected)

        # 3 times
        game.play(times=three_times)
        actual = game._play_df.drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1, 2, 3],
            'die_number': [0, 0, 0]
        }).set_index('roll_number')
        assert_frame_equal(actual, expected)

        # With multiple die
        game = Game(dice=[die1, die2])
        # 1 time
        game.play(times=one_time)
        actual = game._play_df.drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1, 1],
            'die_number': [0, 1]
        }).set_index('roll_number')
        assert_frame_equal(actual, expected)

        # 3 times
        game.play(times=three_times)
        actual = game._play_df.drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1, 2, 3, 1, 2, 3],
            'die_number': [0, 0, 0, 1, 1, 1]
        }).set_index('roll_number')
        assert_frame_equal(actual, expected)

    def test_show_wide(self):
        """
        PURPOSE: Ensure show method returns the dataframe in the correct
            format when display mode is set to wide.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        one_time = 1
        three_times = 3

        # With only 1 die
        game = Game(dice=[die1])
        # 1 time
        game.play(times=one_time)
        actual = game.show(display="wide").drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1],
            'die_number': [0]
        }).set_index(keys=['roll_number', 'die_number']).unstack('die_number')
        self.assertTrue(actual.equals(expected))

        # 3 times
        game.play(times=three_times)
        actual = game.show(display="wide").drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1, 2, 3],
            'die_number': [0, 0, 0]
        }).set_index(keys=['roll_number', 'die_number']).unstack('die_number')
        self.assertTrue(actual.equals(expected))

        # With multiple dice
        game = Game(dice=[die1, die2])
        # 1 time
        game.play(times=one_time)
        actual = game.show(display="wide").drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1, 1],
            'die_number': [0, 1]
        }).set_index(keys=['roll_number', 'die_number']).unstack('die_number')
        self.assertTrue(actual.equals(expected))

        # 3 times
        game.play(times=three_times)
        actual = game.show(display="wide").drop(['face_rolled'], axis=1)
        expected = pd.DataFrame({
            'roll_number': [1, 2, 3, 1, 2, 3],
            'die_number': [0, 0, 0, 1, 1, 1]
        }).set_index(keys=['roll_number', 'die_number']).unstack('die_number')
        self.assertTrue(actual.equals(expected))

    def test_show_narrow(self):
        """
        PURPOSE: Ensure show method returns the dataframe in the correct
            format when display mode is set to narrow.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        one_time = 1
        three_times = 3

        # With only 1 die
        game = Game(dice=[die1])
        # 1 time
        game.play(times=one_time)
        actual = game.show(display="narrow").replace([1, 2, 3, 4, 5, 6], 0)
        expected = pd.DataFrame({
            'roll_number': [1],
            'die_number': [0],
            'face_rolled': [0]
        }).set_index(keys=['roll_number', 'die_number'])
        self.assertTrue(actual.equals(expected))

        # 3 times
        game.play(times=three_times)
        actual = game.show(display="narrow").replace([1, 2, 3, 4, 5, 6], 0)
        expected = pd.DataFrame({
            'roll_number': [1, 2, 3],
            'die_number': [0, 0, 0],
            'face_rolled': [0, 0, 0]
        }).set_index(keys=['roll_number', 'die_number'])
        self.assertTrue(actual.equals(expected))

        # With multiple dice
        game = Game(dice=[die1, die2])
        # 1 time
        game.play(times=one_time)
        actual = game.show(display="narrow").replace([1, 2, 3, 4, 5, 6], 0)
        expected = pd.DataFrame({
            'roll_number': [1, 1],
            'die_number': [0, 1],
            'face_rolled': [0, 0]
        }).set_index(keys=['roll_number', 'die_number'])
        self.assertTrue(actual.equals(expected))

        # 3 times
        game.play(times=three_times)
        actual = game.show(display="narrow").replace([1, 2, 3, 4, 5, 6], 0)
        expected = pd.DataFrame({
            'roll_number': [1, 2, 3, 1, 2, 3],
            'die_number': [0, 0, 0, 1, 1, 1],
            'face_rolled': [0, 0, 0, 0, 0, 0]
        }).set_index(keys=['roll_number', 'die_number'])
        self.assertTrue(actual.equals(expected))


class AnalyzerTestSuite(unittest.TestCase):
    def test_analyzer_initialization(self):
        """
        PURPOSE: Ensure analyzer object is instantiated correctly.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game(dice=[die1, die2])
        analyzer = Analyzer(game=game)
        self.assertEqual(analyzer.game, game)
        self.assertEqual(analyzer.die_face_type, np.int64)

        faces = ['H', 'T']
        die = Die(faces)
        game = Game(dice=[die])
        analyzer = Analyzer(game=game)
        self.assertEqual(analyzer.game, game)
        self.assertEqual(analyzer.die_face_type, str)

        self.assertEqual(analyzer.combos_df, None)
        self.assertEqual(analyzer.jackpots_df, None)
        self.assertEqual(analyzer.face_rolled_occurrences_df, None)

    def test_analyzer_initialization_falsy(self):
        """
        PURPOSE: Instantiation should fail if no dice is detected from the input.
        """
        game = Game(dice=[])
        self.assertRaises(ValueError, Analyzer, game)

    def test_calculate_jackpots(self):
        """
        PURPOSE: Ensure correct number of identical face rolled is returned.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        dice = [die1, die2, die3]
        game = Game(dice=dice)
        game.play(times=3)
        analyzer = Analyzer(game=game)
        num_of_jackpots = analyzer.calculate_jackpots()

        self.assertTrue(isinstance(num_of_jackpots, int))
        self.assertLessEqual(num_of_jackpots, len(dice))

    def test_calculate_combos(self):
        """
        PURPOSE: Ensure correct combos are returned from the method.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        dice = [die1, die2, die3]
        game = Game(dice=dice)
        game.play(times=3)
        analyzer = Analyzer(game=game)
        analyzer.calculate_combos()

        self.assertEqual(analyzer.combos_df.shape, (len(dice), 1))
        self.assertEqual(analyzer.combos_df.ndim, 2)

    def test_ccalculate_face_rolled_occurrences(self):
        """
        PURPOSE: Ensure the transformation happens correctly when unstack face rolled.
        """
        faces = [1, 2, 3, 4, 5, 6]
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        game = Game(dice=[die1, die2, die3])
        game.play(times=3)
        analyzer = Analyzer(game=game)
        analyzer.calculate_face_rolled_occurrences()

        actual_df = analyzer.face_rolled_occurrences_df
        self.assertEqual(list(actual_df.index), [1, 2, 3])


if __name__ == "__main__":
    unittest.main(verbosity=3)
