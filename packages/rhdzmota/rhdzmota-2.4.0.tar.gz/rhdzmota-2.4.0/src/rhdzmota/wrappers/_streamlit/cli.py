import os
import sys
import textwrap
import datetime as dt
from typing import Optional

from rhdzmota.utils.misc import create_temporal_file


class StreamlitCLIWrapper:

    def __init__(self):
        import importlib
        from importlib.metadata import version

        self.version = version("streamlit")
        self.module = importlib.import_module(
            "streamlit.web.cli" if self.version > "1.11.1" else "streamlit.cli"
        )
        self.created_at = dt.datetime.utcnow()
        self.updated_at: Optional[dt.datetime] = None

    def run_from_file(self, filepath: str):
        if not os.path.exists(filepath):
            raise ValueError("Target script does not exists: %s", filepath)
        sys.argv = ["streamlit", "run", filepath]
        self.module.main()
        self.updated_at = dt.datetime.utcnow()
        return f"Execution time(s): {(self.created_at - self.updated_at).total_seconds()}"

    def run_from_content(self, content: str, path: Optional[str] = None):
        filepath = create_temporal_file(
            content=content,
            suffix=".py",
            path=path,
        )
        return self.run_from_file(filepath=filepath)

    def execute_function(self, function_name: str, module_name: str, temp_filepath: Optional[str] = None):
        return self.run_from_content(
            content=textwrap.dedent(
                f"""
                from {module_name} import {function_name}

                if __name__ == "__main__":
                    {function_name}()
                """
            ),
            path=temp_filepath
        )

    def execute_hello_world(self):
        return self.execute_function(
            function_name="hello_world",
            module_name="rhdzmota.wrappers._streamlit.example_views"
        )
