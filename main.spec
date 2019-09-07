# -*- mode: python -*-

from kivy_deps import sdl2, angle

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\dev\\Tarefas'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('Logo.png','C:\dev\Tarefas\Images\Logo.png','Data')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Tarefas',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='C:\dev\Tarefas\Images\Logo.png')
coll = COLLECT(exe,
               Tree('C:\\dev\\Tarefas'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + angle.dep_bins)],
               strip=False,
               upx=True,
               name='Tarefas')
