# Tests

This repo includes a pytest-based coverage system. The following describes how to create a test for newly added code.

## 1. Create a File for Your Tests

Once you enter the `tests` directory, first check if there are pre-existing files that you could use to put your tests in. Tests should go in files whose names reflect what is being tested (i.e. `test_JSON.py` stores tests for JSON parsing).

If there are no pre-existing files for your tests, create a new file with a name following this template: `test_(Descriptor).py`, where "(Descriptor)" should be replaced with something that represents what is being tested.

In this new file, import the code that is being tested with `from DataChallenge.(Path to Module) import ...`. Also import any other needed modules (`os` and `sys` will be very common).

## 2. Writing Your Tests

Once you have a file for your tests, you need to actually write them. Pytest is a powerful testing framework, but it has some notable requirements. First, each test must be written as an individual function. Each function also must be named as follows: `def test_(Descriptor)():`, with "Descriptor" replaced with the name of the test. Note that the tests can take __no__ arguments. Finally, pytest uses `assert` statements to determine a test's success. As a result, each test function must have at least one `assert` statement and __no__ `return` statements. If all the assert statements are successful, pytest reports that the test passed. Otherwise, it failed. Pytest will also measure how many lines of the code in the `DataChallenge` directory have been run. This is reported in a coverage report.

## 3. Adding Extra Files for Tests

Some tests will require the reading, writing, or manipulation of external files. If your tests require this, add these extra files in an aptly named subdirectory. For example, the JSON files used in testing JSON parsing are stored in the `JSON` subdirectory. If such a directory already exists, add your files to it. Otherwise, make a new one. Adding new files to these subdirectories to increase the strength of the tests is always encouraged.

__Note:__ When opening these files from your tests, it is highly encouraged to use the absolute path as returned by `os.path.abspath()`. All relative paths used in tests should start at the __repository's root directory__. The reason will be provided in #4.

## 4. Manually Running Tests

Before wrapping up with a set of tests, it is highly recommended that you manually run the tests yourself. To do so, run the following command from the __repository's root directory__: 

```
pytest --cov-report term-missing --cov=./DataChallenge -v
```

The reason this must be run from the repo's root is that the entire testing suite has been setup to make it easy for [Travis CI](https://travis-ci.com/) to run the tests. Since the `.travis.yml` file must be in the repo's root, pytest has been set up to be most easily run from this location. It is possible to run the tests from elsewhere, but it is highly recommended to run it from the repo's root.

## 5. Pushing Your Tests

Once you've made sure your tests are working correctly, push it to GitHub. When you do, the pushed commit will immediately trigger a Travis CI and Coveralls build. This will ensure that your commit didn't break anything. If the coverage percentage drops below 75% for your branch, Coveralls will report a coverage failure. This will greatly decrease your chances of having your branch merged. Covarge failures will decrease the coverage threashold by 0.5%. Due to the timed nature of the project, the coverage threashold is liable to change with little to no warning and might even be removed.
