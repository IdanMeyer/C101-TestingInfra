
c_file_path = None
def pytest_configure(config):
    global c_file_path
    c_file_path = config.getoption('--path')

def pytest_addoption(parser):
  parser.addoption(
    "--path",
    default=None)

