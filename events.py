from datetime import datetime
import uuid


class ExecutionEvent:

    def __init__(
        self,
        event_type,
        node=None,
        details=None,
        execution_id=None,
        duration_ms=None,
        branch_id=None
    ):
        self.timestamp = datetime.now()

        self.event_type = event_type
        self.node = node
        self.details = details or {}

        self.execution_id = (
            execution_id
            or str(uuid.uuid4())[:8]
        )

        self.duration_ms = duration_ms
        self.branch_id = branch_id

    def __str__(self):

        timestamp = (
            self.timestamp.strftime(
                "%H:%M:%S.%f"
            )[:-3]
        )

        node_name = (
            self.node.name
            if self.node
            else "-"
        )

        duration = (
            f"{self.duration_ms:.2f}ms"
            if self.duration_ms is not None
            else "-"
        )

        branch = self.branch_id or "-"

        return (
            f"[{timestamp}] "
            f"{self.event_type:<18} "
            f"{node_name:<12} "
            f"{branch:<8} "
            f"{duration:<12} "
            f"{self.details}"
        )