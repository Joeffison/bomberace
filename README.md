# Bomberace
Personal project recreating my favorite childhood game using Pygame. This fan-made project is intended for learning and educational purposes only (practicing Pygame), and is not authorized for commercial use.

Please do not redistribute the assets, images, sounds, music, content, etc. without authorization.

## Setup

### Prerequisites
- asdf (recommended)
  - **note:** alternatively you can install poetry and python yourself,
however in that case you have to check pyproject.toml for the appropriate
python version and you must use `poetry install` instead of `make setup`.
- download all free assets that do not allow redistribution
    1. Create a directory free-no-redistribution inside of [assets](assets)
    2. Please go to https://craftpix.net/freebies/free-robot-sprite/?num=3&count=39&sq=bomb&pos=2
    3. Download and uncompress the assets
    4. Move the resulting directory as is to [assets/free-no-redistribution](assets/free-no-redistribution)


1. install all dependencies and create the virtual environment with
    ```sh
    make setup
    ```

**note:** If you are going to run tests and contribute to this project,
please run the command below instead:
```sh
make setup-dev
```


## How to play

1. Make sure you setup the game (one-time step)
2. run the game with:
    ```sh
    make play
    ```

Checkout the recording below:

https://github.com/user-attachments/assets/2730215f-1d21-4033-83ce-7fc35394c846

or [here](docs/videos/bomberace_v0.mov "The player destroying some brick walls")


## Contributing

Please reach out to me in case you would like to contribute.
Before you get started, please see [Setup](#setup) for setting up the project.

### testing

1. Run all tests with:
    ```sh
    make test
    ```
