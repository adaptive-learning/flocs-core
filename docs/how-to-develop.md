# How to develop

## Start working on the project

1. Install Python 3, virtualenv, virtualenvwrapper and npm:

        $ sudo pacman -S python python-virtualenv python-virtualenvwrapper npm

  If you haven't done it already, we recommend to
  [configure virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#shell-startup-file).

2. Clone the project repository:

        $ git clone https://github.com/adaptive-learning/flocs-core.git flocs

3. Create virtual environment and bind it with the project directory:

        $ cd flocs && mkvirtualenv flocs && setvirtualenvproject

4. Install dependencies:

        $ make install

 The `make install` command uses pip and npm to install all development dependencies.
 See [Makefile](https://github.com/adaptive-learning/flocs-core/blob/master/Makefile) for details.

## Workflow

1. Start the virtual environment and jump to the project directory:

        $ workon flocs

2. Pull the changes from the repository.

        $ git pull

3. Update dependencies:

        $ make update

4. Look at the [issues](https://github.com/effa/flocs/issues) to decide what feature you want to implement.

5. Create and checkout a git branch for the implemented feature.

        $ git checkout -b feature_x

6. Write unit tests for the implemented feature (and possibly integration tests as well).
  Check that the tests don't pass.

        $ make test

7. Develop the feature. Enjoy it, experience the state of flow :-)
  Take a regular breaks (after 25 minutes), stretch yourself (including your eyes).

8. Test the implemented feature and check the code by pylint:

        $ make test
        $ make check

9. Commit changes:

        $ git add changed_files
        $ git commit -m "Implement feature X"

10. Merge the feature branch to the master branch:

        $ git checkout master
        $ git merge feature_x

11. Push changes to the GitHub:

        $ git push

12. Deactivate the virtual environment:

        $ deactivate

13. Celebrate the developed feature with some physical exercise and a healthy snack.
