from huey import SqliteHuey
import sys

if "pytest" in sys.modules:
    huey = SqliteHuey(immediate=True)
else:
    huey = SqliteHuey()

