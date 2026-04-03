"""
SSH/SFTP operations on target hosts via Paramiko.
All methods are sync (run in thread pool via asyncio.to_thread).
"""
import io
import logging
import os
import stat
import time
from pathlib import Path
import paramiko
from models.application import Application

logger = logging.getLogger(__name__)


def _build_client(app: Application, retries: int = 3) -> paramiko.SSHClient:
    """Build SSH client with retry mechanism."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connect_kwargs: dict = {
        "hostname": app.ssh_host,
        "port": app.ssh_port,
        "username": app.ssh_user,
        "timeout": 10,
    }

    if app.ssh_auth_type == "KEY" and app.ssh_key_path:
        connect_kwargs["key_filename"] = app.ssh_key_path
    else:
        connect_kwargs["password"] = app.ssh_password or ""

    last_error = None
    for attempt in range(retries):
        try:
            client.connect(**connect_kwargs)
            return client
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(1)
    raise last_error

def test_connection(app: Application) -> dict:
    """Test SSH connectivity and return result dict."""
    try:
        client = _build_client(app)
        _, stdout, _ = client.exec_command("echo ok")
        out = stdout.read().decode().strip()
        client.close()
        return {"success": out == "ok", "message": "SSH connection successful"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def discover_pid(app: Application) -> int | None:
    """Discover JVM PID by jar name using jps (with ps aux fallback)."""
    if not app.java_jar_name:
        print(f"[discover_pid] java_jar_name is None, returning early", flush=True)
        return None
    try:
        client = _build_client(app)
        jar = app.java_jar_name
        _, stdout, stderr = client.exec_command(f"pgrep -f '{jar}'")
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        client.close()
        print(f"[discover_pid] jar={jar!r} out={out!r} err={err!r}", flush=True)
        for line in out.splitlines():
            line = line.strip()
            if line.isdigit():
                return int(line)
    except Exception as e:
        print(f"[discover_pid] exception: {e}", flush=True)
    return None


def push_file(app: Application, local_path: str, remote_path: str) -> None:
    """SCP a local file to the target host."""
    client = _build_client(app)
    sftp = client.open_sftp()
    try:
        remote_dir = str(Path(remote_path).parent)
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            _mkdir_p(sftp, remote_dir)
        sftp.put(local_path, remote_path)
    finally:
        sftp.close()
        client.close()


def push_content(app: Application, content: str, remote_path: str) -> None:
    """Push string content as a file to the target host."""
    client = _build_client(app)
    sftp = client.open_sftp()
    try:
        remote_dir = str(Path(remote_path).parent)
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            _mkdir_p(sftp, remote_dir)
        with sftp.open(remote_path, "w") as f:
            f.write(content)
    finally:
        sftp.close()
        client.close()


def run_command(app: Application, command: str, timeout: int = 30) -> tuple[int, str, str]:
    """Run a remote command; return (exit_code, stdout, stderr)."""
    client = _build_client(app)
    _, stdout, stderr = client.exec_command(command, timeout=timeout)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return exit_code, out, err


def list_remote_files(app: Application, remote_dir: str, since_ts: float | None = None) -> list[str]:
    """List recording files in the remote directory.
    If since_ts is given (unix timestamp), only return files modified at or after that time.
    """
    client = _build_client(app)
    sftp = client.open_sftp()
    try:
        try:
            attrs = sftp.listdir_attr(remote_dir)
        except FileNotFoundError:
            attrs = []
    finally:
        sftp.close()
        client.close()
    result = []
    for a in attrs:
        if a.filename.startswith("."):
            continue
        if since_ts is not None and (a.st_mtime or 0) < since_ts:
            continue
        result.append(a.filename)
    return result


def pull_file_content(app: Application, remote_path: str) -> bytes:
    """Read a remote file and return its raw bytes."""
    client = _build_client(app)
    sftp = client.open_sftp()
    with sftp.open(remote_path, "rb") as f:
        content = f.read()
    sftp.close()
    client.close()
    return content


def clear_remote_dir(app: Application, remote_dir: str) -> int:
    """Delete all non-hidden files in a remote directory. Returns count of deleted files."""
    client = _build_client(app)
    sftp = client.open_sftp()
    deleted = 0
    try:
        attrs = sftp.listdir_attr(remote_dir)
        for a in attrs:
            if not a.filename.startswith("."):
                try:
                    sftp.remove(f"{remote_dir}/{a.filename}")
                    deleted += 1
                except Exception:
                    pass
    except FileNotFoundError:
        pass
    finally:
        sftp.close()
        client.close()
    return deleted


def delete_remote_file(app: Application, remote_path: str) -> None:
    """Delete a single file on the remote host via SFTP."""
    client = _build_client(app)
    sftp = client.open_sftp()
    try:
        sftp.remove(remote_path)
    except FileNotFoundError:
        pass
    finally:
        sftp.close()
        client.close()


def _mkdir_p(sftp: paramiko.SFTPClient, remote_dir: str) -> None:
    """Recursively create remote directories."""
    parts = remote_dir.rstrip("/").split("/")
    current = ""
    for part in parts:
        if not part:
            current = "/"
            continue
        current = current.rstrip("/") + "/" + part
        try:
            sftp.stat(current)
        except FileNotFoundError:
            sftp.mkdir(current)


# AREX-specific methods (stub, to be implemented in Task 4)
async def upload_arex_agent(app, local_agent_jar_path: str):
    raise NotImplementedError("To be implemented in Task 4")

async def inject_javaagent_param(app, arex_storage_url: str, agent_remote_path: str):
    raise NotImplementedError("To be implemented in Task 4")

async def get_javaagent_status(app):
    raise NotImplementedError("To be implemented in Task 4")
