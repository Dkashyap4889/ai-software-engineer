from pathlib import Path


class FileWriter:

    def __init__(self, root_directory="generated_app"):
        self.root_directory = Path(root_directory)

    def write_files(self, files):

        written_files = []

        for file in files:

            path = self.root_directory / file.path

            # Prevent paths such as ../../something
            resolved_path = path.resolve()
            root = self.root_directory.resolve()

            if root not in resolved_path.parents and resolved_path != root:
                raise RuntimeError(
                    f"Unsafe file path: {file.path}"
                )

            resolved_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            resolved_path.write_text(
                file.content,
                encoding="utf-8"
            )

            written_files.append(
                str(resolved_path)
            )

        return written_files