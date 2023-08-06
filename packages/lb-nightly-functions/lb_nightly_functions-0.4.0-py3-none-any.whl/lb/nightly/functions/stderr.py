import asyncio
import cmd
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from py import process

stdout = b""
stderr = b""


async def _stream_to_file(name, stream):
    global stdout
    global stderr
    with open("aout.log", "a", buffering=512) as f:
        while line := await stream.readline():
            if name == "stdout":
                stdout += line
            elif name == "stderr":
                stderr += line
            line = line.decode(errors="surrogateescape")
            f.write(line.strip())


async def _run_sub(cmd):
    process = await asyncio.create_subprocess_exec(
        *cmd,
        limit=8192 * 16,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    await asyncio.gather(
        _stream_to_file("stdout", process.stdout),
        _stream_to_file("stderr", process.stderr),
        process.wait(),
    )


def mycmd():
    sys.stdout.buffer.write("this is stdout")
    sys.stderr.buffer.write("this is stderr")
    return 0


def log_popen_pipe(p, pipe_name):
    result = b""
    while p.poll() is None:
        line = getattr(p, pipe_name).readline()
        result += line
        try:
            line = line.decode().strip()
        except UnicodeDecodeError:
            line = repr(line)
        if line:
            yield line
            # f.write(line)
        #     print(f"cmd {pipe_name}: {line}")
    # return result


def iter_log_popen_pipe(p, pipe_name):
    with open("output.log", "a", buffering=512) as f:
        for i in log_popen_pipe(p, pipe_name):
            f.write(i)


def logging_subprocess_run(cmd):
    with subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as p, ThreadPoolExecutor(2) as pool:
        stdout = pool.submit(iter_log_popen_pipe, p, "stdout")
        stderr = pool.submit(iter_log_popen_pipe, p, "stderr")
        stdout = stdout.result()
        stderr = stderr.result()
    return subprocess.CompletedProcess(cmd, p.returncode, stdout, stderr)


def singularity():
    # from spython.main import Client

    # Client.load("/cvmfs/cernvm-prod.cern.ch/cvm4")
    # # script = f"""#!/bin/bash
    # # echo "This is stdout"
    # # >&2 echo "This is stderr"
    # # {"exit 1" if return_code else ""}
    # # """
    # cmd = [
    #     # sys.executable,
    #     # "-c",
    #     # "import sys; sys.stdout.write(b'out'); sys.stderr.write(b'e'*66000); sys.exit(0)",
    #     "python",
    #     "mycmd.py",
    #     # "lb.nightly.functions.stderr",
    #     # "mycmd",
    # ]
    # # cmd = ["ls"]
    # result = Client.execute(
    #     cmd,
    #     bind=[
    #         "/cvmfs",
    #     ],
    #     stream=True,
    # )
    # with open("output.log", "w", buffering=512) as f:
    #     with redirect_stderr(f):
    #         for line in result:
    #             f.write(line)

    cmd = [
        "singularity",
        "exec",
        "--bind",
        "/cvmfs",
        "/cvmfs/cernvm-prod.cern.ch/cvm4",
        "python",
        "mycmd.py",
    ]

    # with open("output.log", "w", buffering=512) as f:
    #     with redirect_stderr(f):
    #         for line in result:
    #             f.write(line)

    # logging_subprocess_run(cmd)

    asyncio.run(_run_sub(cmd))
    global stderr
    print(stderr)


if __name__ == "__main__":  # pragma: no cover
    globals()[sys.argv[1]](*sys.argv[2:])
