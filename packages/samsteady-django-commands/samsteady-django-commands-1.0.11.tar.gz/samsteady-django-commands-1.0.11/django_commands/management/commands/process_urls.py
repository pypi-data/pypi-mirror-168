import io
import os
import re
from contextlib import redirect_stdout

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

TRUNCATE_PREFIXES = ["/api/"]
IGNORED_PATH_PATTERNS = ['/api/admin/*',]
ARG_REGEX = re.compile("<.*?>")

def format_name_chunk(name):
    old_chunks = name.split("/")
    new_chunks = []
    for name in old_chunks:
        new_chunks.append(name.capitalize())
    name = "".join(new_chunks)
    name = name.replace("_", "")
    name = name.replace("-", "")
    name = name.replace("/", "")
    return name

class Command(BaseCommand):
    help = "Generates url formatter functions for python and javascript"

    def handle(self, *args, **options):
        old_lines = []
        try:
            f = open("api_routes.py", "r")
            old_lines = f.readlines()
            f.close()
        except FileNotFoundError:
            pass
        try:
            with io.StringIO() as buf, redirect_stdout(buf):
                call_command("show_urls")
                output = buf.getvalue()
            processed_routes = {}
            f = open("api_routes.py", "w")
            for line in output.splitlines():
                line_segs = line.split("\t")
                path = line_segs[0]
                ignored = False
                for pattern in IGNORED_PATH_PATTERNS:
                    if re.match(pattern, path):
                        ignored = True
                        break
                if ignored:
                    continue
                for prefix in TRUNCATE_PREFIXES:
                    if path.startswith(prefix):
                        path = path[len(prefix):]
                        break
                if path.endswith("\.<format>/"):
                    continue
                arg_names = []
                for arg_name in re.findall("<.*?>", path):
                    arg_name = re.findall("[^<].*[^>]", arg_name)[0]
                    if ":" in arg_name:
                        arg_name = arg_name.split(":")[1]
                    arg_names.append(arg_name)
                # func_body = '"' + "{}".join(re.split("<.*?>", path))

                func_body = 'f"'

                raw_name_chunks = re.split("<.*?>/", path)
                name_chunks = []
                for chunk in raw_name_chunks:
                    name_chunks.append(format_name_chunk(chunk))
                func_name = "Api_" + "_x_".join(name_chunks)
                if func_name[-1] == "_" and func_name[-2] != "_":
                    func_name = func_name[:-1]

                path_chunks = re.split("<.*?>", path)
                for i in range(len(arg_names)):
                    path_chunk = path_chunks[i]
                    arg_name = arg_names[i]
                    func_body += path_chunk + "{" + arg_name + "}"
                func_body += path_chunks[-1] + '"'

                arg_list = ", ".join(arg_names)
                func_header = "lambda {}: ".format(arg_list)
                func = func_header + func_body
                should_write = True
                i = 2
                # while func_name in processed_routes:
                #     if processed_routes[func_name] == func:
                #         should_write = False
                #         break
                #     # else:
                #     #     func_name = "{}_{}".format(func_name, format_name_chunk(path_chunks[0][:-1].upper()))
                #     #     i += 1
                if should_write:
                    processed_routes[func_name] = func
                    f.write(func_name + " = " + func + "\n")
            f.write("\n")
            func_name_strings = [f'"{k}"' for k in processed_routes.keys()]
            f.write("__all__ = [" + ", ".join(func_name_strings) + "]")
            f.close()
            try:
                os.system("pj api_routes.py")
            except Exception:
                pass
            f = open("api_routes.py", "r")
            lines = f.readlines()[:-1]
            f.close()
            lines.append("__getattr__ = lambda name: locals()[name] if name in locals() else lambda *args : None")
            f = open("api_routes.py", "w")
            f.writelines(lines)
            f.close()
        except Exception as e:
            f = open("api_routes.py", "w")
            f.writelines(old_lines)
            f.close()
            raise CommandError(e)

