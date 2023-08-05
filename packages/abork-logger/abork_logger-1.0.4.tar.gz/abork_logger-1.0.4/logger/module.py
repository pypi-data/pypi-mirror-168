
from enum import Enum
import os
from datetime import datetime
from colorama import init
from termcolor import colored


class WrongTypeError(Exception):
    pass


class MessageTypes(Enum):

    SUCCESS = 'green'
    INFO = None
    WARNING = 'yellow'
    ERROR = 'red'


class TargetAbstract:
    
    def log(self, message: str, type: MessageTypes = MessageTypes.INFO, level: int=0):
        raise NotImplementedError('Method "log" not implemented.')

    def get_timestamp(self):
        
        dateTimeObj = datetime.now()
        return dateTimeObj.strftime("%Y.%m.%d %H:%M:%S")


class StdOutTarget(TargetAbstract):

    def __init__(self) -> None:
        init()
    
    def log(self, message: str, type: MessageTypes = MessageTypes.INFO, level: int=0):

        if not type == MessageTypes.INFO:
            message = f'{self.get_timestamp()} {type.name} - {message}'
        else:
            message = f'{self.get_timestamp()} {type.name} - {message}'

        color = type

        for level in range(level):
            message = '-> ' + message

        print(colored(message, color.value))


class LogFileTarget(TargetAbstract):
    
    def __init__(self, filepath, filename='log') -> None:

        if not os.path.exists(filepath):
            raise ValueError('Path does not exist.')
        
        self.file = os.path.join(filepath, filename)

    def log(self, message: str, type: MessageTypes = MessageTypes.INFO, level: int=0):

        if not type == MessageTypes.INFO:
            message = f'{self.get_timestamp()} {type.name} - {message}'
        else: 
            message = f'{self.get_timestamp()} - {message}'

        for level in range(level):
            message = '\t' + message

        message += '\n'

        with open(self.file, mode='a') as file:
            file.write(message)


class Logger:

    def __init__(self, targets: list[TargetAbstract]) -> None:

        if not isinstance(targets, list):
            raise WrongTypeError('Targets is not a list')

        for target in targets:
            if not isinstance(target, TargetAbstract):
                raise WrongTypeError('One of the targets has a wrong type.')
        
        self.targets = targets

    def log_success(self, message, level=0):
        
        self.log(
            message=message,
            type=MessageTypes.SUCCESS,
            level=level
        )

    def log_info(self, message, level=0):
        
        self.log(
            message=message,
            type=MessageTypes.INFO,
            level=level
        )

    def log_warning(self, message, level=0):
        
        self.log(
            message=message,
            type=MessageTypes.WARNING,
            level=level
        )

    def log_error(self, message, level=0):

        self.log(
            message=message,
            type=MessageTypes.ERROR,
            level=level
        )

    def log(self, type: MessageTypes, message: str, level: int):

        for target in self.targets:

            target.log(
                message=message,
                type=type,
                level=level
            )