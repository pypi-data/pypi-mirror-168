from enum import Enum


class AnalysisFeedback(str, Enum):
    CORRECT = "CORRECT"
    NOT_CORRECT = "NOT_CORRECT"
