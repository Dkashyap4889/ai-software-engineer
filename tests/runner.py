class TestRunner:

    def __init__(self, command_runner):
        self.command_runner = command_runner

    def run(self, test_cases, project_directory):
        results = []

        for test_case in test_cases:

            if test_case.type == "structural":
                result = self.run_structural(
                    test_case,
                    project_directory
                )

            elif test_case.type == "build":
                result = self.run_build(
                    test_case,
                    project_directory
                )

            elif test_case.type == "behavioral":
                result = self.run_behavioral(
                    test_case,
                    project_directory
                )

            else:
                result = {
                    "success": False,
                    "error": f"Unknown test type: {test_case.type}"
                }

            results.append({
                "test": test_case.model_dump(),
                "result": result
            })

            if not result["success"]:
                return results

        return results