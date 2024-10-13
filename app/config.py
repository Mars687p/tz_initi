import os

from dotenv import load_dotenv

load_dotenv()

MAX_COUNT_PER_ITERATION = int(os.getenv('MAX_COUNT_PER_ITERATION'))
TIME_PER_ITERATION = float(os.getenv('TIME_PER_ITERATION'))
TYPE_LOAD_TRAFFIC = str(os.getenv('TYPE_LOAD_TRAFFIC'))
