class VoidDataframeException(Exception):
    def __init__(self, message='dataframe is empty'):
        self.message = message
        # Show full traceback
        super().__init__(self.message)


class CorruptDataframeException(Exception):
    def __init__(self, df, message='dataframe does not match Nexus structure'):
        self.message = f'{message} - {df.head()}'
        self.df = df
        # Show full traceback
        super().__init__(self.message)