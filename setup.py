from setuptools import setup

setup(
    name = "Pyvaders",
    options = {
        "build_apps" : {
            # Files that we want to include. Specifically:
            #  * All of our image-files (.png)
            #  * All of our sound- and music-files (.ogg)
            #  * All of our text-files (.txt)
            #  * All of our 3D models (.egg)
            #    - These will be automatically converted
            #      to .bam files
            #  * And all of our font-files (in the "Font" folder)
            "include_patterns" : [
                "gfx/**",
                "snd/**"
            ],
            # We want a gui-app, and our "main" Python file
            # is "Game.py"
            "gui_apps" : {
                "Pyvaders" : "main.py"
            },
            # Plugins that we're using. Specifically,
            # we're using OpenGL, and OpenAL audio
            "plugins" : [
                "pandagl",
                "pandadx9",
                "p3openal_audio",
                "panda3d-gltf"
            ],
            # Platforms that we're building for.
            # Remove those that you don't want.
            "platforms" : [
                "win_amd64"
            ],
            # The name of our log-file. We're keeping
            # the directory-name short--our title is kinda long--
            # and we're placing the file within the user's
            # "app-data" directory.
            "log_filename" : "output.log",
            # Instead of allowing log-data to accumulate,
            # we're here choosing to start the log fresh
            # on each run.
            "log_append" : False
        }
    }
)
