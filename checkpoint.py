import json
import os


class CheckpointStore:

    def __init__(self, directory="checkpoints"):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def load(self, execution_id):

        path = os.path.join(
            self.directory,
            f"{execution_id}.json"
        )

        if not os.path.exists(path):
            return None

        with open(path, "r") as file:
            return json.load(file)

    def save(
    self,
    execution_id,
    ready,
    waiting,
    terminal_state,
    steps
):
        checkpoint = {
            "execution_id": execution_id,
            "ready": [
                {
                    "node": node.name,
                    "state": state,
                    "branch_id": branch_id
                }
                for node, state, branch_id in ready
            ],
            "waiting": {
                node.name: states
                for node, states in waiting.items()
            },
            "terminal_state": terminal_state,
            "steps": steps
        }

        path = os.path.join(
            self.directory,
            f"{execution_id}.json"
        )

        with open(path, "w") as file:
            json.dump(
                checkpoint,
                file,
                indent=2,
                default=str
            )

        print("  Checkpoint saved")