c = get_config()

c.TerminalIPythonApp.display_banner = True

c.InteractiveShellApp.exec_lines = [
    '%autoawait asyncio',
]

c.InteractiveShellApp.exec_files = [
    'utils/ipython/startup.py'
]

c.InteractiveShell.autoindent = True
c.InteractiveShell.confirm_exit = False
c.InteractiveShell.editor = 'nano'

c.PrefilterManager.multi_line_specials = True

c.AliasManager.user_aliases = [
 ('la', 'ls -al')
]
