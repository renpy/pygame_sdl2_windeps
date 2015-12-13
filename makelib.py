import subprocess
import argparse
import os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dll")
    ap.add_argument("lib")
    ap.add_argument("machine")

    args = ap.parse_args()

    p = subprocess.Popen(["dumpbin", "/exports", args.dll], stdout=subprocess.PIPE)

    for _ in range(19):
        next(p.stdout)

    def_file = args.lib.replace(".lib", ".def")

    with open(def_file, "w") as f:
        f.write("LIBRARY %s\n" %  os.path.basename(args.dll))
        f.write("EXPORTS\n")

        for l in p.stdout:
            l = l.decode("utf-8")
            l = l.strip()

            if not l:
                break

            f.write(l.split()[3] + "\n")

    p = subprocess.check_call([
        "lib",
        "/def:" + def_file,
        "/out:" + args.lib,
        "/machine:" + args.machine,
        ])

if __name__ == "__main__":
    main()
