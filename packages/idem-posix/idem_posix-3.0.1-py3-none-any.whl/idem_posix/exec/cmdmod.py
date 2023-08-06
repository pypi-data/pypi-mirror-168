import asyncio
import copy
import json
import os
import sys
import traceback
from typing import Any
from typing import Dict
from typing import List

__virtualname__ = "cmd"


def __virtual__(hub):
    return os.name == "posix", "idem-posix only runs on posix systems"


async def run(
    hub,
    cmd: str or List[str],
    cwd: str = None,
    shell: bool = False,
    stdin: str = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    render_pipe: str = None,
    env: Dict[str, Any] = None,
    timeout: int or float = None,
    is_string_output: bool = False,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Execute the passed command and return the output as a string

    :param cmd: The command to run. ex: ``ls -lart /home``

    :param cwd: The directory from which to execute the command. Defaults
        to the home directory of the user specified by ``runas`` (or the user
        under which Salt is running if ``runas`` is not specified).

    :param stdin: A string of standard input can be specified for the
        command to be run using the ``stdin`` parameter. This can be useful in
        cases where sensitive information must be read from standard input.

    :param shell: If ``False``, let python handle the positional
        arguments. Set to ``True`` to use shell features, such as pipes or
        redirection.

    :param stdout:

    :param stderr:

    :param env: Environment variables to be set prior to execution.

        .. note::
            When passing environment variables on the CLI, they should be
            passed as the string representation of a dictionary.

            .. code-block:: bash

                idem exec cmd.run 'some command' env='{"FOO": "bar"}'
    :param render_pipe: The render pipe to use on the output
    :param umask: The umask (in octal) to use when running the command.

    :param timeout: A timeout in seconds for the executed process to return.

    :param is_string_output: Give the output in string format irrespective of format the command executed returns

    CLI Example:

    .. code-block:: bash

        $ idem exec cmd.run "shell command --with-flags" cwd=/home render_pipe=json timeout=10
    """
    ret = dict(
        result=True,
        comment="",
        ret={"retcode": 0, "state": {}, "stdout": b"", "stderr": b""},
    )

    if getattr(sys, "frozen", False):
        env = copy.copy(os.environ.copy())
        # Remove the LOAD LIBRARY_PATH for running commands
        # https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#ld-library-path-libpath-considerations
        env.pop("LD_LIBRARY_PATH", None)  # Linux
        env.pop("LIBPATH", None)  # AIX

    # Run the command
    try:
        if shell:
            proc = await asyncio.create_subprocess_shell(
                cmd, cwd=cwd, stdout=stdout, stderr=stderr, env=env, **kwargs
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                *cmd, *args, cwd=cwd, stdout=stdout, stderr=stderr, env=env, **kwargs
            )
    except Exception as e:
        ret["result"] = False
        ret["ret"]["retcode"] = sys.exc_info()[1].errno
        ret["comment"] = traceback.format_exc()
        ret["ret"]["stderr"] = f"{e.__class__.__name__}: {e}"
        return ret

    # This is where the magic happens
    out, err = await asyncio.wait_for(proc.communicate(input=stdin), timeout=timeout)
    std_out = out.decode()
    if not is_string_output:
        # check if we can parse the output to json.
        try:
            std_out = json.parse(std_out)
        except Exception:
            hub.log.info("command output is not json.")
    ret["ret"]["stdout"] = std_out
    ret["comment"] = ret["ret"]["stderr"] = err.decode()
    ret["ret"]["retcode"] = await asyncio.wait_for(proc.wait(), timeout=timeout)

    if render_pipe:
        block = {"bytes": out}
        rendered = await hub.rend.init.parse_bytes(block, pipe=render_pipe)
        ret["ret"]["state"] = rendered

    return ret
