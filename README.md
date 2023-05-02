# Monte Carlo Simulator 🧮

This package contains a broad class of computational algorithms that rely on repeated random sampling to obtain numerical results. The underlying concept is to use randomness to solve problems that might be deterministic in principle.

Author: https://github.com/zeitgeistf

## Setup 🚧

### Installation 🔨
In order to run the program, package need to be installed first by running the following commmand
```bash
cd montecarlo
pip install -e .
```

### Testing 🧪
To run unit tests, use the following command at root level directory
```bash
python tests/montecarlo_tests.py
```

### Importing 🔪
Once the program is installed, the modules need to be imported into another script or program first in order to be used.
(Alternative way to avoid creating new script is playaround the package using the "motecarlo_demo.ipynb" notebook located in the root folder)
```bash
from montecarlo import Analyzer, Die, Game
```

### Dice Creation 🎲

```python
faces = [1, 2, 3, 4, 5, 6]
die = Die(faces)
```

### Game Play 🎯
```python
game = Game(dice=[die, die])
game.play(times=3)
```

### Analytics 🗺️
```python
analyzer = Analyzer(game=game)
analyzer.calculate_jackpots()
```

## API Documentation 📖

Class: 
- **Die**: A die has N sides, or "faces", and W weights, and can be rolled to select a face.
    Methods:
    - **update_weight**: This method is used to change the weight of a single side. Errors out if input validation fails.
        - Input:
            - face: string
            - new_weight: float
        - Output: None
    - **roll**: This method rolss the die one or more times.
        - Input:
            - times: integer (default: 1)
        - Output: list[string or float]
    - **show**: This method returns the current set of faces and weights belong to the die.
        - Input: None
        - Output: dataframe
- **Game**: A game consists of rolling of one or more dice of the same kind one or more times.

    Attributes:
    - dice: list[Die]

    Methods: 
    - **play**: This method will roll the dice passed in as many time as specified, and save the result to the instance object for future usage.
        - Input:
            - times: integer
        - Output: None
    - **show**: This method returns to the user the results of most recent plays either in narrow or wide form
        - Input:
            - display: string (default: wide)
        - Output: None

- **Analyzer**: An analyzer takes the results of a single game and computes various descriptive statistical properties about it. These properties results are available as attributes of an Analyzer object.

    Attributes:
    - game: Game
    - num_of_dice: integer
    - die_face_type: string or float
    - combos_df: dataframe
    - jackpots_df dataframe
    - face_rolled_ocurrences_df: dataframe

    Methods:
    - **calculate_jackpots**: This method computes how many times the game resulted in all faces being identical.
        - Input: None
        - Output: integer
    - **calculate_combos**: This method computes the distinct combinations of faces rolled, along with their counts where combinations are sorted and saved as a multi-columned index
        - Input: None
        - Output: None
    - **calculate_face_rolled_occurrences**: This method computes how many times a given face is rolled in each event.
        - Input: None
        - Output: None
    

## Project Structure ⛩️

    ├── assets
    │   ├── FinalProjectInstructions.pdf
    │   ├── FinalProjectSubmissionTemplate.ipynb
    ├── montecarlo                  
    │   ├── __init__.py
    │   ├── montecarlo.py
    ├── tests
    │   ├── __init__.py
    │   ├── montecarlo_tests.py
    ├── .gitignore
    ├── LICENSE
    ├── montecarlo_demo.ipynb
    ├── README.md
    ├── setup.py
    └── test_output.txt
