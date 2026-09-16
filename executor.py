from collections import deque
from concurrent.futures import ThreadPoolExecutor
import uuid
import time
from checkpoint import CheckpointStore
from events import ExecutionEvent


class GraphExecutor:

    def __init__(
        self,
        graph,
        max_steps=50,
        max_workers=4,
        execution_id=None
    ):
        self.graph = graph
        self.max_steps = max_steps
        self.max_workers = max_workers
        self.events = []

        self.execution_id = (
            execution_id
            or str(uuid.uuid4())[:8]
        )

        self.checkpoint_store = CheckpointStore()

    def run(
        self,
        start_node,
        state=None,
        branch_id=None
    ):

        if state is None:
            state = {}

        if branch_id is None:
            branch_id = str(uuid.uuid4())[:6]


        ready = deque()

        ready.append(
            (   
                start_node,
                state,
                branch_id
            )
        )

        waiting = {}

        terminal_state = state

        steps = 0

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            while ready:

                # ------------------------------------------------
                # 1. Take the current batch of ready nodes
                # ------------------------------------------------

                batch = []

                while ready:
                    batch.append(
                        ready.popleft()
                    )

                # ------------------------------------------------
                # 2. Execute the batch concurrently
                # ------------------------------------------------

                futures = [
                    executor.submit(
                        self._execute_node,
                        node,
                        node_state,
                        branch_id
                    )
                    for node, node_state, branch_id in batch
                ]

                results = [
                    future.result()
                    for future in futures
                ]

                # ------------------------------------------------
                # 3. Process results and schedule next nodes
                # ------------------------------------------------

                for node, current_state, branch_id, error in results:

                    steps += 1

                    if steps > self.max_steps:
                        raise RuntimeError(
                            f"Graph execution exceeded "
                            f"maximum of {self.max_steps} steps"
                        )

                    edges = self._get_matching_edges(
                        node,
                        current_state,
                        error
                    )

                    # ------------------------------------------------
                    # Terminal node
                    # ------------------------------------------------

                    if not edges:

                        terminal_state = current_state

                        continue

                    # ------------------------------------------------
                    # Schedule outgoing edges
                    # ------------------------------------------------

                    for edge in edges:

                        target = edge.target

                        next_branch_id = branch_id

                        if len(edges) > 1:
                            next_branch_id = str(uuid.uuid4())[:6]

                        self._emit(
                            "BranchCreated",
                            node,
                            details={
                                "target": target.name
                            },
                            branch_id=next_branch_id
                        )

                        # ------------------------------------------------
                        # Fan-in / Join
                        # ------------------------------------------------

                        if getattr(
                            target,
                            "is_join",
                            False
                        ):

                            if target not in waiting:
                                waiting[target] = []

                            waiting[target].append(
                                current_state.copy()
                            )

                            received = len(
                                waiting[target]
                            )

                            required = target.expected_branches

                            print(
                                f"  {target.name}: "
                                f"received "
                                f"{received}/{required} branches"
                            )

                            self._emit(
                                "JoinWaiting",
                                target,
                                {
                                    "received": received,
                                    "required": required
                                },
                                branch_id=branch_id
                            )

                            if received < required:
                                continue

                            print(
                                f"  {target.name}: "
                                f"all branches completed"
                            )

                            merged_state = (
                                self._merge_states(
                                    waiting[target]
                                )
                            )

                            del waiting[target]

                            # Create ONE new branch identity
                            # for the merged execution.
                            merged_branch_id = str(uuid.uuid4())[:6]

                            self._emit(
                                "JoinCompleted",
                                target,
                                details={
                                    "branches": required
                                },
                                branch_id=merged_branch_id
                            )

                            ready.append(
                                (
                                    target,
                                    merged_state,
                                    merged_branch_id
                                )
                            )

                        # ------------------------------------------------
                        # Normal edge
                        # ------------------------------------------------

                        else:


                            ready.append(
                                (
                                    target,
                                    current_state.copy(),
                                    next_branch_id
                                )
                            )

            self._save_checkpoint(
                ready,
                waiting,
                terminal_state,
                steps
            )
        if waiting:
            unresolved = [
                node.name
                for node in waiting
            ]

            raise RuntimeError(
                f"Workflow ended with unresolved joins: "
                f"{unresolved}"
            )

        self._emit(
            "WorkflowCompleted",
            details={"steps": steps}
        )

        return terminal_state

    def _execute_node(
    self,
    node,
    state,
    branch_id
):
        self._emit(
            "NodeStarted",
            node,
            branch_id=branch_id
        )

        print(f"Executing {node.name}")

        start_time = time.perf_counter()

        try:
            result = node.execute(state)

            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            self._emit(
                "NodeCompleted",
                node,
                branch_id=branch_id,
                duration_ms=duration_ms
            )

            return node, result, branch_id, None

        except Exception as exc:

            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            self._emit(
                "NodeFailed",
                node,
                details={
                    "error": str(exc)
                },
                branch_id=branch_id,
                duration_ms=duration_ms
            )

            return node, state, branch_id, exc

    

    def _get_matching_edges(self, node, state, error=None):
        edges = self.graph.get_outgoing_edges(node)

        matching = []

        for edge in edges:

            if edge.condition is None:
                matching.append(edge)
                continue

            try:
                if edge.condition(state, error):
                    matching.append(edge)
            except TypeError:
                if edge.condition(state):
                    matching.append(edge)

        return matching

    def _get_incoming_edges(self, node):

        return [
            edge
            for edge in self.graph.edges
            if edge.target == node
        ]

    def _merge_states(self, states):

        merged = {}

        for state in states:

            for key, value in state.items():

                if key == "branches":
                    continue

                merged[key] = value

        merged["branches"] = states

        return merged

    def _emit(
    self,
    event_type,
    node=None,
    details=None,
    duration_ms=None,
    branch_id=None
):

        event = ExecutionEvent(
            event_type=event_type,
            node=node,
            details=details,
            execution_id=self.execution_id,
            duration_ms=duration_ms,
            branch_id=branch_id
        )

        self.events.append(event)

    def load_checkpoint(self):
        checkpoint = self.checkpoint_store.load(
            self.execution_id
        )

        if checkpoint is None:
            return None

        print(
            f"Resuming from node: "
            f"{checkpoint['node']}"
        )

        return checkpoint


    def _find_node(self, name):
        for node in self.graph.nodes:
            if node.name == name:
                return node

        raise ValueError(
            f"Node not found: {name}"
        )

    def resume(self):

        checkpoint = self.load_checkpoint()

        if checkpoint is None:
            raise RuntimeError(
                "No checkpoint found"
            )

        node = self._find_node(
            checkpoint["node"]
        )

        state = checkpoint["state"]
        branch_id = checkpoint["branch_id"]

        edges = self._get_matching_edges(
            node,
            state
        )

        if not edges:
            return state

        # Resume from the next node
        next_node = edges[0].target

        return self.run(
            next_node,
            state=state,
            branch_id=branch_id
        )

    def _save_checkpoint(
    self,
    ready,
    waiting,
    terminal_state,
    steps
):
        self.checkpoint_store.save(
            execution_id=self.execution_id,
            ready=ready,
            waiting=waiting,
            terminal_state=terminal_state,
            steps=steps
        )