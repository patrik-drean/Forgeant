# -*- mode: python -*-

block_cipher = None


a = Analysis(['forgeant.py'],
             pathex=['/Users/patrikdrean/Documents/python_projects/forgeant/forgeant'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='forgeant',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='forgeant')
app = BUNDLE(coll,
             name='forgeant.app',
             icon=None,
             bundle_identifier=None)
