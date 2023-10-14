import subprocess

def get_clipboard_content():
    try:
        clipboard_text = subprocess.check_output(
            ['xclip', '-selection', 'clipboard', '-o'],
            universal_newlines=True
        )
        return clipboard_text.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# clipboard_content = get_clipboard_content()

# if clipboard_content:
#     print(f'Copied content: {clipboard_content}')
# else:
#     print('Failed to retrieve clipboard content.')
