# Drone navigation using Gymnasium environment
For more implementation details pelase consult the [report](Report.md).
## Overview
`DroneNavigation` is a custom environment for OpenAI Gym that simulates a drone navigating from one point to another within a defined area. This environment is designed to help develop and compare reinforcement learning algorithms by providing a platform where a drone agent learns to reach a target destination efficiently while avoiding boundaries.


## Installation

### Prerequisites
Before installing the `DroneNavigation` environment, ensure you have the following:
- Python 3.6+
- pip
- virtualenv (optional, but recommended)

### Setup Environment
It's recommended to use a virtual environment to keep dependencies required by different projects separate and to avoid potential conflicts:
```bash
python -m venv drone-env
source drone-env/bin/activate  # On Unix/macOS
drone-env\Scripts\activate  # On Windows
```

### Install Dependencies
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Program

The DroneNavigation program supports different modes of operation, allowing users to train, evaluate, or render the drone's navigation in the environment. Follow the steps below to run the program in the desired mode.

### Usage

You can run the program in one of three modes: `train`, `eval`, or `render`. Each mode is selected via command-line arguments:

- **Train**: This mode trains the drone using the reinforcement learning algorithm implemented in the training script.
- **Evaluate**: This mode evaluates the performance of the trained model.
- **Render**: This mode visually renders the drone's navigation.

To run the program, use the following command structure in your terminal from the `src ` directory:

```bash
python main.py --mode [mode]
Replace [mode] with either train, eval, or render depending on your needs:
```
#### Examples:
##### To train the drone:
```bash
python main.py --mode train
```
This command starts the training process of the drone within the environment.
##### To evaluate the drone:
```bash
python main.py --mode eval
```
Use this command to evaluate the drone's performance by running 100 episodes cand calculating its landing rate. 
This does not render the environment visually.
##### To render the drone's navigation:
```bash
python main.py --mode render
```
This command will visually render 10 episodes of the drone's navigation in the environment, showing how the drone moves towards the target based on its training.
