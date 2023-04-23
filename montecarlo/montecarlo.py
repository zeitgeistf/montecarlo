import numbers
import random

import numpy as np
import pandas as pd


DEFAULT_WEIGHT = 1.0


class Die:
    """
    A die has N sides, or "faces", and W weights, and can be rolled to select a face.

    Methods:
        - update_weight
        - roll
        - show
    """
    def __init__(self, faces: list[str | float]) -> None:
        self._die_df = pd.DataFrame({
            "faces": faces, 
            "weights": [DEFAULT_WEIGHT for _ in faces]
        })

    def update_weight(self, face: str | float, new_weight: float) -> None:
        """
        PURPOSE: This method is used to change the weight of a single side. Errors
            out if input validation fails.
        INPUT:
            1. face str | float
            2. new_weight float
        OUTPUT: None
        """
        if not face in list(self._die_df.faces):
            raise ValueError(f"Face value {face} not found in the die faces. {list(self._die_df.faces)}")

        if not isinstance(new_weight, numbers.Number):
            raise ValueError(f"New weight {new_weight} is not an instance of number.")

        index = self._die_df.faces.index[self._die_df.faces == face].to_list()[0]
        self._die_df.loc[index, 'weights'] = new_weight

    def roll(self, times=1) -> list[str | float]:
        """
        PURPOSE: this method rolss the die one or more times.
        INPUT: times int
        OUTPUT: list
        """
        return [
            random.choices(
                population=self._die_df.faces, 
                weights=self._die_df.weights, 
                k=1
            )[0]
            for i in range(times)
        ]

    def show(self) -> pd.DataFrame:
        """
        PURPOSE: This method returns the current set of faces and weights belong
            to the die.
        INPUT: None
        OUTPUT: dataframe
        """
        return self._die_df


class Game:
    """
    A game consists of rolling of one or more dice of the same kind one or more times.

    Methods:
        - _get_roll_number
        - _get_die_number
        - _roll_dice
        - play
        - show
    """
    def __init__(self, dice: list[Die]) -> None:
        self.dice = dice
        self._play_df = pd.DataFrame({})

    def _get_roll_number(self, times: int) -> list[int]:
        """
        PURPOSE: This method maps out the roll numbers base on the number of
            times user asks to roll and how many dice there are.
        INPUT: times int
        OUTPUT: list of int
        """
        return [x for _ in self.dice for x in range(1, times + 1)]

    def _get_die_number(self, times: int) -> list[int]:
        """
        PURPOSE: This method maps out the indices base on the die list index position
            from the list passed in during instantiation.
        INPUT: times int
        OUTPUT: list of int
        """
        return [index for index, _ in enumerate(self.dice) for _ in range(times)]

    def _roll_dice(self, times: int) -> list[str | float]:
        """
        PURPOSE: This method go through each die passed in the die list and roll the
            die as many times as specified until the die list is exhausted.
        INPUT: times int
        OUTPUT: list of number or string
        """
        results = []
        for die in self.dice:
            results.extend(die.roll(times=times))
        return results

    def play(self, times: int) -> None:
        """
        PURPOSE: This method will roll the dice passed in as many time as specified, and
            save the result to the instance object for future usage.
        INPUT: times int
        OUTPUT: None

        EXAMPLE: 2 dice with 6 faces roll 3 times

        roll number (index) |  die number | face rolled
                1                  0               2
                2                  0               3
                3                  0               6
                1                  1               2
                2                  1               1
                3                  1               4
        """
        roll_number = self._get_roll_number(times)
        die_number = self._get_die_number(times)
        face_rolled = self._roll_dice(times)

        self._play_df = pd.DataFrame({
            'roll_number': roll_number,
            'die_number': die_number,
            'face_rolled': face_rolled
        }).set_index('roll_number')

    def show(self, display: str = "wide") -> pd.DataFrame:
        """
        PURPOSE: This method returns to the user the results of most recent plays
            either in narrow or wide form
        INPUT: display string
        OUTPUT: Pandas dataframe

        EXAMPLE: 2 dice with 6 faces roll 3 times

        roll number (index) |  die number | face rolled
                1                  0               2
                2                  0               3
                3                  0               6
                1                  1               2
                2                  1               1
                3                  1               4
        
        NARROW: The narrow form of the dataframe will have a two-column index with the roll number
        and the die number, and a column for the face rolled.

        roll number (index) |  die number (index) | face rolled
                1                  0                      2
                2                  0                      3
                3                  0                      6
                1                  1                      2
                2                  1                      1
                3                  1                      4

        WIDE: The wide form of the dataframe will have a single column index with the roll number,
        and each die number as a column.

                die number  |        0      |      1
        roll number (index) |  face rolled  |  face rolled
                1                    2             2
                2                    3             1
                3                    6             4
        """
        if display.lower() not in ("wide", "narrow"):
            raise ValueError(
                f"Incorrect display value passed in: {display}, should be either \"wide\" or \"narrow\".")

        narrow_df = self._play_df.set_index('die_number', append=True)

        return  narrow_df \
            if display.lower() == 'narrow' else narrow_df.unstack('die_number')

class Analyzer:
    """
    An analyzer takes the results of a single game and computes various descriptive statistical properties
    about it. These properties results are available as attributes of an Analyzer object.

    Methods:
        - calculate_jackpots
        - calculate_combos
        - calculate_face_rolled_occurrences
    """
    def __init__(self, game: Game) -> None:
        self.game = game
        self.num_of_dice = len(self.game.dice)
        if self.num_of_dice < 1:
            raise ValueError("Incorrect number of dice detected, please double check and try again.")
        self.die_face_type = type(self.game.dice[0].show()['faces'][0])
        self.combos_df = None
        self.jackpots_df = None
        self.face_rolled_occurrences_df = None

    def calculate_jackpots(self) -> int:
        """
        PURPOSE: This method computes how many times the game resulted in all faces being identical.
        INPUT: None
        OUTPUT: int

        STEP 0 (original narrow dataframe generated from game class)
        roll number (index) |  die number (index) | face rolled
                1                  0                      2
                2                  0                      3
                3                  0                      6
                1                  1                      2
                2                  1                      1
                3                  1                      4

        STEP 1 (group by roll number and face rolled to get num of occurances for each combo)
        roll number (index) |  face rolled (index) |  occurrences
                1                  2                      2
                2                  1                      1
                                   3                      1
                3                  4                      1
                                   6                      1
    
        STEP 2 (only take the rows with with ocurrances equals to the number of dice)                            
        roll number (index) |  face rolled (index) |  occurrences
                1                  2                      2
        """
        occurrences_df = self.game.show(display='narrow') \
            .reset_index() \
            .groupby(by=['roll_number', 'face_rolled']) \
            .size() \
            .to_frame('occurrences')

        self.jackpots_df = occurrences_df[occurrences_df['occurrences'] == self.num_of_dice]
        return self.jackpots_df.shape[0]
        
    def calculate_combos(self) -> None:
        """
        PURPOSE: This method computes the distinct combinations of faces rolled, along with their counts,
            where combinations are sorted and saved as a multi-columned index
        INPUT: None
        OUTPUT: None

        STEP 0 (original narrow dataframe generated from game class)
        roll number (index) |  die number (index) | face rolled
                1                  0                      2
                2                  0                      3
                3                  0                      6
                1                  1                      2
                2                  1                      1
                3                  1                      4

        STEP 1 (group by roll number and aggregate all the face rolled within each "row" into a set 
            with only distinct values)
                    face_rolled
        roll_number
        1             {2}
        2             {1, 3}
        3             {4, 6}
    
        STEP 2 (conduct another group by on the indexed face rolled set and count their occurrences)
                     ocurrances
        face_rolled
        {2}               1
        {1, 3}            1
        {4, 6}            1
        """
        self.combos_df = self.game.show(display='narrow') \
            .groupby('roll_number') \
            .agg({'face_rolled': set}) \
            .astype({'face_rolled': 'str'}) \
            .groupby('face_rolled') \
            .size() \
            .to_frame('occurrences') \
            .sort_values('occurrences', ascending=False)

    def calculate_face_rolled_occurrences(self) -> None:
        """
        PURPOSE: This method computes how many times a given face is rolled in each event.
        INPUT: None
        OUTPUT: None

        SAVED DF STRUCTURE:
               face rolled  |   1   |   2   |   3   |   4   |   5   |   6   |
        roll number (index) |  
                1               0       2       0       0       0       0
                2               1       0       1       0       0       0
                3               0       0       0       1       0       1
        """
        self.face_rolled_occurrences_df = self.game.show(display='narrow') \
            .reset_index() \
            .groupby(by=['roll_number', 'face_rolled']).size() \
            .unstack('face_rolled') \
            .fillna(0)
