# -*- mode: python -*-

block_cipher = None


a = Analysis(['nbody.py'],
             pathex=['C:\\Users\\Troy\\Documents\\Python Scripts\\nbody'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

ui_file =  [('nbody.ui', 'C:\\Users\\Troy\\Documents\\Python Scripts\\nbody\\nbody.ui', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + ui_file,
          name='nbody',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='nbody.ico')
