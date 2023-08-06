import logging
import os
import shutil
import threading
import tempfile
from threading import Thread

import numpy as np
import trimesh
from flask import Flask, send_file, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

DATA_TYPES = ["mesh", "point_cloud", "urdf"]
DATA_DIRS = {"mesh": "meshes", "point_cloud": "point_clouds", "urdf": "urdfs"}
FILE_EXTS = {"mesh": "ply", "point_cloud": "ply", "urdf": "urdf"}

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


# transforms3d quaternions are in the form [w, x, y, z]
# three.js quaternions are in the form [x, y, z, w]
def quaternion_real_to_last(q):
    return [q[1], q[2], q[3], q[0]]


class WebViewer:
    def __init__(self, port=8080, host="localhost", daemon=True, wait_for_connection=True, verbose=False):
        self.port = port
        self.host = host
        self.verbose = verbose
        self.wait_for_connection = wait_for_connection

        self.cache_dir = tempfile.TemporaryDirectory()
        self.counters = {data_type: 0 for data_type in DATA_TYPES}

        self.scene_meta = {"meshes": [], "point_clouds": [], "urdfs": []}

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        CORS(self.app, resources={r"/*": {"origins": "*"}})

        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

        self.app.add_url_rule("/file/<path:path>", "handle_file", self._handle_file)
        self.app.add_url_rule("/", "handle_index", lambda: send_from_directory(STATIC_DIR, "index.html"))
        self.app.add_url_rule(
            "/manifest.json", "handle_manifest", lambda: send_from_directory(STATIC_DIR, "manifest.json")
        )
        self.app.add_url_rule("/favicon.ico", "handle_favicon", lambda: send_from_directory(STATIC_DIR, "favicon.ico"))
        self.app.add_url_rule("/logo192.png", "handle_logo192", lambda: send_from_directory(STATIC_DIR, "logo192.png"))
        self.app.add_url_rule(
            "/static/<path:path>", "handle_static", lambda path: send_from_directory(STATIC_DIR, path)
        )

        self.socketio.on_event("connect", self._handle_connect)
        self.socketio.on_event("disconnect", self._handle_disconnect)

        if self.wait_for_connection:
            self.wait_event = threading.Event()

        def launch_app():
            print(f"WebViewer running on http://{self.host}:{self.port}")
            self.socketio.run(self.app, port=self.port, host=self.host)

        if daemon:
            thread = Thread(target=launch_app, daemon=True)
            thread.start()
        else:
            launch_app()

        if self.wait_for_connection:
            print("Waiting for connection...")
            self.wait_event.wait()

    def _get_relative_path(self, data_type, name_or_path):
        assert data_type in DATA_TYPES, f"Invalid data type: {data_type}"
        if data_type in FILE_EXTS:
            rel_path = os.path.join(DATA_DIRS[data_type], f"{name_or_path}.{FILE_EXTS[data_type]}")
        else:
            rel_path = os.path.join(DATA_DIRS[data_type], name_or_path)
        return rel_path

    def _generate_name(self, data_type):
        name = f"{self.counters[data_type]:05d}"
        self.counters[data_type] += 1
        return name

    def _get_url(self, rel_path):
        return f"http://{self.host}:{self.port}/file/{rel_path}"

    def _handle_connect(self, *args, **kwargs):
        if self.verbose:
            print("Client connected")
        self._emit_scene()

        if self.wait_for_connection:
            self.wait_event.set()

    def _handle_disconnect(self, *args, **kwargs):
        if self.verbose:
            print("Client disconnected")

    def _handle_file(self, path, *args, **kwargs):
        full_path = os.path.join(self.cache_dir.name, path)
        if self.verbose:
            print(f"Sending file {full_path}")
        return send_file(full_path)

    def _emit_scene(self):
        if self.verbose:
            print("Emitting scene")
        self.socketio.emit("scene", self.scene_meta, broadcast=True)

    def close(self):
        self.cache_dir.cleanup()

    def add_mesh(
        self,
        mesh_or_vertices,
        faces=None,
        vertex_colors=None,
        position=None,
        quaternion=None,
        name=None,
        return_name=False,
    ):
        if isinstance(mesh_or_vertices, str):
            mesh = trimesh.load(mesh_or_vertices)
        elif isinstance(mesh_or_vertices, trimesh.Trimesh):
            mesh = mesh_or_vertices.copy()
        elif isinstance(mesh_or_vertices, np.ndarray):
            mesh = trimesh.Trimesh(vertices=mesh_or_vertices, faces=faces, vertex_colors=vertex_colors)
        else:
            raise ValueError("Invalid mesh type")

        if name is None:
            name = self._generate_name("mesh")

        rel_path = self._get_relative_path("mesh", name)
        full_path = os.path.join(self.cache_dir.name, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        mesh.export(full_path)
        if self.verbose:
            print(f"Exported mesh to {full_path}")

        url = self._get_url(rel_path)

        position = [0, 0, 0] if position is None else position
        quaternion = [1, 0, 0, 0] if quaternion is None else quaternion
        quaternion = quaternion_real_to_last(quaternion)
        assert isinstance(position, list) and len(position) == 3, "Invalid position type"
        assert isinstance(quaternion, list) and len(quaternion) == 4, "Invalid quaternion type"

        self.scene_meta["meshes"].append({"name": name, "url": url, "position": position, "quaternion": quaternion})
        self._emit_scene()

        if return_name:
            return name

    def add_urdf(
        self,
        urdf_path,
        position=None,
        quaternion=None,
        joint_values=None,
        name=None,
        return_name=False,
    ):
        if name is None:
            name = self._generate_name("urdf")

        rel_path = self._get_relative_path("urdf", name)
        rel_dir = os.path.splitext(rel_path)[0]
        os.makedirs(os.path.join(self.cache_dir.name, rel_dir), exist_ok=True)
        full_path = os.path.join(self.cache_dir.name, rel_path)
        with open(urdf_path, "r") as f:
            urdf = f.read()
        urdf = urdf.replace('filename="', f'filename="{name}/')
        with open(full_path, "w") as f:
            f.write(urdf)

        urdf_url = self._get_url(rel_path)

        if self.verbose:
            print(f"Exported URDF to {full_path}")

        shutil.copytree(
            os.path.join(os.path.dirname(urdf_path), "meshes"),
            os.path.join(self.cache_dir.name, rel_dir, "meshes"),
            dirs_exist_ok=True,
        )
        if self.verbose:
            print(f"Copied meshes to {os.path.join(self.cache_dir.name, rel_dir, 'meshes')}")

        joint_values = joint_values or {}
        assert isinstance(joint_values, dict), "Invalid joint values type"
        position = [0, 0, 0] if position is None else position
        quaternion = [1, 0, 0, 0] if quaternion is None else quaternion
        quaternion = quaternion_real_to_last(quaternion)
        assert isinstance(position, list) and len(position) == 3, "Invalid position type"
        assert isinstance(quaternion, list) and len(quaternion) == 4, "Invalid quaternion type"

        self.scene_meta["urdfs"].append(
            {
                "name": name,
                "url": urdf_url,
                "position": position,
                "quaternion": quaternion,
                "jointValues": joint_values,
            }
        )
        self._emit_scene()

        if return_name:
            return name

    def transform_mesh(self, name, position=None, quaternion=None):
        for mesh in self.scene_meta["meshes"]:
            if mesh["name"] == name:
                if position is not None:
                    assert isinstance(position, list) and len(position) == 3, "Invalid position type"
                    mesh["position"] = position
                if quaternion is not None:
                    assert isinstance(quaternion, list) and len(quaternion) == 4, "Invalid quaternion type"
                    mesh["quaternion"] = quaternion_real_to_last(quaternion)
                break
        else:
            raise ValueError(f"Mesh with name {name} not found")

        self._emit_scene()

    def transform_urdf(self, name, position=None, quaternion=None, joint_values=None):
        for urdf in self.scene_meta["urdfs"]:
            if urdf["name"] == name:
                if position is not None:
                    assert isinstance(position, list) and len(position) == 3, "Invalid position type"
                    urdf["position"] = position
                if quaternion is not None:
                    assert isinstance(quaternion, list) and len(quaternion) == 4, "Invalid quaternion type"
                    urdf["quaternion"] = quaternion_real_to_last(quaternion)
                if joint_values is not None:
                    assert isinstance(joint_values, dict), "Invalid joint values type"
                    urdf["jointValues"] = joint_values
                break
        else:
            raise ValueError(f"URDF with name {name} not found")

        self._emit_scene()


if __name__ == "__main__":
    viewer = WebViewer(verbose=True)
    viewer.close()
