import copy
import os
from typing import Any
from typing import Dict
from typing import List

__virtualname__ = "cmd"


def __virtual__(hub):
    return os.name == "posix", "idem-posix only runs on posix systems"


async def run(
    hub,
    ctx,
    name: str,
    cmd: str or List[str],
    cwd: str = None,
    shell: bool = False,
    env: Dict[str, Any] = None,
    umask: str = None,
    timeout: int or float = None,
    render_pipe: str = None,
    is_string_output: bool = False,
    **kwargs,
) -> Dict[str, Any]:
    """
    Run a command.

    :param hub:
    :param ctx:
    :param name: The state name
    :param cmd: The command to execute, remember that the command will execute with the path and permissions of the salt-minion.
    :param cwd: The current working directory to execute the command in, defaults to None
    :param shell: Run the command in the shell
    :param env:
    :param umask: The umask (in octal) to use when running the command.
    :param timeout: If the command has not terminated after timeout seconds, send the subprocess sigterm, and if sigterm is ignored, follow up with sigkill
    :param render_pipe: The render pipe to use on the output
    :param is_string_output: Give the output in string format irrespective of format the command executed returns
    :param kwargs: kwargs that will be forwarded to subprocess.Popen

    .. code-block:: sls

        my_state_name:
          cmd.run:
            cmd: ls -l
            cwd: /
            shell: False
            env:
              ENV_VAR_1: ENV_VAL_1
              ENV_VAR_2: ENV_VAL_2
            timeout: 100
            render_pipe:
            kwargs:

    The "new_state" will have the following keys:

        "stdout": The plaintext output of the command
        "stderr": The plaintext error/logging output of the command
        "retcode": The returncode from the command
        "state": The output as rendered from the render_pipe (if one was given), for use in arg_binding
    """
    ret = {
        "name": name,
        "result": True,
        "comment": "",
        "old_state": ctx.get("old_state", {}),
        "new_state": {},
    }

    # Need the check for None here, if env is not provided then it falls back
    # to None and it is assumed that the environment is not being overridden.
    if env is not None and not isinstance(env, (list, dict)):
        ret["result"] = False
        ret["comment"] = "Invalidly-formatted 'env' parameter. See " "documentation."
        return ret

    cmd_kwargs = copy.deepcopy(kwargs)
    cmd_kwargs.update(
        {
            "cwd": cwd,
            "shell": shell,
            "env": env,
            "umask": umask,
        }
    )

    if cwd and not os.path.isdir(cwd):
        ret["result"] = False
        ret["comment"] = f'Desired working directory "{cwd}" ' "is not available"
        return ret

    if ctx["test"]:
        ret["comment"] = f'Command "{cmd}" would have been executed'
        return ret

    cmd_ret = await hub.exec.cmd.run(
        cmd=cmd,
        timeout=timeout,
        python_shell=True,
        render_pipe=render_pipe,
        is_string_output=is_string_output,
        **cmd_kwargs,
    )

    ret["new_state"] = cmd_ret.ret
    ret["result"] = cmd_ret.result
    ret["comment"] = (
        cmd_ret.comment,
        f"stdout: {cmd_ret.ret['stdout']}",
        f"stderr: {cmd_ret.ret['stderr']}",
        f"retcode: {cmd_ret.ret['retcode']}",
    )

    return ret
