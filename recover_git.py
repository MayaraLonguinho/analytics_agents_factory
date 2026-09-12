import os
import zlib

os.makedirs("recovered_objects", exist_ok=True)
for root, _, files in os.walk(".git/objects"):
    for file in files:
        if len(file) == 38:
            path = os.path.join(root, file)
            with open(path, "rb") as f:
                compressed = f.read()
            try:
                data = zlib.decompress(compressed)
                if data.startswith(b"blob "):
                    content = data.split(b"\x00", 1)[1]
                    with open(f"recovered_objects/{file}", "wb") as out:
                        out.write(content)
            except Exception:
                pass
