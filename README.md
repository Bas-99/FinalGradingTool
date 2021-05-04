# AutoGraderProject
## Version
Version 1.0.0
## About
This grading tool is developed for a Bachelor End Project at the TU/e. This autograding tool, as it already says, tries to automatically grade assignments. These assigments consist of students having to model and control a plant which has to perform a certain task. The grading tool is made initiate tests on the performance of the controllers, made by the students. These tests are performed in the Digital Twin environment in Unity. The tool will cycle through all supplied assignments, start all the selected tests and record their perfomance. After this performance is recorded, it tests the videos with an already trained Machine Learning algorithm, which determines if the test is performed correctly. All information of an assignment for all different tests combined, results in the grade for the assignement, which is added to a text file containing all the grades. 

![Grader Tool GUI](images_readme/home.PNG)
## Installation
TODO: add install package.
(Required packages)
## Configuration
This chapter is split into two parts, as this tool can be used for grading. But this tool also needs further improvements to make the grading experience and performance even better.
### Use for grading
Follow the steps for the installation and run the grader.exe (to be added). After this application is ran, the application will start itself. 

### Use for development
For development one needs an IDE to work with the python scripts. This project is made with PyCharm, but you are free to use whatever you want. The seperate files are made as structured and clean as possible to make it easier to work with.

## Usage
First the guide for the GUI will be discussed. When running the application, the Home screen listed in the figure above will pop up. From here you have the following options:
1. Directory Setup
2. Simulation Runner
3. Grader

When this is the first time using the grading tool, go to the Directory Setup, when doing this, the following window will pop up.

![Grader Tool Directory Setup](images_readme/dir.PNG)

Follow the steps in the GUI and add a general directory, also add the path to TwinCat (devenv.exe) at last add the Unity simulation path.
After this press the buttons to initialize the selected directory to make it ready for use.
Now to the folder "all_assignments" add all the unzipped assignments you want to grade.
To the folder "ml_models" add the trained machine learning models.

When this step is finished go to the simulation runner, which will show the following window.

![Grader Tool Sim Runner](images_readme/sim.PNG)

Carefully read the notes listed in this GUI to make sure no problems are caused while testing. This process may take a few hours so make sure you don't need your pc for this duration. When the simulation process is finished, navigate to the grader, which will show the following window.

![Grader Tool Grader](images_readme/grader.PNG)

In this window press start grading, to start the grading process. After this is finished, the final grades will pop up on the left. To see the scores for the individual tests per assignments, select a group on the left and the scores will show on the right as seen in the image. If one thinks it is necessary, you can export the grades to a text file using the Export Grades button.





## Points of improvement




