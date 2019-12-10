import argparse

class LoggingBase:

    def __init__(self, *args, **kwargs) -> None:
        pass

    def main(self) -> None:
        """Abstract class for main body of the class"""
        raise NotImplementedError
