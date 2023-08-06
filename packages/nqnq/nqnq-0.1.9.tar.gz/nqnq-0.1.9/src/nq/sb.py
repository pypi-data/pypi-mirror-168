import subprocess as sb


def test():
    print(sb.run(["python", "i.py"], stdout=sb.PIPE, input="abc".encode("utf-8")))
    print(sb.run(["python", "i.py"], stdout=sb.PIPE))


def bjrun(fp: str, input_text: str, interpreter_path="python"):
    interpreter_loc = sb.run(
        ["which", interpreter_path], stdout=sb.PIPE
    ).stdout.decode()
    interpreter_version = sb.run(
        [interpreter_path, "-VV"], stdout=sb.PIPE
    ).stdout.decode()
    print(f"running {fp} with \n{interpreter_version}at {interpreter_loc}")
    print("--------RES--------")
    result = sb.run(
        [interpreter_path, fp], stdout=sb.PIPE, input=input_text.encode("utf-8")
    ).stdout.decode()
    print(f"{result}--------END--------\n")
