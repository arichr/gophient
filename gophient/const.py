"""gophient.const - Constants for gophient."""

EOL = b'\r\n'
SEPARATOR = '\t'
TYPES = {
    # General
    '0': 'Text file',
    '1': 'Sub-menu',
    '2': 'CCSO Nameserver',
    '3': 'Failure',
    '4': 'BinHex-encoded file',
    '5': 'DOS file',
    '6': 'uuencoded file',
    '7': 'Full-text search',
    '+': 'Mirror or alternate server',
    'g': 'GIF file',
    'I': 'Image file',
    'T': 'Telnet 3270',
    # Gopher+
    ':': 'Bitmap image',
    ';': 'Movie file',
    '<': 'Sound file',
    # etc.
    'd': 'Document file',
    'h': 'HTML file',
    'i': 'Informational message',
    's': 'Sound file',  # Especially WAV files
    # gophient (never use these types to avoid wrong displaying)
    'ꬰ': 'File',
}
