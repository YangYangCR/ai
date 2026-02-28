import argparse
import importlib.metadata
import sys
import pydevd_pycharm

# 1. 创建解析器
parser = argparse.ArgumentParser(description='这是一个示例程序')

# 2. 添加参数
parser.add_argument('--name', type=str, help='你的名字')
parser.add_argument('--age', type=int, help='你的年龄')

# 3. 解析参数
args = parser.parse_args()

# 4. 使用参数
print(f"你好 {args.name}，你 {args.age} 岁")


if __name__ == "__main__":
    from vllm.entrypoints.utils import VLLM_SUBCMD_PARSER_EPILOG, cli_env_setup
    from vllm.utils.argparse_utils import FlexibleArgumentParser

    import vllm_omni.entrypoints.cli.benchmark.main
    import vllm_omni.entrypoints.cli.serve

    CMD_MODULES = [
        vllm_omni.entrypoints.cli.serve,
        vllm_omni.entrypoints.cli.benchmark.main,
    ]

    cli_env_setup()

    parser = FlexibleArgumentParser(
        description="vLLM OMNI CLI",
        epilog=VLLM_SUBCMD_PARSER_EPILOG.format(subcmd="[subcommand]"),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=importlib.metadata.version("vllm_omni"),
    )
    subparsers = parser.add_subparsers(required=False, dest="subparser")
    cmds = {}
    for cmd_module in CMD_MODULES:
        new_cmds = cmd_module.cmd_init()
        for cmd in new_cmds:
            cmd.subparser_init(subparsers).set_defaults(dispatch_function=cmd.cmd)
            cmds[cmd.name] = cmd
    print("cmds is ", cmds)

    args = parser.parse_args()
    if args.subparser in cmds:
        cmds[args.subparser].validate(args)

    if hasattr(args, "dispatch_function"):
        args.dispatch_function(args)
    else:
        parser.print_help()