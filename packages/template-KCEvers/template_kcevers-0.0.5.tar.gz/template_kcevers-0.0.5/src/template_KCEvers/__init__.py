from template_KCEvers import example, tutorial
from template_KCEvers.example import test_path, sum_of_squares # If you don't import these functions here, they won't be available at the top level when having imported template_KCEvers - simply importing the example package does not mean that the functions imported in example/__init__.py become available; they would only be accessible using
# > import template_KCEvers
# > template_KCEvers.example.test_path("C:\\")
from template_KCEvers.tutorial import test_paths, test_sum_of_squares
