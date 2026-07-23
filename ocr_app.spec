import importlib.util
import os

block_cipher = None

# Resolve customtkinter path dynamically
_ctk_spec = importlib.util.find_spec("customtkinter")
_ctk_path = os.path.dirname(_ctk_spec.origin) if _ctk_spec else None

a = Analysis(
    ['ocr_app.py'],
    pathex=[],
    binaries=[],
    datas=(
        [(_ctk_path, 'customtkinter')] if _ctk_path else []
    ),
    hiddenimports=[
        'PIL._tkinter_finder',
        'keyboard.win32',
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PrepGenie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='PrepGenie'
)
