# This file is part of tdmclient-ty.
# Copyright 2021-2022 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Miniature Mobile Robots group, Switzerland
# Author: Yves Piguet
#
# SPDX-License-Identifier: BSD-3-Clause

from thonny import get_workbench, get_shell
from thonny.common import TextRange
import os

from tdmclient import ClientAsync, NodeLockError, aw
from tdmclient.atranspiler import ATranspiler, TranspilerError
from tdmclient.module_thymio import ModuleThymio
from tdmclient.module_clock import ModuleClock
from tdmclient.atranspiler_warnings import missing_global_decl

import tkinter
from tkinter import ttk


client = None
nodes = []
node_default = None
node = None
robot_view = None


def connect_tdm():
    global client, node
    if client is None:
        try:
            client = ClientAsync(tdm_port=ClientAsync.DEFAULT_TDM_PORT)

            def on_nodes_changed(node_list):
                global nodes, node, node_default
                nodes = [
                    node
                    for node in node_list
                    if node.status != ClientAsync.NODE_STATUS_DISCONNECTED
                ]
                if node not in node_list:
                    node = None
                if node_default not in node_list:
                    node_default = node or (node_list[0] if len(node_list) > 0 else None)
                if robot_view is not None:
                    robot_view.update_nodes(nodes)

            client.on_nodes_changed = on_nodes_changed
            global node_default
            node_default = aw(client.wait_for_node(timeout=5))
            if node_default is not None:
                # refresh target node in node list
                if robot_view is not None:
                    robot_view.update_nodes(nodes)
        except ConnectionRefusedError:
            client = None
            node_default = None
            node = None

def connect():
    connect_tdm()
    global node
    node = node_default if robot_view is None else client.first_node(node_id=robot_view.selected_node_id)
    if node is None:
        print_error("Cannot connect to robot\n")
        return
    try:
        aw(node.lock())
        get_workbench().after(100, process_incoming_messages)  # schedule after 100 ms
    except NodeLockError:
        node = None


def disconnect():
    global node
    if node is not None:
        aw(node.unlock())
        node = None


def process_incoming_messages():
    if client is not None:
        client.process_waiting_messages()
        get_workbench().after(100, process_incoming_messages)  # reschedule after 100 ms


def get_source_code():
    editor = get_workbench().get_editor_notebook().get_current_editor()
    code_view = editor.get_code_view()
    source_code = str(code_view.get_content_as_bytes(), "utf-8")
    return source_code


def get_filename():
    editor = get_workbench().get_editor_notebook().get_current_editor()
    return editor.get_filename()


def print_to_shell(str, stderr=False):
    text = get_shell().text
    text._insert_text_directly(str, ("io", "stderr") if stderr else ("io",))
    text.see("end")


def print_error(*args):
    get_shell().print_error(" ".join([str(arg) for arg in args]))


def print_source_code_lineno(lineno, text=None):
    editor = get_workbench().get_editor_notebook().get_current_editor()
    code_view = editor.get_code_view()

    def click_select_line(event):
        code_view.select_range(TextRange(lineno, 0, lineno + 1, 0))

    get_shell().insert_command_link(text or f"line {lineno}", click_select_line)


def get_transpiled_code(warning_missing_global=False):
    # get source code
    program = get_source_code()

    # transpile from Python to Aseba
    transpiler = ATranspiler()
    modules = {
        "thymio": ModuleThymio(transpiler),
        "clock": ModuleClock(transpiler),
    }
    transpiler.modules = {**transpiler.modules, **modules}
    transpiler.set_preamble("""from thymio import *
""")
    transpiler.set_source(program)
    transpiler.transpile()

    # warnings
    if warning_missing_global:
        w = missing_global_decl(transpiler)
        if len(w) > 0:
            print_error("\n")
            for function_name in w:
                print_error(f"""Warning: in function '{function_name}', redefining variable{"s" if len(w[function_name]) > 1 else ""} {", ".join([f"'{var_name}'" for var_name in w[function_name]])} from outer scope\n""")
                lineno = transpiler.context_top.functions[function_name].function_def.lineno
                print_to_shell("    ")
                print_source_code_lineno(lineno, f"Line {lineno}\n")

    return transpiler.get_output(), transpiler


def print_transpiled_code():
    # get source code transpiled to Aseba
    try:
        program_aseba, _ = get_transpiled_code(warning_missing_global=True)
    except TranspilerError as error:
        print_error(f"\nError: {error.message}\n")
        print_to_shell("    ")
        print_source_code_lineno(error.lineno, f"Line {error.lineno}\n")
        return
    except NameError as error:
        print_error(f"\nError: {error}\n")
        return

    # display in the shell
    print_to_shell("\n" + program_aseba)


print_statements = None
exit_received = False
has_started_printing = False  # to print LF before anything else


def on_event_received(node, event_name, event_data):
    global has_started_printing, exit_received
    if event_name == "_exit":
        exit_received = event_data[0]
        stop()
    elif event_name == "_print":
        print_id = event_data[0]
        print_format, print_num_args = print_statements[print_id]
        print_args = tuple(event_data[1:1 + print_num_args])
        print_str = print_format % print_args
        if not has_started_printing:
            print_to_shell("\n")
            has_started_printing = True
        print_to_shell(print_str + "\n")
    else:
        if not has_started_printing:
            print_to_shell("\n")
            has_started_printing = True
        print_to_shell(event_name + "".join(["," + str(d) for d in event_data]) + "\n")

def run():
    # get source code transpiled to Aseba
    try:
        program_aseba, transpiler = get_transpiled_code(warning_missing_global=True)
    except TranspilerError as error:
        print_error(f"\nError: {error.message}\n")
        print_to_shell("    ")
        print_source_code_lineno(error.lineno, f"Line {error.lineno}\n")
        return
    except NameError as error:
        print_error(f"\nError: {error}\n")
        return

    events = []

    global print_statements
    print_statements = transpiler.print_format_strings
    if len(print_statements) > 0:
        events.append(("_print", 1 + transpiler.print_max_num_args))
    if transpiler.has_exit_event:
        events.append(("_exit", 1))
    for event_name in transpiler.events_in:
        events.append((event_name, transpiler.events_in[event_name]))
    for event_name in transpiler.events_out:
        events.append((event_name, transpiler.events_out[event_name]))

    global has_started_printing, exit_received
    has_started_printing = False
    exit_received = False

    # make sure we're connected
    connect()
    if node is None:
        return

    # run
    async def prog():
        nonlocal events
        if len(events) > 0:
            events = await node.filter_out_vm_events(events)
            await node.register_events(events)
        error = await node.compile(program_aseba)
        if error is not None:
            if "error_msg" in error:
                print_error(f"Compilation error: {error['error_msg']}\n")
            elif "error_code" in error:
                if error["error_code"] in ClientAsync.ERROR_MSG_DICT:
                    print_error(f"Cannot run program ({ClientAsync.ERROR_MSG_DICT[error['error_code']]})\n")
                else:
                    print_error(f"Cannot run program (error {error['error_code']})\n")
            else:
                print_error("Cannot run program\n")
            disconnect()  # to attempt to reconnect next time
        else:
            client.clear_events_received_listeners()
            if len(events) > 0:
                client.add_event_received_listener(on_event_received)
                await node.watch(events=True)
            error = await node.run()
            if error is not None:
                print_error(f"Run error {error['error_code']}\n")
                disconnect()  # to attempt to reconnect next time
            else:
                error = await node.set_scratchpad(program_aseba)
                if error is not None:
                    pass  # ignore

    client.run_async_program(prog)


def stop():
    async def prog():
        error = await node.stop()
        if error is not None:
            print_error(f"Stop error {error['error_code']}\n")
            disconnect()  # to attempt to reconnect next time

    connect()
    if client is None:
        return

    client.run_async_program(prog)


def patch_command(command_id, patched_handler):
    """Replace the handler of a command specified by its id with a function
    patched_handler(c), where c is the command dict.
    """
    workbench = get_workbench()
    workbench._commands = [
        c if c["command_id"] != command_id else {
            **c,
            "handler": (lambda c: lambda: patched_handler(c))(c)
        }
        for c in workbench._commands
    ]


def patch(command_id):
    def register(fun):
        patch_command(command_id, fun)
        return fun
    return register


class RobotView(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        #self.pack()

        self.selected_node_id = None

        self.canvas = tkinter.Canvas(self)
        self.canvas.pack(fill=tkinter.BOTH, expand=True);

        # vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.canvas)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=False)

        # table
        self.table = ttk.Treeview(self.canvas, yscrollcommand=self.scrollbar.set)
        self.table.pack(fill=tkinter.BOTH, expand=True)
        self.table["columns"] = ("selected", "name", "status")
        self.table.column("#0", width=0, stretch=tkinter.NO)
        self.table.column("selected", anchor=tkinter.W, width=20, stretch=False)
        self.table.column("name", anchor=tkinter.W, width=80)
        self.table.column("status", anchor=tkinter.W, width=80)
        self.table.heading("#0", text="", anchor=tkinter.W)
        self.table.heading("selected", text="", anchor=tkinter.W)
        self.table.heading("name", text="Name", anchor=tkinter.W)
        self.table.heading("status", text="Status", anchor=tkinter.W)

        connect_tdm()
        self.update_nodes(nodes)

        def on_select_row(_):
            disconnect()
            selected_node_id = self.table.item(self.table.focus())["text"]
            if selected_node_id:  # guard against double-click
                self.selected_node_id = selected_node_id
            self.update_nodes(nodes)

        self.table.bind("<ButtonRelease-1>", on_select_row)

        # set reference to self
        global robot_view
        robot_view = self

        def process_tdm_messages():
            if client is not None:
                client.process_waiting_messages()
            self.after(100, process_tdm_messages)

        process_tdm_messages()

    def clear(self):
        for item in self.table.get_children():
            self.table.delete(item)

    def add_node(self, node1):
        if "name" not in node1.props or node1.status == ClientAsync.NODE_STATUS_DISCONNECTED:
            return
        selected = (
            node1 == node if node is not None
            else node1.id_str == self.selected_node_id if self.selected_node_id is not None
            else node1 == node_default
        )
        status_str = {
            ClientAsync.NODE_STATUS_UNKNOWN: "unknown",
            ClientAsync.NODE_STATUS_CONNECTED: "connected",
            ClientAsync.NODE_STATUS_AVAILABLE: "available",
            ClientAsync.NODE_STATUS_BUSY: "busy",
            ClientAsync.NODE_STATUS_READY: "ready",
            ClientAsync.NODE_STATUS_DISCONNECTED: "disconnected",
        }[node1.status]
        self.table.insert(parent="", index="end", text=node1.id_str,
                          values=(
                              "\u2713" if selected else "",
                              node1.props["name"] if "name" in node1.props else node1.id_str,
                              status_str
                          ))

    def update_nodes(self, nodes):
        self.clear()
        for node1 in nodes:
            self.add_node(node1)

    def selected_node(self):
        pass


def load_plugin():
    # unload function
    get_workbench().bind("WorkbenchClose", unload_plugin, True)

    # add commands in menus and toolbar
    get_workbench().add_command(command_id="run_th",
                                menu_name="Thymio",
                                command_label="Run on Thymio",
                                default_sequence="<Control-Shift-R>",
                                handler=run,
                                tester = lambda: node is not None,
                                caption="Run current script on Thymio",
                                image=os.path.join(os.path.dirname(__file__), "res", "thymio.run.png"),
                                include_in_toolbar=True)
    get_workbench().add_command(command_id="transpile_th",
                                menu_name="Thymio",
                                command_label="Transpile Program",
                                default_sequence="<Control-Shift-T>",
                                handler=print_transpiled_code)
    get_workbench().add_command(command_id="stop_th",
                                menu_name="Thymio",
                                command_label="Stop Thymio",
                                default_sequence="<Control-Shift-space>",
                                handler=stop,
                                tester = lambda: node is not None,
                                caption="Stop Thymio",
                                image=os.path.join(os.path.dirname(__file__), "res", "thymio.stop.png"),
                                include_in_toolbar=True)
    get_workbench().add_command(command_id="unlock_th",
                                menu_name="Thymio",
                                command_label="Unlock Thymio",
                                handler=disconnect,
                                tester = lambda: node is not None)

    # add view
    get_workbench().add_view(RobotView, "Thymio Robots", "se", default_position_key="zz")

    # patch commands to run and stop .pythii scripts on the Thymio
    @patch("run_current_script")
    def patched_run_current_script(c):
        filename = get_filename()
        if filename is not None and filename.endswith(".pythii"):
            run()
        else:
            c["handler"]()

    @patch("restart")
    def patched_restart(c):
        filename = get_filename()
        if filename is not None and filename.endswith(".pythii"):
            stop()
        else:
            c["handler"]()


def unload_plugin(event=None):
    global client
    if client is not None:
        client.disconnect()
        client = None
