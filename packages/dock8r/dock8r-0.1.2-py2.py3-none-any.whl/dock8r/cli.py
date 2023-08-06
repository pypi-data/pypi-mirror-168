# -*- coding: utf-8 -*-

import os
import time
import sys
import string
import ast
import click
import randomname
from decouple import config as dconfig
from kubernetes import client, config
from kubernetes.stream import stream
from tabulate import tabulate
import escapism
import datetime, dateutil
import humanfriendly


DOCK8R_NAMESPACE = dconfig("DOCK8R_NAMESPACE", default="docker-sandbox")
DOCK8R_NOTEBOOKS_PVC = dconfig("DOCK8R_NOTEBOOKS_PVC")
DOCK8R_ADDITIONAL_TRACKED_PATHS = ast.literal_eval(dconfig("DOCK8R_ADDITIONAL_TRACKED_PATHS", default='[]'))


def get_username(safe: bool = True):
    username = os.getenv("JUPYTERHUB_USER")
    safe_chars = set(string.ascii_lowercase + string.digits)

    if safe:
        return escapism.escape(username, safe=safe_chars, escape_char="-").lower()
    else:
        return username


def check_path(path_to_test, tracked_paths):
    # Normalize path with regards to ~'s and symlinks
    path_to_test = os.path.realpath(os.path.expanduser(path_to_test))
    for path in tracked_paths:

        if os.path.samefile(os.path.commonpath([path[0], path_to_test]), path[0]):
            rel_path_to_notebook_mount_path = os.path.relpath(path_to_test, path[0])
            return (
                True,
                path[1],
                os.path.join(path[2], rel_path_to_notebook_mount_path),
            )

    return (False, None)


def get_pods_by_container_names(container_names, all_pods_list):
    for pod in all_pods_list:
        if (
            pod.metadata.name in container_names
            or pod.metadata.uid.split("-")[-1] in container_names
        ):
            yield pod


@click.group()
def main():
    """A self-sufficient runtime for containers"""
    pass


@main.command()
def ps():

    user = get_username(safe=True)

    # Configs can be set in Configuration class directly or using helper utility
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(
        namespace=DOCK8R_NAMESPACE, label_selector=f"creator={user}"
    )

    table = []
    for pod in pod_list.items:
        d = (
            datetime.datetime.now(tz=dateutil.tz.tz.tzlocal())
            - pod.metadata.creation_timestamp
        )
        table.append(
            [
                pod.metadata.uid.split("-")[-1],
                pod.spec.containers[0].image,
                pod.spec.containers[0].command,
                humanfriendly.format_timespan(d, max_units=1) + " ago",
                pod.status.phase,
                "",
                pod.metadata.name,
            ]
        )

    headers = [
        "CONTAINER ID",
        "IMAGE",
        "COMMAND",
        "CREATED",
        "STATUS",
        "PORTS",
        "NAMES",
    ]
    print(tabulate(table, headers, tablefmt="plain"))


# Run Docker container as a Kubernetes pod using a random name
@main.command(context_settings={"ignore_unknown_options": True})
@click.argument("image")
@click.option("--interactive", "-i", is_flag=True, help="Keep STDIN open even if not attached")
@click.option("--tty", "-t", is_flag=True, help="Allocate a pseudo-TTY")
@click.option("--rm", is_flag=True, help="Automatically remove the container when it exits")
@click.option("--volume", "-v", multiple=True, help="Bind mount a volume")
@click.argument("args", nargs=-1)
def run(image, interactive, tty, rm, volume, args):
    if interactive:
        click.echo("Interactive option --interactive/-i is not supported yet and will be ignored")
    if tty:
        click.echo("TTY option --tty/-t is not supported yet and will be ignored")
    if rm:
        click.echo("Automatic container remove option --rm is not supported yet and will be ignored")
    user = get_username(safe=True)

    config.load_incluster_config()
    v1 = client.CoreV1Api()

    # Check if mounted volumes are backed by PVCs and create volumes and volumeMounts
    # tracked_paths consists of tuples containing mountPath, PVC name, subPath for attached volumes
    tracked_paths = [
        ("/home/jovyan/work/", DOCK8R_NOTEBOOKS_PVC, user),
        ("/opt/shared/notebooks", DOCK8R_NOTEBOOKS_PVC, "shared"),
        *DOCK8R_ADDITIONAL_TRACKED_PATHS
    ]

    volumes = []
    volume_mounts = []
    for v in volume:
        v.split(":")
        if not len(v.split(":")) == 2:
            click.echo("Volume must be in the form of <local path>:<container path>")
            sys.exit(1)

        local_path = v.split(":")[0]
        container_path = v.split(":")[1]

        result = check_path(local_path, tracked_paths)
        if result[0] == True:
            volumes.append(
                client.V1Volume(
                    name="volume",
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=result[1]
                    ),
                )
            )
            volume_mounts.append(
                client.V1VolumeMount(
                    name="volume", mount_path=container_path, sub_path=result[2]
                )
            )
        else:
            # TODO: Only display the path part of the tuple
            click.echo(
                f"Path must be inside one of the following {', '.join([p[0] for p in tracked_paths])}"
            )
            sys.exit(1)

    # Configure a new Pod with a random name
    pod_name = randomname.get_name(
        adj=("emotions"), noun=("algorithms", "machine_learning", "physics")
    )
    pod = client.V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=client.V1ObjectMeta(name=pod_name, labels={"creator": user}),
        spec=client.V1PodSpec(
            containers=[
                client.V1Container(
                    name="container",
                    image=image,
                    # command=["sleep", "infinity"] if len(cmds)==0 else cmds,
                    args=args,
                    volume_mounts=volume_mounts,
                )
            ],
            volumes=volumes,
            restart_policy="Never"
        ),
    )

    # Create the Pod
    v1.create_namespaced_pod(namespace=DOCK8R_NAMESPACE, body=pod)

    # Wait for pod to be running
    while True:
        pod = v1.read_namespaced_pod(name=pod_name, namespace=DOCK8R_NAMESPACE)
        if pod.status.phase == "Running":
            break
        else:
            time.sleep(1)

    print(pod.metadata.uid)


@main.command()
@click.argument("container")
def logs(container):
    user = get_username(safe=True)

    config.load_incluster_config()
    v1 = client.CoreV1Api()

    pod_list = v1.list_namespaced_pod(
        namespace=DOCK8R_NAMESPACE, label_selector=f"creator={user}"
    )

    for pod in pod_list.items:
        if (
            pod.metadata.name == container
            or pod.metadata.uid.split("-")[-1] == container
        ):
            # Get logs from pod
            logs = v1.read_namespaced_pod_log(
                name=pod.metadata.name,
                namespace=DOCK8R_NAMESPACE,
                follow=False,
                timestamps=False,
            )
            print(logs)
            sys.exit(0)
    else:
        click.echo(f"Container {container} not found")
        sys.exit(1)


@main.command()
@click.argument("container")
@click.option(
    "--interactive", "-i", is_flag=True, help="Keep STDIN open even if not attached"
)
def exec(container, interactive):
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    command = ["/bin/bash"]
    stderr = True
    stdin = True
    stdout = True
    tty = True

    if interactive:
        resp = stream(
            v1.connect_get_namespaced_pod_exec,
            container,
            DOCK8R_NAMESPACE,
            command=command,
            stderr=stderr,
            stdin=stdin,
            stdout=stdout,
            tty=tty,
            _preload_content=False,
        )

        time.sleep(2)
        resp.update()
        resp.write_stdin("\n\n")

        while resp.is_open():
            resp.update()
            lsr = resp.readline_stdout(timeout=0.1)
            out = [lsr]
            while lsr != None:
                resp.update()
                lsr = resp.readline_stdout(timeout=0.1)
                out.append(lsr)

            resp.update()
            command = input("\n".join(out[1:-1])[:-1])
            if command == "exit":
                break
            else:
                resp.write_stdin(command + "\n\n")

        resp.close()


@main.command()
@click.argument("containers", nargs=-1)
def stop(containers):
    user = get_username(safe=True)

    # Configs can be set in Configuration class directly or using helper utility
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(
        namespace=DOCK8R_NAMESPACE, label_selector=f"creator={user}"
    )

    for pod in get_pods_by_container_names(containers, pod_list.items):
        v1.delete_namespaced_pod(
            pod.metadata.name,
            namespace=DOCK8R_NAMESPACE,
            body=client.V1DeleteOptions(),
        )

        # Wait for pod to be deleted
        while True:
            try:
                v1.read_namespaced_pod(pod.metadata.name, namespace=DOCK8R_NAMESPACE)
            except Exception:
                break
            time.sleep(1)

        print(pod.metadata.uid.split("-")[-1])


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
